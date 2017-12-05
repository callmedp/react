import json
import mimetypes
import logging
import time
import os
import mimetypes
from random import random

from wsgiref.util import FileWrapper

from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseForbidden,)
# from django.contrib import messages
from django.views.generic import TemplateView, View
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile

# from console.decorators import Decorate, stop_browser_cache
from core.library.haystack.query import SQS
from order.models import Order, OrderItem
from review.models import Review
from emailers.email import SendMail
from emailers.tasks import send_email_task
from emailers.sms import SendSMS
from wallet.models import Wallet
from core.api_mixin import ShineCandidateDetail
from core.mixins import InvoiceGenerate
from console.decorators import Decorate, stop_browser_cache
from search.helpers import get_recommendations
from .dashboard_mixin import DashboardInfo


@Decorate(stop_browser_cache())
class DashboardView(TemplateView):
    template_name = "dashboard/dashboard-inbox.html"

    def get(self, request, *args, **kwargs):
        if request.session.get('candidate_id', None):
            return super(DashboardView, self).get(request, args, **kwargs)
        return HttpResponseRedirect(reverse('homepage'))

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        candidate_id = self.request.session.get('candidate_id', None)
        email = self.request.session.get('email')

        empty_inbox = DashboardInfo().check_empty_inbox(candidate_id=candidate_id)
        if not empty_inbox:
            inbox_list = DashboardInfo().get_inbox_list(candidate_id=candidate_id, request=self.request)

            pending_resume_items = DashboardInfo().get_pending_resume_items(candidate_id=candidate_id, email=email)
            context.update({
                'inbox_list': inbox_list,
                'pending_resume_items': pending_resume_items,
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
                if response.status_code == 200:
                    default_name = 'shine_resume' + timezone.now().strftime('%d%m%Y')
                    file_name = request.session.get('shine_resume_name', default_name)
                    # file_name = file_name + '.' + resume_extn

                    order_items = OrderItem.objects.filter(
                        order__status=1,
                        id__in=list_ids, order__candidate_id=candidate_id,
                        no_process=False, oi_status=2)

                    for obj in order_items:
                        try:
                            order = obj.order
                            file = ContentFile(response.content)
                            file_name = 'resumeupload_shine_resume_' + str(order.pk) + '_' + str(obj.pk) + '_' + str(int(random()*9999)) \
                                + '_' + timezone.now().strftime('%Y%m%d') + '.' + resume_extn
                            full_path = '%s/' % str(order.pk)
                            if not os.path.exists(settings.RESUME_DIR + full_path):
                                os.makedirs(settings.RESUME_DIR +  full_path)
                            dest = open(
                                settings.RESUME_DIR + full_path + file_name, 'wb')
                            for chunk in file.chunks():
                                dest.write(chunk)
                            dest.close()
                        except Exception as e:
                            logging.getLogger('error_log').error("%s-%s" % ('resume_upload', str(e))) 
                            continue

                        # obj.oi_resume.save(file_name, ContentFile(response.content))
                        obj.oi_resume = full_path + file_name
                        last_oi_status = obj.oi_status
                        obj.oi_status = 5
                        obj.last_oi_status = 13
                        obj.save()
                        obj.orderitemoperation_set.create(
                            oi_status=13,
                            oi_resume=obj.oi_resume,
                            last_oi_status=last_oi_status,
                            assigned_to=obj.assigned_to)

                        obj.orderitemoperation_set.create(
                            oi_status=obj.oi_status,
                            last_oi_status=obj.last_oi_status,
                            assigned_to=obj.assigned_to)

                    # with open(file_name, 'wb') as fd:
                    #     for chunk in response.iter_content(chunk_size=128):
                    #         fd.write(chunk)

            elif file:
                extn = file.name.split('.')[-1]
                if extn in ['doc', 'docx', 'pdf'] and list_ids:
                    data = {
                        "list_ids": list_ids,
                        "candidate_resume": file,
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
                self.oi = OrderItem.objects.get(pk=self.oi_pk)
                if self.oi and self.oi.order.candidate_id == self.candidate_id and self.oi.order.status in [1, 3]:
                    pass
                else:
                    return ''
            except:
                return ''
            return super(DashboardDetailView, self).get(request, args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(DashboardDetailView, self).get_context_data(**kwargs)
        if self.oi and self.oi.order.candidate_id == self.candidate_id and self.oi.order.status in [1, 3]:
            ops = []
            if self.oi.product.type_flow in [1, 12, 13]:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 5, 24, 26, 27, 161, 162, 163])
            elif self.oi.product.type_flow == 2:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[5, 6, 161, 162, 163])

            elif self.oi.product.type_flow == 3:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 5, 121, 161, 162, 163])
            elif self.oi.product.type_flow == 4:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 5, 6, 61, 161, 162, 163])
            elif self.oi.product.type_flow == 5:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 5, 6, 61, 161, 162, 163])
            elif self.oi.product.type_flow == 6:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[6, 81, 82, 161, 162, 163])
            elif self.oi.product.type_flow == 7:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[2, 4, 5, 6, 61, 161, 162, 163])
            elif self.oi.product.type_flow == 8:
                oi_status_list = [49, 5, 46, 48, 27, 4, 161, 162, 163]
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=oi_status_list)
            elif self.oi.product.type_flow == 10:
                ops = self.oi.orderitemoperation_set.filter(oi_status__in=[5, 6, 101, 161, 162, 163])
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
                self.oi = OrderItem.objects.get(pk=self.oi_pk)
                if self.oi and self.oi.order.candidate_id == self.candidate_id and self.oi.order.status in [1, 3]:
                    pass
                else:
                    return ''
            except:
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
            except:
                pass
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

    def get(self, request, *args, **kwargs):
        self.candidate_id = request.session.get('candidate_id', None)
        self.oi_pk = request.GET.get('oi_pk')
        if request.is_ajax() and self.oi_pk and self.candidate_id:
            try:
                self.oi = OrderItem.objects.get(pk=self.oi_pk)
                if self.oi and self.oi.order.candidate_id == self.candidate_id and self.oi.order.status in [1, 3] and self.oi.oi_status == 4 and not self.oi.user_feedback:
                    pass
                else:
                    return ''
            except:
                return ''
            return super(DashboardFeedbackView, self).get(request, args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(DashboardFeedbackView, self).get_context_data(**kwargs)
        if self.oi and self.oi.order.candidate_id == self.candidate_id:
            context.update({
                "oi": self.oi,
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
                self.oi = OrderItem.objects.get(pk=self.oi_pk)
                review = request.POST.get('review', '').strip()
                rating = int(request.POST.get('rating', 1))
                if rating and self.oi and self.oi.order.candidate_id == self.candidate_id and self.oi.order.status in [1, 3]:
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
                        average_rating=rating
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
                        to_emails = [self.oi.order.email]
                        email_dict.update({
                            "username": self.oi.order.first_name if self.oi.order.first_name else self.oi.order.candidate_id,
                            "subject": 'You earned a discount coupon worth Rs. <500>',
                            "coupon_code": '',
                            'valid': '',
                        })

                        try:
                            SendMail().send(to_emails, mail_type, email_dict)
                        except Exception as e:
                            logging.getLogger('email_log').error("%s - %s - %s" % (str(to_emails), str(e), str(mail_type)))

                else:
                    data['display_message'] = "select valid input for feedback"
            except:
                data['display_message'] = "select valid input for feedback"
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return HttpResponseForbidden()


class DashboardRejectService(View):
    
    def post(self, request, *args, **kwargs):
        candidate_id = request.session.get('candidate_id', None)
        oi_pk = request.POST.get('oi_pk', None)
        comment = request.POST.get('comment', '').strip()
        reject_file = request.FILES.get('reject_file', '')
        if request.is_ajax() and candidate_id and oi_pk and (comment or reject_file):
            data = {
                "display_message": '',
            }
            try:
                oi = OrderItem.objects.get(pk=oi_pk)
                if oi and oi.order.candidate_id == candidate_id and oi.order.status in [1, 3]:
                    if oi.oi_status in [24, 46]:
                        if reject_file:    
                            try:
                                order = oi.order
                                file = reject_file
                                filename = os.path.splitext(file.name)
                                extention = filename[len(filename)-1] if len(
                                    filename) > 1 else ''
                                file_name = 'draftreject_' + str(order.pk) + '_' + str(oi.pk) + '_' + str(int(random()*9999)) \
                                    + '_' + timezone.now().strftime('%Y%m%d') + extention
                                full_path = '%s/' % str(order.pk)
                                if not os.path.exists(settings.RESUME_DIR + full_path):
                                    os.makedirs(settings.RESUME_DIR +  full_path)
                                dest = open(
                                    settings.RESUME_DIR + full_path + file_name, 'wb')
                                for chunk in file.chunks():
                                    dest.write(chunk)
                                dest.close()
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
            except:
                data['display_message'] = "please do valid action only"
            return HttpResponse(json.dumps(data), content_type="application/json")

        return HttpResponseForbidden()


class DashboardAcceptService(View):
    def post(self, request, *args, **kwargs):
        candidate_id = request.session.get('candidate_id', None)
        oi_pk = request.POST.get('oi_pk', None)
        if request.is_ajax() and candidate_id and oi_pk:
            data = {
                "display_message": '',
            }
            try:
                oi = OrderItem.objects.get(pk=oi_pk)
                if oi and oi.order.candidate_id == candidate_id and oi.order.status in [1, 3]:
                    if oi.oi_status in [24, 46]:
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

                        to_emails = [oi.order.email]
                        email_sets = list(
                            oi.emailorderitemoperation_set.all().values_list(
                                'email_oi_status', flat=True).distinct())
                        sms_sets = list(
                            oi.smsorderitemoperation_set.all().values_list(
                                'sms_oi_status', flat=True).distinct())
                        mail_type = 'WRITING_SERVICE_CLOSED'
                        email_dict = {}
                        email_dict.update({
                            "subject": 'Closing your ' + oi.product.name + ' service',
                            "username": oi.order.first_name,
                            'draft_added': oi.draft_added_on,
                            'mobile': oi.order.mobile,
                        })

                        if oi.product.type_flow in [1, 12, 13] and (9 not in email_sets and 4 not in sms_sets):
                            send_email_task.delay(
                                to_emails, mail_type, email_dict,
                                status=9, oi=oi.pk)
                            try:
                                SendSMS().send(sms_type=mail_type, data=data)
                                oi.smsorderitemoperation_set.create(
                                    sms_oi_status=4,
                                    to_mobile=email_dict.get('mobile'),
                                    status=1)
                            except Exception as e:
                                logging.getLogger('sms_log').error(
                                    "%s - %s" % (str(mail_type), str(e)))

                        elif oi.product.type_flow == 8 and (9 not in email_sets and 4 not in sms_sets):
                            send_email_task.delay(
                                to_emails, mail_type, email_dict,
                                status=9, oi=oi.pk)
                            try:
                                SendSMS().send(sms_type=mail_type, data=data)
                                oi.smsorderitemoperation_set.create(
                                    sms_oi_status=4,
                                    to_mobile=email_dict.get('mobile'),
                                    status=1)
                            except Exception as e:
                                logging.getLogger('sms_log').error(
                                    "%s - %s" % (str(mail_type), str(e)))
                    else:
                        data['display_message'] = "please do valid action only"
            except:
                data['display_message'] = "please do valid action only"
            return HttpResponse(json.dumps(data), content_type="application/json")

        return HttpResponseForbidden()


class DashboardInboxLoadmoreView(View):
    def post(self, request, *args, **kwargs):
        candidate_id = request.session.get('candidate_id', None)
        if request.is_ajax() and candidate_id:
            try:
                page = int(request.POST.get('page', 1))
                last_month_from = int(request.POST.get('last_month_form', 3))
                select_type = int(request.POST.get('select_type', 0))
                orderitem_list = DashboardInfo().get_inbox_list(
                    candidate_id=candidate_id, request=request,
                    last_month_from=last_month_from,
                    select_type=select_type, page=page)
                data = {"orderitem_list": orderitem_list, }
                return HttpResponse(
                    json.dumps(data), content_type="application/json")
            except Exception as e:
                logging.getLogger('error_log').error("%s " % str(e))

        return HttpResponseForbidden()


class DashboardInboxFilterView(View):
    def post(self, request, *args, **kwargs):
        candidate_id = request.session.get('candidate_id', None)
        if request.is_ajax() and candidate_id:
            try:
                last_month_from = int(request.POST.get('last_month_form', 3))
                select_type = int(request.POST.get('select_type', 0))
                orderitem_list = DashboardInfo().get_inbox_list(
                    candidate_id=candidate_id, request=request,
                    last_month_from=last_month_from,
                    select_type=select_type)
                data = {"orderitem_list": orderitem_list, }
                return HttpResponse(
                    json.dumps(data), content_type="application/json")
            except Exception as e:
                logging.getLogger('error_log').error("%s " % str(e))

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
        file_path = settings.MEDIA_ROOT + '/attachment/' + 'Resume Questionnaire.docx'
        path = file_path
        try:
            fsock = FileWrapper(open(path, 'rb'))
        except IOError:
            raise Exception("Resume not found.")

        filename = 'reseme_questionnaire' + '.docx'

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
                    file_path = settings.INVOICE_DIR + invoice.name
                    fsock = FileWrapper(open(file_path, 'rb'))
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
                    file_path = settings.RESUME_DIR + file
                    fsock = FileWrapper(open(file_path, 'rb'))
                    filename = file.split('/')[-1]
                    response = HttpResponse(fsock, content_type=mimetypes.guess_type(filename)[0])
                    response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
                    return response
        except Exception as e:
            logging.getLogger('error_log').error("%s" % str(e))
                        
        return HttpResponseRedirect(reverse('dashboard:dashboard'))

