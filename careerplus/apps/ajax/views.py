import json
import logging
import datetime

from django.views.generic import View, TemplateView
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings

from cms.models import Page
from cms.mixins import LoadMoreMixin
from shop.models import Category
from blog.models import Blog, Comment
from geolocation.models import Country
from review.models import Review
from users.mixins import RegistrationLoginApi
from order.models import Order, OrderItem
from console.order_form import FileUploadForm, VendorFileUploadForm
from emailers.email import SendMail
from emailers.sms import SendSMS
from core.mixins import TokenGeneration
from core.tasks import upload_resume_to_shine
from order.functions import pending_item_email, process_mailer
from console.mixins import ActionUserMixin


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
                pass
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
            except:
                pass
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

            except:
                pass
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
            page_obj = Category.objects.get(slug=slug, active=True)
            products = page_obj.product_set.all()
            paginator = Paginator(products, 1)
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                # products=paginator.page(paginator.num_pages)
                products = 0
            context.update({'products': products, 'page': page, 'slug': slug})
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
            page_obj = Category.objects.get(slug=slug, active=True)
            prod_id_list = page_obj.product_set.values_list('id', flat=True)
            prod_reviews = Review.objects.filter(id__in=prod_id_list)
            paginator = Paginator(prod_reviews, 1)
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
            country = request.GET.get('country', 'India')
            country_obj = Country.objects.get(name=country)
            states = country_obj.state_set.all().values_list('name', flat=True)
            data['states'] = list(states)
        except:
            pass
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
            except:
                pass
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
                    email_dict = {}
                    email_dict.update({
                        "first_name": obj.order.first_name if obj.order.first_name else obj.order.first_name,
                        "subject": 'Your developed document has been uploaded',
                        "email": obj.order.email,
                        "candidateid": obj.order.candidate_id,
                    })

                    mail_type = 'RESUME_CRITIQUE_CLOSED'
                    try:
                        SendMail().send(to_emails, mail_type, email_dict)
                    except Exception as e:
                        logging.getLogger('email_log').error("%s - %s - %s" % (str(to_emails), str(e), str(mail_type)))

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
                    to_emails = [obj.order.email]
                    email_dict = {}
                    email_dict.update({
                        "draft_level": obj.draft_counter,
                        "first_name": obj.order.first_name if obj.order.first_name else obj.order.candidate_id,
                        "email": obj.order.email,
                        "candidateid": obj.order.candidate_id,
                    })

                    if obj.draft_counter == 1:
                        email_dict['subject'] = "Your developed document has been uploaded" 
                        mail_type = 'DRAFT_UPLOAD'
                        try:
                            SendMail().send(to_emails, mail_type, email_dict)
                        except Exception as e:
                            logging.getLogger('email_log').error("%s - %s - %s" % (str(to_emails), str(e), str(mail_type)))

                        try:
                            SendSMS().send(sms_type=mail_type, data=email_dict)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                    elif obj.draft_counter < settings.DRAFT_MAX_LIMIT:
                        email_dict['subject'] = "Your developed document is ready"
                        mail_type = 'DRAFT_UPLOAD'
                        try:
                            SendMail().send(to_emails, mail_type, email_dict)
                        except Exception as e:
                            logging.getLogger('email_log').error("%s - %s - %s" % (str(to_emails), str(e), str(mail_type)))

                        try:
                            SendSMS().send(sms_type=mail_type, data=email_dict)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                    elif obj.draft_counter == settings.DRAFT_MAX_LIMIT:
                        email_dict['subject'] = "Your final document is ready"
                        mail_type = 'DRAFT_UPLOAD'
                        try:
                            SendMail().send(to_emails, mail_type, email_dict)
                        except Exception as e:
                            logging.getLogger('email_log').error("%s - %s - %s" % (str(to_emails), str(e), str(mail_type)))

                        try:
                            SendSMS().send(sms_type=mail_type, data=email_dict)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

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
            except:
                pass
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
            except:
                pass
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
                    if obj.draft_counter == 3:
                        obj.oi_status = 4
                        obj.closed_on = timezone.now()
                    else:
                        obj.oi_status = 46
                    obj.approved_on = timezone.now()
                    obj.save()

                    # mail to candidate
                    to_emails = [obj.order.email]
                    email_dict = {}
                    email_dict.update({
                        "draft_level": obj.draft_counter,
                        "first_name": obj.order.first_name,
                    })

                    if obj.draft_counter == 1:
                        mail_type = 'DRAFT_UPLOAD'
                        try:
                            SendMail().send(to_emails, mail_type, email_dict)
                        except Exception as e:
                            logging.getLogger('email_log').error("%s - %s - %s" % (str(to_emails), str(e), str(mail_type)))

                        try:
                            SendSMS().send(sms_type=mail_type, data=email_dict)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))
                    if obj.draft_counter == 2:
                        mail_type = 'DRAFT_UPLOAD'
                        try:
                            SendMail().send(to_emails, mail_type, email_dict)
                        except Exception as e:
                            logging.getLogger('email_log').error("%s - %s - %s" % (str(to_emails), str(e), str(mail_type)))

                        try:
                            SendSMS().send(sms_type=mail_type, data=email_dict)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))

                    if obj.draft_counter == 3:
                        mail_type = 'DRAFT_UPLOAD'
                        try:
                            SendMail().send(to_emails, mail_type, email_dict)
                        except Exception as e:
                            logging.getLogger('email_log').error("%s - %s - %s" % (str(to_emails), str(e), str(mail_type)))

                        try:
                            SendSMS().send(sms_type=mail_type, data=email_dict)
                        except Exception as e:
                            logging.getLogger('sms_log').error("%s - %s" % (str(mail_type), str(e)))
                            
                    if obj.oi_status == 4:
                        obj.orderitemoperation_set.create(
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
                            oi_status=obj.oi_status,
                            last_oi_status=last_status,
                            assigned_to=obj.assigned_to,
                            added_by=request.user)
            except:
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
            except:
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
                obj.status = 1
                obj.paid_by = request.user
                obj.payment_date = timezone.now()
                obj.save()
                data['display_message'] = "order %s marked paid successfully" % (order_pk)
                # pending item email send
                pending_item_email(order=obj)

                # send email through process mailers
                process_mailer(order=obj)

            except Exception as e:
                data['display_message'] = '%s order id - %s' % (str(e), order_pk)
            return HttpResponse(json.dumps(data), content_type="application/json")
        elif request.is_ajax() and request.user.is_authenticated():
            data['display_message'] = "Permission denied"
            return HttpResponse(json.dumps(data), content_type="application/json")

        return HttpResponseForbidden()
