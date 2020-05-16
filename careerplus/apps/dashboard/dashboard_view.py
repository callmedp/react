import json, ast
import mimetypes
import logging
import time
import os
import mimetypes
from random import random
from dateutil.relativedelta import relativedelta
from wsgiref.util import FileWrapper

from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseForbidden, HttpResponseBadRequest)
# from django.contrib import messages
from django.views.generic import TemplateView, View
from rest_framework.views import APIView
from django.urls import reverse
from django.template.response import TemplateResponse
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile

# from console.decorators import Decorate, stop_browser_cache
from order.models import Order, OrderItem
from resumebuilder.models import Candidate
from resumebuilder.utils import ResumeGenerator
from order.choices import CANCELLED, OI_CANCELLED
from review.models import Review
from emailers.email import SendMail
from emailers.tasks import send_email_task
from emailers.sms import SendSMS
from wallet.models import Wallet
from core.api_mixin import ShineCandidateDetail
from core.mixins import InvoiceGenerate
from console.decorators import Decorate, stop_browser_cache
from search.helpers import get_recommendations
from .dashboard_mixin import DashboardInfo, DashboardCancelOrderMixin
from linkedin.autologin import AutoLogin
from shop.models import Product
from core.library.gcloud.custom_cloud_storage import \
    GCPPrivateMediaStorage, GCPInvoiceStorage, GCPMediaStorage, GCPResumeBuilderStorage


@Decorate(stop_browser_cache())
class DashboardView(TemplateView):
    template_name = "dashboard/dashboard-inbox.html"

    def get(self, request, *args, **kwargs):
        if request.session.get('candidate_id', None):
            return super(DashboardView, self).get(request, args, **kwargs)
        return HttpResponseRedirect(reverse('homepage'))

    def get_context_data(self, **kwargs):

        context = super(DashboardView, self).get_context_data(**kwargs)
        if self.request.GET.get('oirate'):
            try:
                oirate = ast.literal_eval(self.request.GET.get('oirate'))
                context.update({"ref_item_id": oirate[0], "ref_rating": oirate[1]})
            except Exception as e:
                pass
        candidate_id = self.request.session.get('candidate_id', None)
        email = self.request.session.get('email')

        empty_inbox = DashboardInfo().check_empty_inbox(candidate_id=candidate_id)
        if not empty_inbox:
            inbox_list = DashboardInfo().get_inbox_list(candidate_id=candidate_id, request=self.request)

            pending_resume_items = DashboardInfo().get_pending_resume_items(candidate_id=candidate_id, email=email)
            context.update({
                'inbox_list': inbox_list,
                'pending_resume_items': pending_resume_items,
                'candidate_id': candidate_id
            })
        if self.request.flavour == 'mobile' and not empty_inbox:
            if not self.request.session.get('resume_id', None):
                DashboardInfo().check_user_shine_resume(candidate_id=candidate_id, request=self.request)

            if self.request.session.get('resume_id', None):
                context.update({
                    "resume_id": self.request.session.get('resume_id', ''),
                    "shine_resume_name": self.request.session.get('shine_resume_name', ''),
                    "resume_extn": self.request.session.get('extension', ''),
                })
        context.update({
            "empty_inbox": empty_inbox,
        })
        rcourses = get_recommendations(
            self.request.session.get('func_area', None),
            self.request.session.get('skills', None))

        if rcourses:
            rcourses = rcourses[:6]
            context['recommended_products'] = rcourses
        return context

    def post(self, request, *args, **kwargs):
        if request.session.get('candidate_id', None):
            candidate_id = request.session.get('candidate_id')
            file = request.FILES.get('file', '')
            list_ids = request.POST.getlist('resume_pending', [])
            shine_resume = request.POST.get('shine_resume', None)
            resume_extn = request.session.get('resume_extn', '')
            validation_error = ''
            if shine_resume and resume_extn:
                response = ShineCandidateDetail().get_shine_candidate_resume(
                    candidate_id=candidate_id,
                    resume_id=request.session.get('resume_id'))
                if not response:
                    request.session.pop('resume_id')
                    DashboardInfo().check_user_shine_resume(candidate_id=candidate_id,request=request)
                    response = ShineCandidateDetail().get_shine_candidate_resume(
                                                        candidate_id=candidate_id,
                                                        resume_id=request.session.get('resume_id'))
                if response.status_code == 200:
                    file = ContentFile(response.content)
                    data = {
                        "list_ids": list_ids,
                        "candidate_resume": file,
                        'last_oi_status': 13,
                        'is_shine':True,
                        'extension':request.session.get('resume_extn', '')
                    }
                    DashboardInfo().upload_candidate_resume(candidate_id=candidate_id, data=data)
            elif file:
                extn = file.name.split('.')[-1]
                if extn in ['doc', 'docx', 'pdf'] and list_ids:
                    data = {
                        "list_ids": list_ids,
                        "candidate_resume": file,
                        'last_oi_status': 3
                    }
                    DashboardInfo().upload_candidate_resume(candidate_id=candidate_id, data=data)
                elif not list_ids:
                    validation_error = 'Please select atleast one services to upload resume'
                    context = self.get_context_data()
                    context.update({
                        "validation_error": validation_error,
                    })
                    return TemplateResponse(
                        request, ["dashboard/dashboard-inbox.html"], context)
                else:
                    validation_error = 'Only doc, docx and pdf formats are allowed'
                    context = self.get_context_data()
                    context.update({
                        "validation_error": validation_error,
                    })
                    return TemplateResponse(
                        request, ["dashboard/dashboard-inbox.html"], context)
        return HttpResponseRedirect(reverse('dashboard:dashboard'))


class DashboardMyorderView(TemplateView):
    template_name = 'dashboard/dashboard-order.html'

    def get(self, request, *args, **kwargs):

        if request.session.get('candidate_id', None):
            return super(DashboardMyorderView, self).get(request, args, **kwargs)
        return HttpResponseRedirect(reverse('homepage'))

    def get_context_data(self, **kwargs):
        context = super(DashboardMyorderView, self).get_context_data(**kwargs)
        candidate_id = self.request.session.get('candidate_id', None)
        if candidate_id:
            order_list = DashboardInfo().get_myorder_list(candidate_id=candidate_id, request=self.request)
        else:
            order_list = ''

        context.update({
            "order_list": order_list,
        })
        rcourses = get_recommendations(
            self.request.session.get('func_area', None),
            self.request.session.get('skills', None))

        if rcourses:
            rcourses = rcourses[:6]
            context['recommended_products'] = rcourses

        return context


class DashboardDetailView(TemplateView):
    template_name = 'partial/inboxoi-deatil.html'

    def __init__(self):
        self.oi_pk = None
        self.oi = None
        self.candidate_id = None

    def get(self, request, *args, **kwargs):
        self.candidate_id = request.session.get('candidate_id', None)
        if request.is_ajax() and self.candidate_id:
            self.oi_pk = request.GET.get('oi_pk')

            try:

                self.oi = OrderItem.objects.select_related('order').get(pk=self.oi_pk)
                if self.oi and self.oi.order.candidate_id == self.candidate_id and self.oi.order.status in [1, 3]:
                    pass

                else:
                    return ''
            except Exception as e:
                logging.getLogger('error_log').error('unable to fetch order item %s' % str(e))
                return ''
            return super(DashboardDetailView, self).get(request, args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
       
        context = super(DashboardDetailView, self).get_context_data(**kwargs)
        if self.oi and self.oi.order.candidate_id == self.candidate_id and self.oi.order.status in [1, 3]:
            ops = []

            if self.oi.product.type_flow in [1, 12, 13]:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 5, 24, 26, 27, 161, 162, 163, 164, 181])

            elif self.oi.product.vendor.slug == 'neo':
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[5, 33, 4, 161, 162, 163, 164])

            elif self.oi.product.type_flow in [2, 14]:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[5, 6, 161, 162, 163, 164])

            elif self.oi.product.type_flow == 3:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 5, 121, 161, 162, 163, 164])
            elif self.oi.product.type_flow == 4:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 5, 6, 61, 161, 162, 163, 164])
            elif self.oi.product.type_flow == 5:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 5, 6, 61, 161, 162, 163, 164])
            elif self.oi.product.type_flow == 6:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[6, 81, 82, 161, 162, 163, 164])
            elif self.oi.product.type_flow in [7, 15]:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 4, 5, 6, 61, 161, 162, 163, 164])
            elif self.oi.product.type_flow == 8:
                oi_status_list = [2, 49, 5, 46, 48, 27, 4, 161, 162, 163, 181, 164]
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=oi_status_list)
            elif self.oi.product.type_flow == 10:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[5, 6, 101, 161, 162, 163, 164])
            elif self.oi.product.type_flow == 16:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[5, 6, 4])

            context.update({
                "oi": self.oi,
                "max_draft_limit": settings.DRAFT_MAX_LIMIT,
                "ops": list(ops),
            })
        return context


class DashboardCommentView(TemplateView):
    template_name = 'partial/user-inbox-comment.html'

    def __init__(self):
        self.oi_pk = None
        self.oi = None
        self.candidate_id = None

    def get(self, request, *args, **kwargs):
        self.candidate_id = request.session.get('candidate_id', None)
        self.oi_pk = request.GET.get('oi_pk')
        if self.oi_pk and self.candidate_id:
            try:
                self.oi = OrderItem.objects.select_related("order").get(pk=self.oi_pk)

                if self.oi and self.oi.order.candidate_id == self.candidate_id and self.oi.order.status in [1, 3]:
                    pass
                else:
                    return ''
            except Exception as e:
                logging.getLogger('error_log').error('unable to get comments %s' % str(e))
                return ''
            return super(DashboardCommentView, self).get(request, args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(DashboardCommentView, self).get_context_data(**kwargs)
        if self.oi and self.oi.order.candidate_id == self.candidate_id:
            comments = self.oi.message_set.filter(is_internal=False).order_by('created')
            context.update({
                "oi": self.oi,
                "comments": comments,
            })
        return context

    def post(self, request, *args, **kwargs):
        self.candidate_id = request.session.get('candidate_id', None)
        if request.is_ajax() and self.candidate_id:
            self.oi_pk = request.POST.get('oi_pk')
            comment = request.POST.get('comment', '').strip()
            try:
                self.oi = OrderItem.objects.get(pk=self.oi_pk)
                if self.oi.order.candidate_id == self.candidate_id and self.oi.order.status in [1, 3] and comment:
                    self.oi.message_set.create(
                        message=comment,
                        candidate_id=self.candidate_id,
                    )
            except Exception as e:
                logging.getLogger('error_log').error('unable to create comment %s' % str(e))
            redirect_url = reverse('dashboard:dashboard-comment') + '?oi_pk=%s' % (self.oi_pk)
            return HttpResponseRedirect(redirect_url)
        else:
            return HttpResponseForbidden()


class DashboardFeedbackView(TemplateView):
    template_name = 'partial/myinbox-feedback.html'

    def __init__(self):
        self.oi_pk = None
        self.oi = None
        self.candidate_id = None
        self.rating = None
        self.sel_rat = None

    def get(self, request, *args, **kwargs):
        self.candidate_id = request.session.get('candidate_id', None)
        self.oi_pk = request.GET.get('oi_pk')
        self.rating = request.GET.get('rating', None)

        if request.is_ajax() and self.oi_pk and self.candidate_id:
            try:
                self.oi = OrderItem.objects.select_related("order").get(pk=self.oi_pk)
                if self.oi and self.oi.order.candidate_id == self.candidate_id and \
                        self.oi.order.status in [1, 3] and self.oi.oi_status == 4 \
                        and not self.oi.user_feedback:
                    pass
                else:
                    return HttpResponseBadRequest()
            except Exception as e:
                logging.getLogger('error_log').error('unable to get order item object%s' % str(e))
                return HttpResponseBadRequest()
            return super(DashboardFeedbackView, self).get(request, args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(DashboardFeedbackView, self).get_context_data(**kwargs)
        ratings = self.rating
        if ratings:
            self.sel_rat = ratings[-1:]
        else:
            self.sel_rat = 0

        if self.oi and self.oi.order.candidate_id == self.candidate_id:
            context.update({
                "oi": self.oi,
                ratings: 'checked',
                "var": self.sel_rat,

            })
        return context

    def post(self, request, *args, **kwargs):

        email_dict = {}
        self.candidate_id = request.session.get('candidate_id', None)
        self.oi_pk = request.POST.get('oi_pk')
        data = {
            "display_message": 'Thank you for sharing your valuable feedback',
        }
        if request.is_ajax() and self.oi_pk and self.candidate_id:
            try:
                self.oi = OrderItem.objects.select_related("order").get(pk=self.oi_pk)
                review = request.POST.get('review', '').strip()
                rating = int(request.POST.get('rating', 1))
                title = request.POST.get('title', '').strip()
                if rating and self.oi and self.oi.order.candidate_id == self.candidate_id and self.oi.order.status in [
                    1, 3]:
                    name = ''
                    if request.session.get('first_name'):
                        name += request.session.get('first_name')
                    if request.session.get('last_name'):
                        name += ' ' + request.session.get('last_name')

                    email = request.session.get('email')
                    content_type = ContentType.objects.get(app_label="shop", model="product")
                    review_obj = Review.objects.create(
                        content_type=content_type,
                        object_id=self.oi.product.id,
                        user_name=name,
                        user_email=email,
                        user_id=self.candidate_id,
                        content=review,
                        average_rating=rating,
                        title=title
                    )

                    extra_content_obj = ContentType.objects.get(app_label="order", model="OrderItem")

                    review_obj.extra_content_type = extra_content_obj
                    review_obj.extra_object_id = self.oi.id
                    review_obj.save()

                    self.oi.user_feedback = True
                    self.oi.save()
                    # send mail for coupon
                    if self.oi.user_feedback:
                        mail_type = "FEEDBACK_COUPON"
                        to_emails = [self.oi.order.get_email()]
                        email_dict.update({
                            "username": self.oi.order.first_name if self.oi.order.first_name else self.oi.order.candidate_id,
                            "subject": 'You earned a discount coupon worth Rs. <500>',
                            "coupon_code": '',
                            'valid': '',
                        })

                        try:
                            SendMail().send(to_emails, mail_type, email_dict)
                        except Exception as e:
                            logging.getLogger('error_log').error(
                                "%s - %s - %s" % (str(to_emails), str(e), str(mail_type)))

                else:
                    data['display_message'] = "select valid input for feedback"
            except Exception as e:
                logging.getLogger('error_log').error(str(e))

                data['display_message'] = "select valid input for feedback"
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return HttpResponseForbidden()


class DashboardRejectService(View):

    def post(self, request, *args, **kwargs):
        candidate_id = request.session.get('candidate_id', None)
        if not candidate_id:
            candidate_id = request.data.get('candidate_id', None)

        oi_pk = request.POST.get('oi_pk', None)
        if not oi_pk:
            oi_pk = request.data.get('oi_pk', None)

        comment = request.POST.get('comment', '').strip()
        if not comment:
            comment = request.data.get('comment', '').strip()

        reject_file = request.FILES.get('reject_file', '')
        if candidate_id and oi_pk and (comment or reject_file):
            data = {
                "display_message": '',
            }
            try:
                oi = OrderItem.objects.select_related('order').get(pk=oi_pk)
                if oi and oi.order.candidate_id == candidate_id and oi.order.status in [1, 3]:
                    if oi.oi_status in [24, 46]:
                        if reject_file:
                            try:
                                order = oi.order
                                file = reject_file
                                filename = os.path.splitext(file.name)
                                extention = filename[len(filename) - 1] if len(
                                    filename) > 1 else ''
                                file_name = 'draftreject_' + str(order.pk) + '_' + str(oi.pk) + '_' + str(
                                    int(random() * 9999)) \
                                            + '_' + timezone.now().strftime('%Y%m%d') + extention
                                full_path = '%s/' % str(order.pk)
                                if not settings.IS_GCP:
                                    if not os.path.exists(settings.RESUME_DIR + full_path):
                                        os.makedirs(settings.RESUME_DIR + full_path)
                                    dest = open(
                                        settings.RESUME_DIR + full_path + file_name, 'wb')
                                    for chunk in file.chunks():
                                        dest.write(chunk)
                                    dest.close()
                                else:
                                    GCPPrivateMediaStorage().save(settings.RESUME_DIR + full_path + file_name, file)
                                reject_file = full_path + file_name
                            except Exception as e:
                                logging.getLogger('error_log').error("%s-%s" % ('resume_upload', str(e)))
                                raise
                        last_oi_status = oi.oi_status
                        if oi.oi_status == 24:
                            oi.oi_status = 26
                        else:
                            oi.oi_status = 48

                        oi.last_oi_status = last_oi_status
                        oi.save()

                        oi.orderitemoperation_set.create(
                            oi_status=oi.oi_status,
                            last_oi_status=oi.last_oi_status,
                            oi_draft=reject_file,
                            draft_counter=oi.draft_counter,
                            assigned_to=oi.assigned_to
                        )
                        if comment:
                            oi.message_set.create(
                                message=comment,
                                candidate_id=candidate_id
                            )
                        data['display_message'] = "your draft is successfully rejected"
                    else:
                        data['display_message'] = "please do valid action only"
            except Exception as e:
                logging.getLogger('error_log').error(str(e))

                data['display_message'] = "please do valid action only"
            return HttpResponse(json.dumps(data), content_type="application/json")

        return HttpResponseForbidden()


class DashboardAcceptService(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        candidate_id = request.session.get('candidate_id', None)
        if not candidate_id:
            candidate_id = request.data.get('candidate_id', None)
        oi_pk = request.POST.get('oi_pk', None)

        if not oi_pk:
            oi_pk = request.data.get('oi_pk', None)

        if not candidate_id and oi_pk:
            return HttpResponseBadRequest(json.dumps({'result': 'Candidate or order_item pk not available'}),
                                          content_type="application/json")
        data = {
            "display_message": '',
        }
        oi = OrderItem.objects.filter(id=oi_pk).first()

        if not oi and (not oi.order.candidate_id == candidate_id and oi.order.status not in [1, 3]) and\
                oi.oi_status in [24, 46]:
            return HttpResponseBadRequest(json.dumps({'result': 'Valid Actions Only'}), content_type="application/json")

        last_oi_status = oi.oi_status
        oi.oi_status = 4
        oi.closed_on = timezone.now()
        oi.last_oi_status = 27
        oi.save()
        
        oi.orderitemoperation_set.create(
            oi_status=27,
            oi_draft=oi.oi_draft,
            draft_counter=oi.draft_counter,
            last_oi_status=last_oi_status,
            assigned_to=oi.assigned_to
        )

        oi.orderitemoperation_set.create(
            oi_status=oi.oi_status,
            last_oi_status=oi.last_oi_status,
            assigned_to=oi.assigned_to
        )

        data['display_message'] = "You Accept draft successfully"

        to_emails = [oi.order.get_email()]
        email_sets = list(
            oi.emailorderitemoperation_set.all().values_list(
                'email_oi_status', flat=True).distinct())
        sms_sets = list(
            oi.smsorderitemoperation_set.all().values_list(
                'sms_oi_status', flat=True).distinct())
        mail_type = 'WRITING_SERVICE_CLOSED'
        email_dict = {}
        token = AutoLogin().encode(
            oi.order.email, oi.order.candidate_id, days=None)
        email_dict.update({
            "subject": 'Closing your ' + oi.product.name + ' service',
            "username": oi.order.first_name,
            'draft_added': oi.draft_added_on,
            'mobile': oi.order.get_mobile(),
            'upload_url': "%s://%s/autologin/%s/?next=/dashboard" % (
                settings.SITE_PROTOCOL, settings.SITE_DOMAIN, token),
        })

        if oi.product.type_flow in [1, 12, 13] and (9 not in email_sets and 4 not in sms_sets):
            send_email_task.delay(
                to_emails, mail_type, email_dict,
                status=9, oi=oi.pk)
            SendSMS().send(sms_type=mail_type, data=data)
            oi.smsorderitemoperation_set.create(
                sms_oi_status=4,
                to_mobile=email_dict.get('mobile'),
                status=1)

        elif oi.product.type_flow == 8 and (9 not in email_sets and 4 not in sms_sets):
            send_email_task.delay(
                to_emails, mail_type, email_dict,
                status=9, oi=oi.pk)
            SendSMS().send(sms_type=mail_type, data=data)
            oi.smsorderitemoperation_set.create(
                sms_oi_status=4,
                to_mobile=email_dict.get('mobile'),
                status=1)
        return HttpResponse(json.dumps(data), content_type="application/json")


class DashboardInboxLoadmoreView(View):
    def post(self, request, *args, **kwargs):
        candidate_id = request.session.get('candidate_id', None)
        if request.is_ajax() and candidate_id:
            try:
                page = int(request.POST.get('page', 1))
                last_month_from = int(request.POST.get('last_month_from', 3))
                select_type = int(request.POST.get('select_type', 0))
                orderitem_list = DashboardInfo().get_inbox_list(
                    candidate_id=candidate_id, request=request,
                    last_month_from=last_month_from,
                    select_type=select_type, page=page)
                data = {"orderitem_list": orderitem_list, }
                return HttpResponse(
                    json.dumps(data), content_type="application/json")
            except Exception as e:
                logging.getLogger('error_log').error(str(e))

        return HttpResponseForbidden()


class DashboardInboxFilterView(View):
    def post(self, request, *args, **kwargs):
        candidate_id = request.session.get('candidate_id', None)
        if request.is_ajax() and candidate_id:
            try:
                last_month_from = int(request.POST.get('last_month_from', 3))
                select_type = int(request.POST.get('select_type', 0))
                orderitem_list = DashboardInfo().get_inbox_list(
                    candidate_id=candidate_id, request=request,
                    last_month_from=last_month_from,
                    select_type=select_type)
                data = {"orderitem_list": orderitem_list, }
                return HttpResponse(
                    json.dumps(data), content_type="application/json")
            except Exception as e:
                logging.getLogger('error_log').error(str(e))

        return HttpResponseForbidden()


class DashboardNotificationBoxView(TemplateView):
    template_name = 'partial/notification-box.html'

    def __init__(self):
        self.candidate_id = None

    def get(self, request, *args, **kwargs):
        self.candidate_id = request.session.get('candidate_id', None)
        if request.is_ajax() and self.candidate_id:
            return super(DashboardNotificationBoxView, self).get(request, args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(DashboardNotificationBoxView, self).get_context_data(**kwargs)
        email = self.request.session.get('email', None)
        pending_resume_items = DashboardInfo().get_pending_resume_items(candidate_id=self.candidate_id, email=email)
        context.update({
            "pending_resume_items": pending_resume_items,
        })
        candidate_id = self.candidate_id
        if candidate_id:
            if not self.request.session.get('resume_id', None):
                res = ShineCandidateDetail().get_candidate_detail(email=None, shine_id=candidate_id)
                resumes = res['resumes']
                default_resumes = [resume for resume in resumes if resume['is_default']]
                if default_resumes:
                    self.request.session.update({
                        "resume_id": default_resumes[0].get('id', ''),
                        "shine_resume_name": default_resumes[0].get('resume_name', ''),
                        "resume_extn": default_resumes[0].get('extension', ''),
                    })
                    context.update({
                        "resume_id": self.request.session.get('resume_id', ''),
                        "shine_resume_name": self.request.session.get('shine_resume_name', ''),
                        "resume_extn": self.request.session.get('extension', ''),
                    })
            else:
                context.update({
                    "resume_id": self.request.session.get('resume_id', ''),
                    "shine_resume_name": self.request.session.get('shine_resume_name', ''),
                    "resume_extn": self.request.session.get('extension', ''),
                })

        return context


# class DashboardInvoiceDownload(View):

#     def post(self, request, *args, **kwargs):
#         candidate_id = request.session.get('candidate_id', None)
#         email = request.session.get('email', None)
#         try:
#             order_pk = request.POST.get('order_pk', None)
#             order = Order.objects.get(pk=order_pk)
#             if candidate_id and order.status in [1, 3] and (order.email == email or order.candidate_id == candidate_id):
#                 if order.invoice:
#                     invoice = order.invoice
#                 else:
#                     order = InvoiceGenerate().save_order_invoice_pdf(order=order)
#                     invoice = order.invoice
#                 filename = invoice.name.split('/')[-1]
#                 response = HttpResponse(invoice, content_type='application/pdf')
#                 response['Content-Disposition'] = 'attachment; filename=%s' % filename
#                 return response
#         except:
#             raise Exception("Invoice not found.")
#         return HttpResponseRedirect(reverse('dashboard:dashboard-myorder'))


class DownloadQuestionnaireView(View):
    def get(self, request, *args, **kwargs):
        file_path = 'attachment/' + 'Resume Questionnaire.docx'
        path = file_path
        try:
            if not settings.IS_GCP:
                fsock = FileWrapper(open(settings.MEDIA_ROOT + '/' + path, 'rb'))
            else:
                fsock = GCPMediaStorage().open(path)
        except IOError:
            raise Exception("Resume not found.")

        filename = 'resume_questionnaire' + '.docx'

        response = HttpResponse(fsock, content_type=mimetypes.guess_type(path)[0])
        response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
        return response


class DashboardMyWalletView(TemplateView):
    template_name = 'dashboard/dashboard-wallet.html'

    def get(self, request, *args, **kwargs):
        if request.session.get('candidate_id', None):
            return super(DashboardMyWalletView, self).get(request, args, **kwargs)
        return HttpResponseRedirect(reverse('homepage'))

    def get_context_data(self, **kwargs):
        context = super(DashboardMyWalletView, self).get_context_data(**kwargs)
        candidate_id = self.request.session.get('candidate_id', None)
        wal_obj, created = Wallet.objects.get_or_create(owner=candidate_id)
        wal_total = wal_obj.get_current_amount()
        wal_txns = wal_obj.wallettxn.filter(txn_type__in=[1, 2, 3, 4, 5], point_value__gt=0).order_by('-created')
        wal_txns = wal_txns.order_by('-created').select_related('order', 'cart')
        context.update({
            "wal_obj": wal_obj,
            "wal_total": wal_total,
            "wal_txns": wal_txns,
        })
        rcourses = get_recommendations(
            self.request.session.get('func_area', None),
            self.request.session.get('skills', None))

        if rcourses:
            rcourses = rcourses[:6]
            context['recommended_products'] = rcourses
        return context


class DashboardInvoiceDownload(View):

    def post(self, request, *args, **kwargs):
        candidate_id = request.session.get('candidate_id', None)
        email = request.session.get('email', None)
        try:
            order_pk = request.POST.get('order_pk', None)
            order = Order.objects.get(pk=order_pk)
            if candidate_id and order.status in [1, 3] and (order.email == email or order.candidate_id == candidate_id):
                if order.invoice:
                    invoice = order.invoice
                else:
                    order, invoice = InvoiceGenerate().save_order_invoice_pdf(order=order)
                if invoice:
                    file_path = invoice.name
                    if not settings.IS_GCP:
                        file_path = invoice.path
                        fsock = FileWrapper(open(file_path, 'rb'))
                    else:
                        fsock = GCPInvoiceStorage().open(file_path)
                    filename = invoice.name.split('/')[-1]
                    response = HttpResponse(fsock, content_type=mimetypes.guess_type(filename)[0])
                    response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
                    return response
        except Exception as e:
            logging.getLogger('error_log').error("%s" % str(e))

        return HttpResponseRedirect(reverse('dashboard:dashboard-myorder'))


class DashboardResumeDownload(View):

    def get(self, request, *args, **kwargs):
        candidate_id = request.session.get('candidate_id', None)
        email = request.session.get('email', None)
        try:
            order_pk = kwargs.get('pk', None)
            order = Order.objects.get(pk=order_pk)
            if candidate_id and order.status in [1, 3] and (order.email == email or order.candidate_id == candidate_id):
                file = request.GET.get('path', None)
                if file:
                    if file.startswith('/'):
                        file = file[1:]
                    file_path = settings.RESUME_DIR + file
                    if not settings.IS_GCP:
                        fsock = FileWrapper(open(file_path, 'rb'))
                    else:
                        fsock = GCPPrivateMediaStorage().open(file_path)
                    filename = file.split('/')[-1]
                    response = HttpResponse(fsock, content_type=mimetypes.guess_type(filename)[0])
                    response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
                    return response
        except Exception as e:
            logging.getLogger('error_log').error("%s" % str(e))

        return HttpResponseRedirect(reverse('dashboard:dashboard'))


class DashboardResumeTemplateDownload(View):

    def post(self, request, *args, **kwargs):
        
        candidate_id = request.session.get('candidate_id', None)
        email = request.session.get('email', None)
        product_id = request.POST.get('product_id', None)
        product = Product.objects.filter(id=product_id).first()
        if product.sub_type_flow == 1701:
            is_combo = True
        else:
            is_combo = True if product.attr.get_value_by_attribute(product.attr.get_attribute_by_name('template_type')).value == 'multiple' else False
        order_pk = request.POST.get('order_pk', None)
        candidate_obj = Candidate.objects.filter(candidate_id=candidate_id).first()
        selected_template = candidate_obj.selected_template if candidate_obj and candidate_obj.selected_template else 1
        order = Order.objects.get(pk=order_pk)

        if not candidate_id or not order.status in [1, 3, 0] or not (order.email == email) \
                or not (order.candidate_id == candidate_id):
            return HttpResponseRedirect(reverse('dashboard:dashboard-myorder'))

        filename_prefix = "{}_{}".format(order.first_name or "resume", order.last_name or order_pk)
        file_path = settings.RESUME_TEMPLATE_DIR + "/{}/pdf/{}.pdf".format(candidate_obj.id, selected_template)
        content_type = "application/pdf"
        filename_suffix = ".pdf"

        if is_combo:
            file_path = settings.RESUME_TEMPLATE_DIR + "/{}/zip/combo.zip".format(candidate_obj.id)
            content_type = "application/zip"
            filename_suffix = ".zip"

        try:
            if not settings.IS_GCP:
                file_path = "{}/{}".format(settings.MEDIA_ROOT, file_path)
                fsock = FileWrapper(open(file_path, 'rb'))
            else:
                fsock = GCPResumeBuilderStorage().open(file_path)

            filename = filename_prefix + filename_suffix
            response = HttpResponse(fsock, content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
            return response

        except Exception as e:
            logging.getLogger('error_log').error("%s" % str(e))
            return HttpResponseRedirect(reverse('dashboard:dashboard-myorder'))


class DashboardCancelOrderView(View):

    def post(self, request, *args, **kwargs):
        candidate_id = request.session.get('candidate_id', None)
        email = request.session.get('email', None)
        try:
            order_pk = request.POST.get('order_pk', None)
            order = Order.objects.get(pk=order_pk)
            DashboardCancelOrderMixin().perform_cancellation(candidate_id=candidate_id, email=email, order=order)

        except Exception as e:
            logging.getLogger('error_log').error("%s" % str(e))

        return HttpResponseRedirect(reverse('dashboard:dashboard-myorder'))
