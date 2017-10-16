import json
import logging
import datetime

from django.views.generic import View, TemplateView
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from core.library.haystack.query import SQS

from cms.models import Page
from cms.mixins import LoadMoreMixin
from blog.models import Blog, Comment
from geolocation.models import Country
from review.models import Review
from users.mixins import RegistrationLoginApi
from order.models import Order, OrderItem
from console.order_form import FileUploadForm, VendorFileUploadForm
from emailers.tasks import send_email_task
from emailers.sms import SendSMS
from core.mixins import TokenGeneration
from core.tasks import upload_resume_to_shine
from console.mixins import ActionUserMixin
from order.functions import create_short_url
from linkedin.autologin import AutoLogin
from order.mixins import OrderMixin
from order.tasks import pending_item_email, process_mailer
from .functions import draft_upload_mail, roundone_product


class ArticleCommentView(View):
    def post(self, request, *args, **kwargs):
        status = 0
        if request.is_ajax():
            try:
                message = request.POST.get('message').strip()
                pk = request.POST.get('pk', None)
                blog = Blog.objects.get(pk=pk, status=1)

                if request.session.get('candidate_id') and message:
                    name = ''
                    if request.session.get('first_name'):
                        name = request.session.get('first_name')
                    if request.session.get('last_name'):
                        name += ' ' + request.session.get('last_name')
                    Comment.objects.create(blog=blog, message=message, name=name, candidate_id=request.session.get('candidate_id'))
                    status = 1
                    blog.no_comment += 1
                    blog.save()
            except Exception as e:
                logging.getLogger('error_log').error("%s " % str(e))
            data = {"status": status}
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return HttpResponseForbidden()


class ArticleShareView(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            article_slug = request.GET.get('article_slug')
            try:
                obj = Blog.objects.get(slug=article_slug)
                obj.no_shares += 1
                obj.update_score()
                obj.save()
            except Exception as e:
                logging.getLogger('error_log').error("%s " % str(e))
            data = {"status": "success"}
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return HttpResponseForbidden()


class AjaxCommentLoadMoreView(View, LoadMoreMixin):

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            pk = request.POST.get('pk', None)
            page = int(request.POST.get('page', 1))
            try:
                page_obj = Page.objects.get(pk=pk, is_active=True)
                comments = page_obj.comment_set.filter(is_published=True,
                    is_removed=False)
                comment_list = self.pagination_method(page=page,
                    comment_list=comments, page_obj=page_obj)
                return HttpResponse(json.dumps({'comment_list': comment_list}))
            except Exception as e:
                logging.getLogger('error_log').error("Error in loading more comments %s " % str(e))
        return HttpResponseForbidden()


class CmsShareView(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            page_id = request.GET.get('page_id')
            try:
                obj = Page.objects.get(id=page_id)
                obj.total_share += 1
                obj.save()
                today = timezone.now()
                today_date = datetime.date(day=1, month=today.month, year=today.year)
                pg_counter, created = self.page_obj.pagecounter_set.get_or_create(count_period=today_date)
                pg_counter.no_shares += 1
                pg_counter.save()

            except Exception as e:
                logging.getLogger('error_log').error("%s " % str(e))
            data = ["Success"]
            return HttpResponse(json.dumps(list(data)), content_type="application/json")


class AjaxProductLoadMoreView(TemplateView):
    template_name = 'include/load_product.html'

    def get(self, request, *args, **kwargs):
        return super(AjaxProductLoadMoreView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AjaxProductLoadMoreView, self).get_context_data(**kwargs)
        slug = self.request.GET.get('slug', '')
        page = int(self.request.GET.get('page', 1))
        try:
            all_results = SQS().filter(pCtg=slug)
            paginator = Paginator(all_results, 5)
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                # products=paginator.page(paginator.num_pages)
                products = 0
            for product in products:
                if float(product.pPfin):
                    product.discount = round((float(product.pPfin) - float(product.pPin)) * 100 / float(product.pPfin), 2)
            context.update({
                'products': products, 'page': page,
                'slug': slug,
            })
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
        return context


class AjaxReviewLoadMoreView(TemplateView):
    template_name = 'include/load_review.html'

    def get(self, request, *args, **kwargs):
        return super(AjaxReviewLoadMoreView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AjaxReviewLoadMoreView, self).get_context_data(**kwargs)
        slug = self.request.GET.get('slug', '')
        page = int(self.request.GET.get('page', 1))
        try:
            prod_id_list = SQS().filter(pCtg=slug).only('id').values_list('id', flat=True)
            # page_obj = Category.objects.get(slug=slug, active=True)
            # prod_id_list = page_obj.product_set.values_list('id', flat=True)
            prod_reviews = Review.objects.filter(id__in=prod_id_list)
            paginator = Paginator(prod_reviews, 4)
            try:
                page_reviews = paginator.page(page)
            except PageNotAnInteger:
                page_reviews = paginator.page(1)
            except EmptyPage:
                page_reviews = 0
            context.update({'page_reviews': page_reviews, 'page': page, 'slug': slug})
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
        return context


class EmailExistView(View):

    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')
        data = RegistrationLoginApi.check_email_exist(email)
        return HttpResponse(json.dumps(data), content_type="application/json")


class AjaxStateView(View):

    def get(self, request, *args, **kwargs):
        data = {"states": []}
        try:
            country = request.GET.get('country', None)
            country_obj = Country.objects.get(pk=country, active=True)
            states = country_obj.state_set.all().values_list('name', flat=True)
            data['states'] = list(states)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
        return HttpResponse(json.dumps(data), content_type="application/json")


class AjaxOrderItemCommentView(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax() and request.user.is_active:
            try:
                data = {"status": 0}
                if request.is_ajax():
                    oi_pk = request.POST.get('pk', None)
                    message = request.POST.get('message', '').strip()
                    is_internal = request.POST.get('is_internal', False)
                    if is_internal:
                        is_internal = True
                    else:
                        is_internal = False
                    if oi_pk and message:
                        oi_obj = OrderItem.objects.get(pk=oi_pk)
                        oi_obj.message_set.create(
                            message=message,
                            added_by=request.user,
                            is_internal=is_internal)
                        data['status'] = 1
            except Exception as e:
                logging.getLogger('error_log').error("%s " % str(e))
            return HttpResponse(json.dumps(data), content_type="application/json")
        return HttpResponseForbidden()


class ApproveByAdminDraft(View):
    def post(self, request, *args, **kwargs):
        data = {"status": 0}
        if request.is_ajax() and request.user.is_authenticated():
            oi_pk = request.POST.get('oi_pk', None)
            try:
                obj = OrderItem.objects.get(pk=oi_pk)
                data['status'] = 1
                product_flow = obj.product.type_flow

                if product_flow == 3:
                    last_oi_status = obj.last_oi_status
                    obj.oi_status = 4
                    obj.last_oi_status = 121
                    obj.draft_counter += 1
                    obj.closed_on = timezone.now()
                    obj.save()

                    # mail to candidate for resume critique closed
                    to_emails = [obj.order.email]
                    token = token = AutoLogin().encode(obj.order.email, obj.order.candidate_id, days=None)
                    email_sets = list(obj.emailorderitemoperation_set.all().values_list('email_oi_status',flat=True).distinct())
                    email_dict = {}
                    email_dict.update({
                        "first_name": obj.order.first_name if obj.order.first_name else obj.order.first_name,
                        "subject": 'Your developed document has been uploaded',
                        "email": obj.order.email,
                        "candidateid": obj.order.candidate_id,
                        "order_id": obj.order.id,
                        'upload_url': "%s://%s/autologin/%s/?next=dashboard" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token.decode())
                    })

                    mail_type = 'RESUME_CRITIQUE_CLOSED'

                    if 42 not in email_sets:
                        send_email_task.delay(to_emails, mail_type, email_dict, status=42, oi=obj.pk)
                        try:
                            urlshortener = create_short_url(login_url=email_dict)
                            email_dict.update({'url': urlshortener.get('url')})
                            SendSMS().send(sms_type=mail_type, data=email_dict)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))
                    
                    obj.orderitemoperation_set.create(
                        oi_draft=obj.oi_draft,
                        draft_counter=obj.draft_counter,
                        oi_status=121,
                        last_oi_status=last_oi_status,
                        assigned_to=obj.assigned_to,
                        added_by=request.user)

                    obj.orderitemoperation_set.create(
                        oi_status=obj.oi_status,
                        last_oi_status=obj.last_oi_status,
                        assigned_to=obj.assigned_to,
                        added_by=request.user)

                elif product_flow in [1, 12, 13]:
                    last_oi_status = obj.last_oi_status
                    if (obj.draft_counter + 1) == settings.DRAFT_MAX_LIMIT:
                        obj.oi_status = 4
                        obj.last_oi_status = 24
                        obj.closed_on = timezone.now()
                    else:
                        obj.oi_status = 24
                        obj.last_oi_status = last_oi_status
                    obj.draft_counter += 1
                    obj.approved_on = timezone.now()
                    obj.save()

                    # mail to candidate
                    email_sets = list(obj.emailorderitemoperation_set.all().values_list('email_oi_status',flat=True).distinct()) 
                    to_emails = [obj.order.email]
                    token = AutoLogin().encode(obj.order.email, obj.order.candidate_id, days=None)
                    mail_type = 'DRAFT_UPLOAD'
                    data = {}
                    data.update({
                        "draft_level": obj.draft_counter,
                        "first_name": obj.order.first_name if obj.order.first_name else obj.order.candidate_id,
                        "email": obj.order.email,
                        "candidateid": obj.order.candidate_id,
                        "order_id": obj.order.id,
                        'upload_url': "%s://%s/autologin/%s/?next=dashboard" % (settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token.decode()),
                    })

                    draft_upload_mail(oi=obj, to_emails=to_emails, mail_type=mail_type, email_dict=data)
                    if obj.oi_status == 4:
                        obj.orderitemoperation_set.create(
                            oi_status=24,
                            draft_counter=obj.draft_counter,
                            oi_draft=obj.oi_draft,
                            last_oi_status=last_oi_status,
                            assigned_to=obj.assigned_to,
                            added_by=request.user)

                        obj.orderitemoperation_set.create(
                            oi_status=obj.oi_status,
                            last_oi_status=24,
                            assigned_to=obj.assigned_to,
                            added_by=request.user)

                        # sync resume on shine
                        upload_resume_to_shine(oi_pk=obj.pk)
                    else:
                        obj.orderitemoperation_set.create(
                            oi_draft=obj.oi_draft,
                            draft_counter=obj.draft_counter,
                            oi_status=obj.oi_status,
                            last_oi_status=obj.last_oi_status,
                            assigned_to=obj.assigned_to,
                            added_by=request.user)
            except Exception as e:
                logging.getLogger('error_log').error("%s " % str(e))
                
            return HttpResponse(json.dumps(data), content_type="application/json")
        return HttpResponseForbidden()


class RejectByAdminDraft(View):
    def post(self, request, *args, **kwargs):
        data = {"status": 0}
        if request.is_ajax() and request.user.is_authenticated():
            oi_pk = request.POST.get('oi_pk', None)
            try:
                obj = OrderItem.objects.get(pk=oi_pk)
                data['status'] = 1
                last_status = obj.oi_status
                obj.oi_status = 25
                obj.save()
                obj.orderitemoperation_set.create(
                    oi_status=obj.oi_status,
                    last_oi_status=last_status,
                    assigned_to=obj.assigned_to,
                    added_by=request.user)
            except Exception as e:
                logging.getLogger('error_log').error("%s " % str(e))
                
            return HttpResponse(json.dumps(data), content_type="application/json")
        return HttpResponseForbidden()


class UploadDraftView(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax() and request.user.is_authenticated():
            data = {'display_message': "", }
            try:
                flow = int(request.POST.get('flow', 0))
            except Exception as e:
                flow = 0

            if flow in [2, 6, 10]:
                form = VendorFileUploadForm(request.POST, request.FILES)
            else:
                form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    oi_pk = request.POST.get('oi_pk', None)
                    obj = OrderItem.objects.get(pk=oi_pk)
                    mixin_data = {
                        "oi_draft": request.FILES.get('file', ''), }
                    data = ActionUserMixin().upload_draft_orderitem(oi=obj, data=mixin_data, user=request.user)
                except Exception as e:
                    data['display_message'] = str(e)
            else:
                error_message = form.errors.get('file')
                if error_message:
                    data['display_message'] = error_message
            return HttpResponse(json.dumps(data), content_type="application/json")
        return HttpResponseForbidden()


class SaveWaitingInput(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax() and request.user.is_authenticated():
            data = {"message": "Waiting input Not Updated"}
            oi_pk = request.POST.get('oi_pk', None)
            waiting_input = request.POST.get('waiting_input', None)
            try:
                obj = OrderItem.objects.get(pk=oi_pk)
                if waiting_input:
                    obj.waiting_for_input = True
                else:
                    obj.waiting_for_input = False
                obj.save()
                data['message'] = 'Waiting Input Updated Successfully.'
            except Exception as e:
                data['message'] = str(e)
            return HttpResponse(json.dumps(data), content_type="application/json")
        return HttpResponseForbidden()


class ApproveDraftByLinkedinAdmin(View):
    def post(self, request, *args, **kwargs):
        data = {"status": 0}
        if request.is_ajax():
            oi_pk = request.POST.get('oi_pk', None)
            try:
                obj = OrderItem.objects.get(pk=oi_pk)
                data['status'] = 1
                last_status = obj.oi_status
                if obj.product.type_flow == 8:
                    if (obj.draft_counter + 1) == settings.DRAFT_MAX_LIMIT:
                        obj.oi_status = 4
                        obj.closed_on = timezone.now()
                    else:
                        obj.oi_status = 46
                    obj.draft_counter += 1
                    obj.approved_on = timezone.now()
                    obj.save()

                    # mail to candidate
                    to_emails = [obj.order.email]
                    email_sets = list(obj.emailorderitemoperation_set.all().values_list('email_oi_status',flat=True).distinct())
                    sms_sets = list(obj.smsorderitemoperation_set.all().values_list('sms_oi_status',flat=True).distinct())
                    mail_type = 'DRAFT_UPLOAD'
                    token = AutoLogin().encode(obj.order.email, obj.order.candidate_id, days=None)
                    email_dict = {}
                    email_dict.update({
                        "draft_level": obj.draft_counter,
                        "first_name": obj.order.first_name if obj.order.first_name else obj.order.candidate_id,
                        "email": obj.order.email,
                        "candidateid": obj.order.candidate_id,
                        "order_id": obj.order.id,
                        'upload_url': "%s/autologin/%s/?next=dashboard" % (settings.SITE_DOMAIN, token.decode()),
                    })

                    if obj.draft_counter == 1:
                        if 102 not in email_sets and 102 not in sms_sets:
                            send_email_task.delay(to_emails, mail_type, email_dict, status=102, oi=obj.pk)
                            try:
                                urlshortener = create_short_url(login_url=email_dict)
                                email_dict.update({'url': urlshortener.get('url')})
                                SendSMS().send(sms_type=mail_type, data=email_dict)
                                obj.smsorderitemoperation_set.create(sms_oi_status=102)
                            except Exception as e:
                                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))
                    elif obj.draft_counter == 2:
                        if 103 not in email_sets and 103 not in sms_sets:
                            send_email_task.delay(to_emails, mail_type, email_dict, status=103, oi=obj.pk)
                            try:
                                urlshortener = create_short_url(login_url=email_dict)
                                email_dict.update({'url': urlshortener.get('url')})
                                SendSMS().send(sms_type=mail_type, data=email_dict)
                                obj.smsorderitemoperation_set.create(sms_oi_status=103)
                            except Exception as e:
                                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                    elif obj.draft_counter == settings.DRAFT_MAX_LIMIT and 104 not in email_sets:
                        if 104 not in email_sets and 104 not in sms_sets:
                            send_email_task.delay(to_emails, mail_type, email_dict, status=104, oi=obj.pk)
                            try:
                                urlshortener = create_short_url(login_url=email_dict)
                                email_dict.update({'url': urlshortener.get('url')})
                                SendSMS().send(sms_type=mail_type, data=email_dict)
                                obj.smsorderitemoperation_set.create(sms_oi_status=104)
                            except Exception as e:
                                logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                    if obj.oi_status == 4:
                        obj.orderitemoperation_set.create(
                            linkedin=obj.oio_linkedin,
                            draft_counter=obj.draft_counter,
                            oi_status=46,
                            last_oi_status=last_status,
                            assigned_to=obj.assigned_to,
                            added_by=request.user)

                        obj.orderitemoperation_set.create(
                            oi_status=obj.oi_status,
                            last_oi_status=46,
                            assigned_to=obj.assigned_to,
                            added_by=request.user)
                    else:
                        obj.orderitemoperation_set.create(
                            linkedin=obj.oio_linkedin,
                            draft_counter=obj.draft_counter,
                            oi_status=obj.oi_status,
                            last_oi_status=last_status,
                            assigned_to=obj.assigned_to,
                            added_by=request.user)
            except Exception as e:
                logging.getLogger('error_log').error("%s " % str(e))
                pass
            return HttpResponse(json.dumps(data), content_type="application/json")
        return HttpResponseForbidden()


class RejectDraftByLinkedinAdmin(View):
    def post(self, request, *args, **kwargs):
        data = {"status": 0}
        if request.is_ajax():
            oi_pk = request.POST.get('oi_pk', None)
            try:
                obj = OrderItem.objects.get(pk=oi_pk)
                data['status'] = 1
                last_status = obj.oi_status
                obj.oi_status = 47
                obj.save()
                obj.orderitemoperation_set.create(
                    oi_status=obj.oi_status,
                    last_oi_status=last_status,
                    assigned_to=obj.assigned_to,
                    added_by=request.user)
            except Exception as e:
                logging.getLogger('error_log').error("%s " % str(e))
                pass
            return HttpResponse(json.dumps(data), content_type="application/json")
        return HttpResponseForbidden()


class GenerateAutoLoginToken(View):
    def post(self, request, *args, **kwargs):
        data = {"status": 0, "display_message": ''}
        if request.is_ajax() and request.user.is_authenticated():
            try:
                email = request.POST.get('email', '')
                enc_type = int(request.POST.get('type', 1))
                exp_days = int(request.POST.get('expires', 30))
                token = TokenGeneration().encode(email, enc_type, exp_days)
                data.update({
                    "token": token,
                })
                data["status"] = 1
            except Exception as e:
                data['display_message'] = str(e)
            return HttpResponse(json.dumps(data), content_type="application/json")
        return HttpResponseForbidden()


class MarkedPaidOrderView(View):
    def post(self, request, *args, **kwargs):
        data = {"status": 0, "display_message": ''}
        if request.is_ajax() and request.user.is_authenticated() and request.user.has_perm('order.can_mark_order_as_paid'):
            order_pk = request.POST.get('order_pk', None)
            try:
                obj = Order.objects.get(pk=order_pk)
                data['status'] = 1
                payment_date = timezone.now()
                obj.status = 1
                obj.paid_by = request.user
                obj.payment_date = payment_date
                obj.save()

                txn_objs = obj.ordertxns.filter(status=0)
                for txn_obj in txn_objs:
                    txn_obj.status = 1
                    txn_obj.payment_date = payment_date
                    txn_obj.save()

                data['display_message'] = "order %s marked paid successfully" % (str(order_pk))
                # add reward_point in wallet
                OrderMixin().addRewardPointInWallet(order=obj)
                # pending item email send
                pending_item_email.apply_async((obj.pk), countdown=900)

                # send email through process mailers
                process_mailer.apply_async((obj.pk), countdown=900)

                #roundone order
                roundone_product(order=obj)

            except Exception as e:
                data['display_message'] = '%s order id - %s' % (str(e), str(order_pk))
            return HttpResponse(json.dumps(data), content_type="application/json")
        elif request.is_ajax() and request.user.is_authenticated():
            data['display_message'] = "Permission denied"
            return HttpResponse(json.dumps(data), content_type="application/json")

        return HttpResponseForbidden()
