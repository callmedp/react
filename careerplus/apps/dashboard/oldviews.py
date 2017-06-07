# stdlib imports
import os
from random import random
from datetime import datetime
import logging
import json

# django imports
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import Http404
from django.views.generic.base import TemplateView, View
from django.contrib.messages import get_messages
from django.shortcuts import HttpResponseRedirect
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseForbidden
from django.middleware.csrf import get_token

from constance import config
from copy import deepcopy

# app imports
from shinecp.cart.views import CommonContext
from shinecp.cart.models import Order, OrderItem, Message, OrderItemOperation
from shinecp.theme.utils import delete_session_keys, fetchDir
from shinecp.config import delivery_types_4_sms
from channel.utils import superexpress_sms
from product.models import Feedback
from core.common import OrderItemAllocation, PersonalRecommendation, Invoice
from cashback.models import WalletTransaction
from core.common import Token, CampaignUrl, ShineCandidateDetail
from mailers.email import SendMail
from mailers.sms import SendSMS
from mailers.mailers_config import MAIL_TYPE, SMS_TYPE
from shinecp.theme.utils import is_mobile_browser
from resume_builder.views import ResumeBuilderContext
from microsite.roundone import RoundOneAPI
from channel.utils import sms_for_delivery_type
# self-app imports
from .mixins import AjaxPostResponseRedirectView, HasRoundOneOrderMixin
from .config import ROUNDONE_REFERRAL_STATUS, ROUNDONE_PAST_STATUS,\
    ROUNDONE_INTERACTION_RESULT, ROUNDONE_PAST_ACTION, ROUNDONE_FINAL_RESULT


class DashboardView(CommonContext, TemplateView):
    template_name = "dashboard/inbox.html"

    def get(self, request, *args, **kwargs):

        if is_mobile_browser(self.request):
            return HttpResponseRedirect(
                reverse_lazy('mobile:mobile_dashboard_inbox'))
        return super(DashboardView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context.update(self.get_common_context_data())

        orders = self.request.user.order_set.filter(status__in=[2, 5])

        feedback_qs = Feedback.objects.filter(user=self.request.user)
        user_feedback = feedback_qs.values_list(
            'productvariation__id', flat=True)

        is_coupon_sent = feedback_qs.filter(coupon_sent=True).exists()
        messages = get_messages(self.request)

        # recommended/upsell products
        upsell_products = self.get_dashboard_upsell(orders)

        if hasattr(self.request.user, 'wallet'):
            wallet = self.request.user.wallet

            wallet_transaction = WalletTransaction.objects.filter(
                wallet=wallet, status=2,
                type_cashback__in=[1, 2]).order_by('-created_on')

            if wallet_transaction.count() > 0:
                wallet_transaction_obj = wallet_transaction
            else:
                wallet_transaction_obj = None

        else:
            wallet = None
            wallet_transaction_obj = None

        linkedin_flag = False

        context.update({
            'orders': orders,
            'allow_accept_reject_operation_types': (2, 3, ),
            'final_draft_operation_types': (4, ),
            'allow_oio_operation_types': (0, 1, 2, 3, 4, 9, 12, 14),
            'show_error_status_for': (0, 5, 6, 13, ),
            'show_success_status_for': (4, 12, ),
            'helpline_nos': config.SALES_NOS,
            'helpline_time': '9AM TO 6PM',
            'user_feedback': user_feedback,
            'upsell_products': upsell_products,
            'is_coupon_sent': is_coupon_sent,
            'questionaire_category': ('Executive Bio', 'Profile Updates',),
            'resume_non_download_category': (
                'Job Referral', 'Resume Showcase', 'Profile Updates'),
            'resume_type_category': (
                'Resume Writing', 'Resume Plus (Visual Resume)'),
            'messages': messages,
            'wallet': wallet,
            'wallet_transaction_obj': wallet_transaction_obj,
            'inbox_active': True
        })

        return context

    def get_dashboard_upsell(self, orders):
        user_email = None
        if self.request.user.is_authenticated() and self.request.user.email:
            user_email = self.request.user.email
        upsells = PersonalRecommendation().get_variation_qs(
            email=user_email, orders=orders)
        return upsells


class DashboardOrderView(CommonContext, TemplateView):
    template_name = "dashboard/orders.html"

    def get(self, request, *args, **kwargs):

        if is_mobile_browser(self.request):
            return HttpResponseRedirect(
                reverse_lazy('mobile:mobile_dashboard_inbox'))
        return super(DashboardOrderView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context.update(self.get_common_context_data())

        orders = self.request.user.order_set.filter(status__in=[2, 5])

        feedback_qs = Feedback.objects.filter(user=self.request.user)
        user_feedback = feedback_qs.values_list(
            'productvariation__id', flat=True)

        is_coupon_sent = feedback_qs.filter(coupon_sent=True).exists()
        messages = get_messages(self.request)

        # recommended/upsell products
        upsell_products = self.get_dashboard_upsell(orders)

        if hasattr(self.request.user, 'wallet'):
            wallet = self.request.user.wallet

            wallet_transaction = WalletTransaction.objects.filter(
                wallet=wallet, status=2,
                type_cashback__in=[1, 2]).order_by('-created_on')

            if wallet_transaction.count() > 0:
                wallet_transaction_obj = wallet_transaction
            else:
                wallet_transaction_obj = None

        else:
            wallet = None
            wallet_transaction_obj = None
        linkedin_flag = False

        context.update({
            'orders': orders,
            'allow_accept_reject_operation_types': (2, 3, ),
            'final_draft_operation_types': (4, ),
            'allow_oio_operation_types': (0, 1, 2, 3, 4, 9, 12, 14),
            'show_error_status_for': (0, 5, 6, 13, ),
            'show_success_status_for': (4, 12, ),
            'helpline_nos': config.SALES_NOS,
            'helpline_time': '9AM TO 6PM',
            'user_feedback': user_feedback,
            'upsell_products': upsell_products,
            'is_coupon_sent': is_coupon_sent,
            'questionaire_category': ('Executive Bio', 'Profile Updates',),
            'resume_non_download_category': (
                'Job Referral', 'Resume Showcase', 'Profile Updates'),
            'resume_type_category': (
                'Resume Writing', 'Resume Plus (Visual Resume)'),
            'messages': messages,
            'wallet': wallet,
            'wallet_transaction_obj': wallet_transaction_obj,
            'order_active': True
        })

        return context

    def get_dashboard_upsell(self, orders):
        user_email = None
        if self.request.user.is_authenticated() and self.request.user.email:
            user_email = self.request.user.email
        upsells = PersonalRecommendation().get_variation_qs(
            email=user_email, orders=orders)
        return upsells


class DashboardRecommendView(CommonContext, TemplateView):
    template_name = "dashboard/recommended.html"

    def get(self, request, *args, **kwargs):

        if is_mobile_browser(self.request):
            return HttpResponseRedirect(
                reverse_lazy('mobile:mobile_dashboard_recommend'))
        return super(DashboardRecommendView, self).get(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context.update(self.get_common_context_data())

        context = super(self.__class__, self).get_context_data(**kwargs)
        context.update(self.get_common_context_data())

        orders = self.request.user.order_set.filter(status__in=[2, 5])
        upsell_products = self.get_dashboard_upsell(orders)

        context.update({
            'orders': orders,
            'helpline_nos': config.SALES_NOS,
            'helpline_time': '9AM TO 6PM',
            'upsell_products': upsell_products,
            'reco_active': True
        })

        return context

    def get_dashboard_upsell(self, orders):
        user_email = None
        if self.request.user.is_authenticated() and self.request.user.email:
            user_email = self.request.user.email
        upsells = PersonalRecommendation().get_variation_qs(
            email=user_email, orders=orders)
        return upsells


class DashboardCreditView(CommonContext, TemplateView):
    template_name = "dashboard/credits.html"

    def get(self, request, *args, **kwargs):

        if is_mobile_browser(self.request):
            return HttpResponseRedirect(
                reverse_lazy('mobile:mobile_dashboard_credits'))
        return super(DashboardCreditView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context.update(self.get_common_context_data())

        orders = self.request.user.order_set.filter(status__in=[2, 5])
        messages = get_messages(self.request)

        if hasattr(self.request.user, 'wallet'):
            wallet = self.request.user.wallet

            wallet_transaction = WalletTransaction.objects.filter(wallet=wallet, status=2, type_cashback__in=[1, 2]).order_by('-created_on')

            if wallet_transaction.count() > 0:
                wallet_transaction_obj = wallet_transaction
            else:
                wallet_transaction_obj = None

        else:
            wallet = None
            wallet_transaction_obj = None

        context.update({
            'orders': orders,
            'helpline_nos': config.SALES_NOS,
            'helpline_time': '9AM TO 6PM',
            'wallet': wallet,
            'wallet_transaction_obj': wallet_transaction_obj,
            'credits_active': True
        })

        return context


class OioMessageCreateView(AjaxPostResponseRedirectView):

    http_method_names = ['post', ]
    model = Message
    url = reverse_lazy('user_dashboard')

    def post_response(self, request):
        try:
            order_item = OrderItem.objects.get(
                pk=self.request.POST.get('order_item'),
                order__candidate=self.request.user)
        except OrderItem.DoesNotExist:
            raise Http404('User are not allowed to access this order item.')
        message = self.request.POST.get('message')
        if message:
            self.model.objects.create(**{
                'oio': order_item.get_most_recent_operation(),
                'from_user': self.request.user,
                'message': self.request.POST.get('message')
            })
            messages.add_message(
                request, messages.INFO, 'Message sent Successfully.')
        return True


class ResumeActionView(AjaxPostResponseRedirectView):

    http_method_names = ['post', ]

    def post_response(self, request):
        rejected_with_upload = False
        no_of_closed_objs = no_of_objs = 0
        latest_oio = None

        item = int(request.POST.get('item', 0))
        order_item = int(request.POST.get('order_item', 0))
        action = int(request.POST.get('action', 0))
        comment = request.POST.get('comments', 0)
        last_op = None
        try:
            o_item = OrderItem.objects.get(pk=order_item, order__candidate=self.request.user)
            last_op = o_item.get_most_recent_operation()
        except OrderItem.DoesNotExist:
            return HttpResponseRedirect(reverse_lazy('user_dashboard'))
         
        if action not in [4, 6]:
            messages.add_message(request, messages.ERROR, 'Invalid Action')
            return HttpResponseRedirect(reverse_lazy('user_dashboard'))
        if last_op:
            if last_op.operation_type not in [2,3]:
                messages.add_message(request, messages.ERROR, 'Cannot Accept/Reject Now.')
                return HttpResponseRedirect(reverse_lazy('user_dashboard'))

        try:
            if order_item:
                item_object = OrderItem.objects.get(pk=int(order_item)).orderitemoperation_set.latest('pk')
            else:
                item_object = OrderItemOperation.objects.get(pk=int(item), operation_changed_from=0)
        except Exception:
            messages.add_message(request, messages.ERROR, 'Invalid Order Item.')
            return HttpResponseRedirect(reverse_lazy('user_dashboard'))
        order_assinged_by = item_object.order_item.orderitemoperation_set.filter(operation_type=7)
        if order_assinged_by:
            latest_oio = order_assinged_by.latest('added_on')
        
        if request.FILES and action == 6:
            rejected_with_upload = True

            upload_full_path = '/%s/%s_%s' % (
                fetchDir(str(item_object.order_item.order.candidate.pk)),
                str(item_object.order_item.order.candidate.pk),
                str(item_object.order_item.order.pk))

            f_obj = request.FILES['resume_uploader']
            file_name_tuple = os.path.splitext(f_obj.name)
            extention = file_name_tuple[len(
                file_name_tuple)-1] if len(file_name_tuple) > 1 else ''

            file_name = str(item_object.order_item.order.candidate.pk)+'_'+str(
                item_object.order_item.order.pk)+'_'+str(
                int(random()*9999))+extention

            if not os.path.exists(
               settings.UPLOADS_DIR_RESUME+upload_full_path):
                os.makedirs(settings.UPLOADS_DIR_RESUME+upload_full_path)
            dest = open(
                settings.UPLOADS_DIR_RESUME + upload_full_path + '/' + file_name, 'wb')

            for chunk in f_obj.chunks():
                dest.write(chunk)
            dest.close()

            if settings.ENABLE_S3:
                from shinecp.theme.tasks import upload_aws
                upload_aws.delay(
                    {'upload_dir': settings.UPLOADS_DIR_RESUME,
                     'resume_path': upload_full_path,
                     'file_name': file_name})

        count = order_assinged_by.count()

        user = User.objects.get(email=request.user.email if request.user.email else request.session.get('email'))

        if rejected_with_upload:
            resume = upload_full_path+'/'+file_name
            operation_changed_from = 13
        else:
            resume = item_object.resume
            operation_changed_from = 0
        linkedin = None

        if o_item.new_status:
            if o_item.variation.sub_type_of_product == 7:
                linkedin = item_object.linkedin
                if not linkedin:
                    linkedin = o_item.oio_linkedin

        if action == 6 and item_object:
            item_object.operation_changed_from = 6
            item_object.save()

            if linkedin:
                linkedin = self.make_copy_draft(draft=linkedin)

            if latest_oio:
                if latest_oio.assigned_by == latest_oio.assigned_to:
                    try:
                        latest_oio = OrderItemOperation.objects.filter(order_item=item_object.order_item, operation_type=8).latest('added_on')
                    except:
                        pass
                    oio = OrderItemOperation.objects.create(order_item_id=int(item_object.order_item.id),
                                                            resume=resume,
                                                            operation_type=6,
                                                            assigned_by=user,
                                                            assigned_to=latest_oio.assigned_to,
                                                            operation_changed_from=operation_changed_from,linkedin=linkedin)

                elif count > 0:
                    oio = OrderItemOperation.objects.create(order_item_id=int(item_object.order_item.id),
                                                            resume=resume,
                                                            operation_type=6,
                                                            assigned_by=user,
                                                            assigned_to=order_assinged_by[count-1].assigned_by,
                                                            operation_changed_from=operation_changed_from,linkedin=linkedin)

            else:
                latest_oio = OrderItemOperation.objects.filter(order_item=item_object.order_item, operation_type=8).latest('added_on')
                oio = OrderItemOperation.objects.create(order_item_id=int(item_object.order_item.id),
                                                        resume=resume,
                                                        operation_type=6,
                                                        assigned_by=user,
                                                        assigned_to=latest_oio.assigned_by,
                                                        operation_changed_from=operation_changed_from,linkedin=linkedin)

            for itms in oio.order_item.order.orderitem_set.all():
                if itms.name in delivery_types_4_sms:
                    try:
                        sms_for_delivery_type(
                            itms.oio_assigned_to,
                            itms.order.id,
                            itms.name,
                            'candidate')
                    except:
                        pass
            if comment:
                Message.objects.create(from_user=oio.order_item.order.candidate, message=comment, oio=oio)
            messages.add_message(request, messages.SUCCESS, 'You Rejected the document.')
            return HttpResponseRedirect(reverse_lazy('user_dashboard'))

        elif action == 4 and item_object:
            item_object.operation_changed_from = 4
            item_object.save()
            oio = OrderItemOperation.objects.create(order_item_id=int(item_object.order_item.id), resume=item_object.resume, operation_type=4, assigned_by=item_object.assigned_by, assigned_to=item_object.assigned_to,linkedin=linkedin)
            if comment:
                Message.objects.create(from_user=oio.order_item.order.candidate, message=comment, oio=oio)

            try:
                if item_object.order_item.parent and item_object.order_item.parent.product.is_international:
                    for_international = item_object.order_item.parent.orderitem_set.filter(parent__isnull=False, addon__is_allocable=True, addon__is_service=False)
                    no_of_objs = for_international.count()
                    if no_of_objs > 0:
                        for items in for_international:
                            if int(items.oio_operation_type) == 4:
                                no_of_closed_objs += 1
                        if no_of_closed_objs == no_of_objs:
                            OrderItemOperation.objects.create(order_item=item_object.order_item.parent, resume=item_object.resume, operation_type=4)

            except:
                pass
            messages.add_message(request, messages.SUCCESS, 'Thank you for accepting.')
            email = ''
            draft = 3

            try:
                candidate = item_object.order_item.order.candidate
                email = candidate.email
                title = candidate.first_name if candidate.first_name else 'Candidate'
                token = Token().encode(str(email), 10, 30)
                mail_data = {'draft': draft, 'order_item': item_object.order_item, 'token': token, 'title': title}
                mail_data.update(CampaignUrl().google(data={'x_mailertag': 'Resume_Accepted', 'email': email}))
                SendMail().send(to=[email], mail_type=MAIL_TYPE.get(13, "DRAFT_UPLOAD"), data=mail_data)
            except Exception as e:
                error_msg = 'ACCEPT_DRAFT MAIL: Can not send accept draft mail for OrderItem: %s' % str(item_object.order_item.pk)
                logging.getLogger('error_log').error("%s ERROR: %s" % (error_msg, str(e)))

            try:
                od = item_object.order_item.order
                if not email:
                    email = od.candidate.email
                mobile = od.order_mobile if od.order_mobile else od.candidate.userprofile.mobile
                mobile_data = {'mobile': mobile, 'email': email}
                SendSMS().send(sms_type=SMS_TYPE.get(11, "CLOSER"), data=mobile_data)
            except Exception as e:
                error_msg = 'ACCEPT_DRAFT SMS: Can not send draft upload SMS for OrderItem: %s' % str(item_object.order_item.pk)
                logging.getLogger('error_log').error("%s ERROR: %s" % (error_msg, str(e)))
            return HttpResponseRedirect(reverse_lazy('user_dashboard'))
        else:
            messages.add_message(request, messages.ERROR, 'Required information is missing')
            return HttpResponseRedirect(reverse_lazy('user_dashboard'))
    
    def make_copy_draft(self,draft=None):
        if draft:
            draft_copy = deepcopy(draft)
            draft_copy.id = None
            draft_copy.save()

            for keyskill in draft.keyskill_set.all():
                keyskill_copy = deepcopy(keyskill)
                keyskill_copy.id = None
                keyskill_copy.draft = draft_copy
                keyskill_copy.save()
            for organization in draft.organization_set.all():
                organization_copy = deepcopy(organization)
                organization_copy.id = None
                organization_copy.draft = draft_copy
                organization_copy.save()
            for education in draft.education_set.all():
                education_copy = deepcopy(education)
                education_copy.id = None
                education_copy.draft = draft_copy
                education_copy.save()    
            draft_copy.save()
        return draft_copy

class DashboardResumeUploadView(AjaxPostResponseRedirectView):

    http_method_names = ['post', ]
    model = Message
    url = reverse_lazy('user_dashboard')

    def post_response(self, request):
        order_id = request.POST.get('order_id')
        if order_id:
            order = Order.objects.get(pk=order_id)
        else:
            order = Order.objects.get(pk=request.session.get('order_id'))

        if order:
            upload_full_path = '/%s/%s_%s' % (fetchDir(str(order.candidate.pk)), str(order.candidate.pk), str(order.pk))
            f_obj = request.FILES['resume_uploader']
            file_name_tuple = os.path.splitext(f_obj.name)
            extention = file_name_tuple[len(file_name_tuple)-1] if len(file_name_tuple)>1 else ''
            file_name=str(order.candidate.pk)+'_'+str(order.pk)+'_'+str(int(random()*9999))+extention

            if not os.path.exists(settings.UPLOADS_DIR_RESUME+upload_full_path):
                os.makedirs(settings.UPLOADS_DIR_RESUME+upload_full_path)
            dest = open(settings.UPLOADS_DIR_RESUME + upload_full_path +'/' + file_name, 'wb')

            for chunk in f_obj.chunks():
                dest.write(chunk)
            dest.close()

            for oi in order.orderitem_set.exclude(variation__type_of_product__in=[2, 3, 6]).exclude(product__flags__true='exclude_midout').exclude(addon__flags__true='interview'):
                OrderItemAllocation().allocate(request=request, order_item=oi, resume=upload_full_path+'/'+file_name)
                oi.oio_resume=upload_full_path+'/'+file_name
                oi.save()
                if oi.name=="Super Express Delivery":
                    superexpress_sms(order_id)
            delete_session_keys(request, ['int_child_count','int_child','quantity_calculate_discount', 'is_combo', 'combo_price'])
            messages.add_message(self.request, messages.SUCCESS, "Resume uploaded successfully.")
            return True
        else:
            messages.add_message(self.request, messages.ERROR, "Resume couldn't be uploaded.")
            return True



class DashboardInvoice(View):
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id', '')
        
        if self.request.user.is_anonymous():
            return HttpResponseForbidden()
        if not self.request.user:
            return HttpResponseForbidden()
        if not self.request.user.order_set.filter(status__in=[2, 5],pk=order_id):
            return HttpResponseForbidden()

        data_dict = {}
        try:
            order = Order.objects.get(id=order_id)
            if order.orderitem_set.filter(variation__type_of_product=3).count() > 0:
                data_dict['is_tssc'] = True
                data_dict['template'] = 'mailers/candidate/tssc_invoice.html'
            else:
                data_dict['template'] = 'careerplus/invoice.html'
            data_dict['order'] = order
            invoice = Invoice().generate(data_dict)
            # return invoice
            response = HttpResponse(invoice)
            response['Content-Type'] = 'application/pdf'
            response['Content-Disposition'] = 'filename="Shine Career Plus Invoice.pdf"'
            return response
        except Exception as e:
            logging.getLogger('error_log').error("Invoice Not Generated for order #%s - %s " % (order_id, str(e)))
        return HttpResponseRedirect(reverse('user_dashboard'))


class DashboardMyProfileView(CommonContext, ShineCandidateDetail,ResumeBuilderContext, TemplateView):
    template_name = "dashboard/myprofile.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardMyProfileView, self).get_context_data(
            **kwargs)
        context.update(self.get_common_context_data())
        try:
            request = self.request
            shine_profile = request.session.get('candidate_profile', '')
            if not shine_profile:
                email = request.user.email
                shine_profile = self.get_candidate_detail(email=email)
                request.session.update({'candidate_profile': shine_profile})
            personal_detail = self.get_personal_detail(request)
            education_detail = self.get_edu_history(request)
            experience_detail = self.get_job_history(request)
            skill_detail = self.get_skills(request)
            latest_job = self.get_latest_job(request)
            context.update({
                "personal_detail": personal_detail,
                "education_detail": education_detail,
                "experience_detail": experience_detail,
                "latest_job": latest_job,
                "skill_detail": skill_detail
            })
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        context.update({"myprofile_active": True})
        return context


class DashboardRoundoneView(CommonContext, HasRoundOneOrderMixin, TemplateView):
    template_name = "dashboard/roundone.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardRoundoneView, self).get_context_data(**kwargs)
        context.update(self.get_common_context_data())
        context.update({'round_active': True})
        show_msg = self.request.GET.get('msg', '')
        if show_msg:
            messages.add_message(
                self.request,
                messages.INFO,
                'Complete the following details to initiate the service')
            context.update({'messages': messages})
        return context


class DashboardRoundoneProfileView(RoundOneAPI, View):

    def get_context_data(self, **kwargs):
        context = super(
            DashboardRoundoneProfileView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            profile_reload = request.GET.get('profile_reload', '')
            roundone_profile = request.session.get("roundone_profile")
            if profile_reload or not roundone_profile:
                roundone_profile = self.get_roundone_profile(request)
            template_html = render_to_string(
                    "dashboard/default_roundone.html")
            if roundone_profile.get("response"):
                request.session.update({"roundone_profile": roundone_profile})
                job_params_list = request.session.get("roundone_job_params", "").split("-")
                jobId = ""
                if job_params_list:
                    jobId = job_params_list[0]
                    job_params = '-'.join(job_params_list)
                rouser = roundone_profile.get("user")
                education = {}
                employments = {}
                latest_job = {}
                skill_list = []
                if rouser:
                    education = rouser.get("education")
                    employments = rouser.get("employments")
                    for job in employments:
                        if job.get("curent") == 1:
                            latest_job = job
                    skill_str = rouser.get("skills", "")
                    skill_list = skill_str.split(",")
                csrf_token_value = get_token(request)
                today_date =  datetime.now().date().strftime("%Y-%m-%d")
                context = {
                    "STATIC_URL": settings.STATIC_URL,
                    "rouser": rouser,
                    "education_list": education,
                    "employment_list": employments,
                    "latest_job": latest_job,
                    "skill_str": skill_str,
                    "skill_list": skill_list,
                    "csrf_token_value": csrf_token_value,
                    "jobId": jobId,
                    "job_params": job_params,
                    "today_date": today_date,
                    "resume_upload_url": settings.ROUNDONE_API_DICT.get("submit_resume"),
                    "access_token": roundone_profile.get("access_token")
                }
                template_html = render_to_string(
                    "dashboard/roundone_profile.html", context)
            return HttpResponse(json.dumps(
                {'status': True, 'response': roundone_profile.get("response"), 'template': template_html}))
        else:
            return HttpResponseRedirect(reverse_lazy('user_dashboard'))

        return HttpResponse(json.dumps({'status': False, 'response': False}))


class RoundonePersonalSubmit(RoundOneAPI, View):

    def post(self, request, *args, **kwargs):
        try:
            name = request.POST.get("name")
            contact = request.POST.get("contact")
            total_exp = request.POST.get("total_exp")
            roundone_profile = request.session.get("roundone_profile")
            if not roundone_profile:
                roundone_profile = self.get_roundone_profile(request)
            if roundone_profile.get("response"):
                rouser = roundone_profile.get("user")
                rouser.update({
                    "name": name,
                    "mobile": contact,
                    "total_exp": total_exp
                })
                response_json = self.post_roundone_profile(
                    request, roundone_profile)
                if response_json.get("response"):
                    request.session.update({
                        "roundone_profile": roundone_profile})
                    return HttpResponse(json.dumps({
                        "status": True,
                        "message": response_json.get("msg")}))
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return HttpResponse(json.dumps({
            "status": False, "message": "Profile Not Updated"}))
     

class RoundoneAddEducation(RoundOneAPI, View):

    def post(self, request, *args, **kwargs):
        try:
            institute = request.POST.get("institute")
            degree = request.POST.get("degree")
            major = request.POST.get("major")
            year = request.POST.get("year")
            marks = request.POST.get("marks")
            if institute and degree and major and year and marks:
                roundone_profile = request.session.get("roundone_profile")
                if not roundone_profile:
                    roundone_profile = self.get_roundone_profile(request)
                if roundone_profile.get("response"):
                    rouser = roundone_profile.get("user")
                    user_education = rouser.get("education", [])
                    add_education = {
                        "institute": institute,
                        "degree": degree,
                        "major": major,
                        "year": year,
                        "marks": marks
                    }
                    user_education.append(add_education)
                    rouser.update({
                        "education": user_education
                    })
                    response_json = self.post_roundone_profile(
                        request, roundone_profile)
                    if response_json.get("response"):
                        request.session.update({
                            "roundone_profile": roundone_profile})
                        return HttpResponse(json.dumps({
                            "status": True,
                            "message": response_json.get("msg")}))
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return HttpResponse(json.dumps({
            "status": False, "message": "Profile Not Updated"}))


class RoundoneEditEducation(RoundOneAPI, View):
    def post(self, request, *args, **kwargs):
        try:
            idx = kwargs.get("idx")
            institute = request.POST.get("institute" + idx)
            degree = request.POST.get("degree" + idx)
            major = request.POST.get("major" + idx)
            year = request.POST.get("year" + idx)
            marks = request.POST.get("marks" + idx)
            if institute and degree and major and year and marks:
                roundone_profile = request.session.get("roundone_profile")
                if not roundone_profile:
                    roundone_profile = self.get_roundone_profile(request)
                if roundone_profile.get("response"):
                    rouser = roundone_profile.get("user")
                    user_education = rouser.get("education", [])
                    add_education = {
                        "institute": institute,
                        "degree": degree,
                        "major": major,
                        "year": year,
                        "marks": marks,
                    }
                    try:
                        user_education[int(idx)] = add_education
                    except:
                        user_education.append(add_education)
                    rouser.update({
                        "education": user_education
                    })
                    response_json = self.post_roundone_profile(
                        request, roundone_profile)
                    if response_json.get("response"):
                        request.session.update({
                            "roundone_profile": roundone_profile})
                        return HttpResponse(json.dumps({
                            "status": True,
                            "message": response_json.get("msg")}))
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return HttpResponse(json.dumps({
            "status": False, "message": "Profile Not Updated"}))


class RoundoneAddWorkEx(RoundOneAPI, View):

    def post(self, request, *args, **kwargs):
        try:
            company = request.POST.get("company")
            position = request.POST.get("position")
            from_date = request.POST.get("from")
            to_date = request.POST.get("to")
            current = request.POST.get("current")
            if current:
                to_date = ""
                current = 1
            if company and position and from_date:
                roundone_profile = request.session.get("roundone_profile")
                if not roundone_profile:
                    roundone_profile = self.get_roundone_profile(request)
                if roundone_profile.get("response"):
                    rouser = roundone_profile.get("user")
                    user_workex = rouser.get("employments", [])
                    add_workex = {
                        "company": company,
                        "position": position,
                        "from": from_date,
                        "to": to_date,
                        "curent": current
                    }
                    user_workex.append(add_workex)
                    rouser.update({
                        "employments": user_workex
                    })
                    response_json = self.post_roundone_profile(
                        request, roundone_profile)
                    if response_json.get("response"):
                        request.session.update({
                            "roundone_profile": roundone_profile})
                        return HttpResponse(json.dumps({
                            "status": True,
                            "message": response_json.get("msg")}))
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return HttpResponse(json.dumps({
            "status": False, "message": "Profile Not Updated"}))


class RoundoneEditWorkex(RoundOneAPI, View):
    def post(self, request, *args, **kwargs):
        try:
            idx = kwargs.get("idx")
            company = request.POST.get("company" + idx)
            position = request.POST.get("position" + idx)
            from_date = request.POST.get("from" + idx)
            to_date = request.POST.get("to" + idx)
            current = request.POST.get("current" + idx)
            if current:
                to_date = ""
                current = 1
            if company and position and from_date:
                roundone_profile = request.session.get("roundone_profile")
                if not roundone_profile:
                    roundone_profile = self.get_roundone_profile(request)
                if roundone_profile.get("response"):
                    rouser = roundone_profile.get("user")
                    user_workex = rouser.get("employments", [])
                    add_workex = {
                        "company": company,
                        "position": position,
                        "from": from_date,
                        "to": to_date,
                        "curent": current
                    }
                    try:
                        user_workex[int(idx)] = add_workex
                    except:
                        user_workex.append(add_workex)
                    rouser.update({
                        "employments": user_workex
                    })
                    response_json = self.post_roundone_profile(
                        request, roundone_profile)
                    if response_json.get("response"):
                        request.session.update({
                            "roundone_profile": roundone_profile})
                        return HttpResponse(json.dumps({
                            "status": True,
                            "message": response_json.get("msg")}))
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return HttpResponse(json.dumps({
            "status": False, "message": "Profile Not Updated"}))


class RoundoneAddSkill(RoundOneAPI, View):

    def post(self, request, *args, **kwargs):
        try:
            skill = request.POST.get("skill")
            if skill:
                roundone_profile = request.session.get("roundone_profile")
                if not roundone_profile:
                    roundone_profile = self.get_roundone_profile(request)
                if roundone_profile.get("response"):
                    rouser = roundone_profile.get("user")
                    user_skill = rouser.get("skills", "")
                    skill_list = user_skill + "," + skill
                    rouser.update({
                        "skills": skill_list
                    })
                    response_json = self.post_roundone_profile(
                        request, roundone_profile)
                    if response_json.get("response"):
                        request.session.update({
                            "roundone_profile": roundone_profile})
                        return HttpResponse(json.dumps({
                            "status": True, "message": response_json.get("msg")}))
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return HttpResponse(json.dumps({
            "status": False, "message": "Profile Not Updated"}))


class RoundoneEditSkill(RoundOneAPI, View):

    def post(self, request, *args, **kwargs):
        try:
            skill = request.POST.get("skill_str")
            if skill:
                roundone_profile = request.session.get("roundone_profile")
                if not roundone_profile:
                    roundone_profile = self.get_roundone_profile(request)
                if roundone_profile.get("response"):
                    rouser = roundone_profile.get("user")
                    rouser.update({
                        "skills": skill
                    })
                    response_json = self.post_roundone_profile(
                        request, roundone_profile)
                    if response_json.get("response"):
                        request.session.update({
                            "roundone_profile": roundone_profile})
                        return HttpResponse(json.dumps({
                            "status": True, "message": response_json.get("msg")}))
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return HttpResponse(json.dumps({
            "status": False, "message": "Profile Not Updated"}))


class DashboardReferralView(RoundOneAPI, View):

    def get(self, request, *args, **kwargs):
        pending = []
        accepted = []
        if request.is_ajax():
            referral_status = self.get_referral_status(request)
            if referral_status:
                if referral_status.get("status") == "1":
                    for data in referral_status.get('data'):
                        try:
                            status = data.get("status", "")
                            status_str = ROUNDONE_REFERRAL_STATUS.get(str(status))
                            data.update({"status": status_str})

                            data.update(
                                {"requestedDate": datetime.utcfromtimestamp(
                                    int(data.get(
                                        'requestedDate', 0))
                                    ).strftime("%d %b, %Y")})

                            data.update(
                                {"expiryDate": datetime.utcfromtimestamp(
                                    int(data.get(
                                        'expiryDate', 0))
                                    ).strftime("%d %b, %Y")})

                            if data.get("acceptedDate") and str(status) == "1":
                                data.update(
                                    {"acceptedDate": datetime.utcfromtimestamp(
                                        int(data.get('acceptedDate', 0))
                                        ).strftime("%d %b, %Y")})
                                accepted.append(data)
                            else:
                                pending.append(data)
                        except:
                            pass

                context = {
                    "STATIC_URL": settings.STATIC_URL,
                    'pending': pending,
                    'accepted': accepted}
                template_html = render_to_string(
                    "dashboard/roundone_referral.html", context)
                return HttpResponse(
                    json.dumps({'status': True, 'response': referral_status.get('response'), 'template': template_html}))
        else:
            return HttpResponseRedirect(reverse_lazy('user_dashboard'))
        return HttpResponse(json.dumps({'status': False, 'response': False}))


class DashboardReferralConfirmView(RoundOneAPI, View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            response_json = self.get_referral_confirm(request)
            if response_json.get("status") == "1":
                return HttpResponse(json.dumps(
                    {'status': True, 'message': response_json.get('msg')}))
            return HttpResponse(json.dumps(
                {'status': False, 'message': response_json.get('msg')}))
        else:
            return HttpResponseRedirect(reverse_lazy('user_dashboard'))
        return HttpResponse(json.dumps({'status': False}))


class DashboardUpcomingView(RoundOneAPI, View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            upcoming_interaction = self.get_upcoming_status(request)
            upcoming_data = upcoming_interaction.get("data")
            if upcoming_data:
                for data in upcoming_data:
                    time_str = data.get("interactionScheduledTime", "")
                    if time_str:
                        try:
                            strpdt = datetime.strptime(
                                time_str, "%Y-%m-%d %H:%M:%S").strftime(
                                "%d %b, %Y at %H:%M")
                            data.update({
                                "interactionScheduledTime": strpdt
                                })
                        except:
                            pass
            context = {"STATIC_URL": settings.STATIC_URL, 'upcoming_interaction': upcoming_interaction}
            template_html = render_to_string("dashboard/roundone_upcoming.html", context)
            return HttpResponse(json.dumps({'status': True, 'response': upcoming_interaction.get('response'), 'template': template_html}))
        else:
            return HttpResponseRedirect(reverse_lazy('user_dashboard'))
        return HttpResponse(json.dumps({'status': False, 'response': False}))


class DashboardPastView(RoundOneAPI, View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            past_interaction = self.get_past_interaction(request)

            if past_interaction:

                if past_interaction.get("status") == "1":

                    for data in past_interaction.get('data'):
                        try:
                            status = data.get("status", "")
                            status_str = ROUNDONE_PAST_STATUS.get(str(status))
                            action = ROUNDONE_PAST_ACTION.get(str(status), '')
                            data.update({"status_str": status_str})
                            data.update({"action": action})
                        except:
                            pass
            context = {
                "STATIC_URL": settings.STATIC_URL,
                "past_interaction": past_interaction}

            template_html = render_to_string(
                "dashboard/roundone_past.html", context)
            return HttpResponse(json.dumps({
                'status': True, 'response': past_interaction.get('response'), 'template': template_html}))
        else:
            return HttpResponseRedirect(reverse_lazy('user_dashboard'))
        return HttpResponse(json.dumps({'status': False, 'response': False}))


class DashboardResultView(RoundOneAPI, TemplateView):
    template_name = "dashboard/roundone_result_feedback.html"

    def get_context_data(self, **kwargs):
        show_feedback = True
        context = super(DashboardResultView, self).get_context_data(**kwargs)
        past_interaction = str(self.request.GET.get('status', ''))

        if past_interaction == '1' or past_interaction == '0':
            show_feedback = False
            context.update({'show_feedback': show_feedback})
        else:

            context.update({'show_feedback': show_feedback})

        try:
            data_dict = {
                'userEmail': self.request.user.email,
                'orderId': kwargs.get("order_id"),
            }

            result_html = self.get_result_template(
                self.request, data_dict, show_feedback)
            context.update({'result_html': result_html})
        except:
            pass
        context.update(kwargs)
        return context

    def post(self, request, *args, **kwargs):
        interviewerRating = request.POST.get('interviewerRating')
        roundoneRating = request.POST.get('roundoneRating')
        comments = request.POST.get('comments')
        orderId = kwargs.get('order_id')

        userEmail = request.user.email

        data_dict = {
            'userEmail': userEmail,
            'interviewerRating': interviewerRating,
            'roundoneRating': roundoneRating,
            'comments': comments,
            'orderId': orderId
        }

        response_json = self.feedback_submit(request, data_dict)

        if response_json.get("status") == "1":
            template_html = self.get_result_template(request, data_dict, False)
            return HttpResponse(json.dumps({
                'status': True, 'template': template_html}))

        return HttpResponse(json.dumps({
            'status': False, 'message': response_json.get('msg')}))

    def get_result_template(self, request, data_dict, show_feedback):
        result_json = self.interaction_result(request, data_dict)

        if result_json.get("status") == "1":
            try:
                data = result_json.get("data", {})

                feedback = data.get("referrerFeedback", {})

                commSkills = feedback.get("commSkills")
                subjectKnowledge = feedback.get("subjectKnowledge")
                culturalFit = feedback.get("culturalFit")
                status = data.get("status", '')

                commSkills_str = ROUNDONE_INTERACTION_RESULT.get(
                    str(commSkills))
                subjectKnowledge_str = ROUNDONE_INTERACTION_RESULT.get(
                    str(subjectKnowledge))
                culturalFit_str = ROUNDONE_INTERACTION_RESULT.get(
                    str(culturalFit))
                # status_str = ROUNDONE_FINAL_RESULT.get(str(status))

                feedback.update({
                    "commSkills": commSkills_str,
                    "subjectKnowledge": subjectKnowledge_str,
                    "culturalFit": culturalFit_str
                })
            except:
                pass

        context = {
            "STATIC_URL": settings.STATIC_URL,
            'result': result_json,
            'show_feedback': show_feedback,
            "status": status}

        template_html = render_to_string(
            "dashboard/roundone_result.html", context)
        return template_html


class DashboardSavedView(RoundOneAPI, View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            csrf_token_value = get_token(request)
            saved_history = self.get_saved_history(request)
            context = {"STATIC_URL": settings.STATIC_URL, 'saved_history': saved_history, 'partner': 'roundone', "csrf_token_value": csrf_token_value}
            template_html = render_to_string("dashboard/roundone_saved.html", context)
            return HttpResponse(json.dumps({'status': True, 'response': saved_history.get('response'), 'template': template_html}))
        else:
            return HttpResponseRedirect(reverse_lazy('user_dashboard'))
        return HttpResponse(json.dumps({'status': False, 'response': False}))


class DashboardSavedDeleteView(RoundOneAPI, View):

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            job_params = request.POST.get('job_params').split('-')
            response_json = self.delete_saved_job(request, job_params)
            if response_json.get("status") and response_json.get("status") == "1":
                return HttpResponse(json.dumps({'status': True}))
            return HttpResponse(json.dumps({'status': False, "message": "Error Deleting This Job"}))
        else:
            return HttpResponseRedirect(reverse_lazy('user_dashboard'))
        return HttpResponse(json.dumps({'status': False}))
