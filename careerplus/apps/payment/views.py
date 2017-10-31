import logging
import time
import os
import mimetypes
from random import random


from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.urls import reverse
from django.shortcuts import render
from django.conf import settings
from cart.models import Cart
from order.mixins import OrderMixin
from order.models import Order
from console.decorators import Decorate, stop_browser_cache
from dashboard.dashboard_mixin import DashboardInfo
from django.core.files.base import ContentFile
from django.utils import timezone

from core.api_mixin import ShineCandidateDetail
from .models import PaymentTxn

from .forms import StateForm, PayByCheckForm
from .mixin import PaymentMixin


@Decorate(stop_browser_cache())
class PaymentOptionView(TemplateView, OrderMixin, PaymentMixin):
    template_name = "payment/payment-option.html"

    def __init__(self):
        self.cart_obj = None

    def redirect_if_necessary(self):
        if not self.request.session.get('cart_pk'):
            self.cart_obj = self.getCartObject()
        else:
            cart_pk = self.request.session.get('cart_pk')
            if not cart_pk:
                return HttpResponsePermanentRedirect(reverse('homepage'))
            try:
                self.cart_obj = Cart.objects.get(pk=cart_pk)
                cart_dict = self.get_solr_cart_items(cart_obj=self.cart_obj)
                if not cart_dict.get('total_amount'):
                    return HttpResponsePermanentRedirect(reverse('homepage'))
                elif not self.cart_obj.shipping_done or not self.cart_obj.owner_id:
                    return HttpResponsePermanentRedirect(reverse('cart:payment-shipping'))
            except:
                return HttpResponsePermanentRedirect(reverse('homepage'))
        if self.cart_obj and not (self.cart_obj.shipping_done):
            return HttpResponsePermanentRedirect(reverse('cart:payment-login'))

        elif not self.cart_obj:
            return HttpResponsePermanentRedirect(reverse('homepage'))
        elif self.cart_obj and not self.cart_obj.lineitems.filter(no_process=False).exists():
            return HttpResponsePermanentRedirect(reverse('homepage'))
        return None

    def get(self, request, *args, **kwargs):
        redirect = self.redirect_if_necessary()
        if redirect:
            return redirect
        return super(PaymentOptionView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        payment_type = request.POST.get('payment_type', '').strip()
        if payment_type == 'cash':
            form = StateForm(request.POST)
            if form.is_valid():
                cart_pk = request.session.get('cart_pk')
                if cart_pk:
                    cart_obj = Cart.objects.get(pk=cart_pk)
                    order = self.createOrder(cart_obj)
                    self.closeCartObject(cart_obj)
                    if order:
                        txn = 'CP%d%s' % (order.pk, int(time.time()))
                        pay_txn = PaymentTxn.objects.create(
                            txn=txn,
                            order=order,
                            cart=cart_obj,
                            status=0,
                            payment_mode=1,
                            currency=order.currency,
                            txn_amount=order.total_incl_tax,
                        )
                        payment_type = "CASH"
                        return_parameter = self.process_payment_method(
                            payment_type, request, pay_txn)
                        try:
                            del request.session['cart_pk']
                            del request.session['checkout_type']
                            request.session.modified = True
                        except:
                            pass
                        return HttpResponseRedirect(return_parameter)
                else:
                    return HttpResponseRedirect(reverse('homepage'))
            else:
                context = self.get_context_data()
                context['state_form'] = form
                return render(request, self.template_name, context)
        elif payment_type == 'cheque':
            form = PayByCheckForm(request.POST)
            if form.is_valid():
                cart_pk = request.session.get('cart_pk')
                if cart_pk:
                    cart_obj = Cart.objects.get(pk=cart_pk)
                    order = self.createOrder(cart_obj)
                    self.closeCartObject(cart_obj)
                    if order:
                        txn = 'CP%d%s%s' % (
                            order.pk,
                            int(time.time()),
                            request.POST.get('cheque_no'))
                        pay_txn = PaymentTxn.objects.create(
                            txn=txn,
                            order=order,
                            cart=cart_obj,
                            status=0,
                            payment_mode=4,
                            currency=order.currency,
                            txn_amount=order.total_incl_tax,
                            instrument_number=request.POST.get('cheque_no'),
                            instrument_issuer=request.POST.get('drawn_bank'),
                            instrument_issue_date=request.POST.get('deposit_date')
                        )
                        payment_type = "CHEQUE"
                        return_parameter = self.process_payment_method(
                            payment_type, request, pay_txn)
                        try:
                            del request.session['cart_pk']
                            del request.session['checkout_type']
                            request.session.modified = True
                        except:
                            pass
                        return HttpResponseRedirect(return_parameter)
                else:
                    return HttpResponseRedirect(reverse('homepage'))
            else:
                context = self.get_context_data()
                context['check_form'] = form
                return render(request, self.template_name, context)

        return HttpResponseRedirect(reverse('cart:cart-product-list'))

    def get_context_data(self, **kwargs):
        context = super(PaymentOptionView, self).get_context_data(**kwargs)
        payment_dict = self.getPayableAmount(cart_obj=self.cart_obj)
        context.update({
            "state_form": StateForm(),
            "check_form": PayByCheckForm(),
            "total_amount": payment_dict.get('total_payable_amount'),
            "cart_id": self.request.session.get('cart_pk'),
        })
        return context


@Decorate(stop_browser_cache())
class ThankYouView(TemplateView):
    template_name = "payment/thank-you.html"

    def get(self, request, *args, **kwargs):
        if self.request.session.get('order_pk'):
            return super(ThankYouView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('homepage'))

    def get_context_data(self, **kwargs):
        context = super(ThankYouView, self).get_context_data(**kwargs)
        order_pk = self.request.session.get('order_pk')
        if order_pk:
            order = Order.objects.get(pk=order_pk)
            order_items = []
            if order:
                parent_ois = order.orderitems.filter(parent=None).select_related('product', 'partner')
                for p_oi in parent_ois:
                    data = {}
                    data['oi'] = p_oi
                    data['addons'] = order.orderitems.filter(
                        parent=p_oi,
                        is_addon=True).select_related('product', 'partner')
                    data['variations'] = order.orderitems.filter(
                        parent=p_oi,
                        is_variation=True).select_related('product', 'partner')
                    order_items.append(data)
                context.update({
                    'orderitems': order_items,
                    'order': order})

                pending_resume_items = order.orderitems.filter(
                    order__status__in=[0, 1],
                    no_process=False, oi_status=2)
                context.update({
                    "pending_resume_items": pending_resume_items,
                })

                if not self.request.session.get('resume_id', None):
                    DashboardInfo().check_user_shine_resume(
                        candidate_id=self.request.session.get('candidate_id'),
                        request=self.request)
        return context

    def post(self, request, *args, **kwargs):
        action_type = request.POST.get('action_type', '').strip()
        order_pk = request.session.get('order_pk')
        resume_id = request.session.get('resume_id', None)
        candidate_id = request.session.get('candidate_id', None)
        try:
            order = Order.objects.get(pk=order_pk)
        except:
            return HttpResponseRedirect(reverse('payment:thank-you'))
        file = request.FILES.get('resume_file', '')
                
        if action_type == 'upload_resume' and order_pk and file:
            try:
                filename = os.path.splitext(file.name)
                extention = filename[len(filename)-1] if len(
                    filename) > 1 else ''
                file_name = 'resumeupload_' + str(order.pk) + '_' + str(int(random()*9999)) \
                    + '_' + timezone.now().strftime('%Y%m%d') + extention
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
                return HttpResponseRedirect(reverse('payment:thank-you'))
            
            order = Order.objects.get(pk=order_pk)
            pending_resumes = order.orderitems.filter(order__status__in=[0, 1], no_process=False, oi_status=2)
            
            for obj in pending_resumes:
                
                obj.oi_resume = full_path + file_name
                last_oi_status = obj.oi_status
                obj.oi_status = 5
                obj.last_oi_status = 3
                obj.save()
                obj.orderitemoperation_set.create(
                    oi_status=3,
                    oi_resume=obj.oi_resume,
                    last_oi_status=last_oi_status,
                    assigned_to=obj.assigned_to)

                obj.orderitemoperation_set.create(
                    oi_status=obj.oi_status,
                    last_oi_status=obj.last_oi_status,
                    assigned_to=obj.assigned_to)

        elif action_type == "shine_reusme" and order_pk and candidate_id and resume_id:
            order = Order.objects.get(pk=order_pk)
            pending_resumes = order.orderitems.filter(
                order__status__in=[0, 1],
                no_process=False, oi_status=2)
            response = ShineCandidateDetail().get_shine_candidate_resume(
                candidate_id=candidate_id,
                resume_id=request.session.get('resume_id'))
            if response.status_code == 200:
                default_name = 'shine_resume' + timezone.now().strftime('%d%m%Y')
                file_name = request.session.get('shine_resume_name', default_name)
                resume_extn = request.session.get('resume_extn', '')
                try:
                    file = ContentFile(response.content)
                    file_name = 'resumeupload_' + str(order.pk) + '_' + str(obj.pk) + '_' + str(int(random()*9999)) \
                        + '_' + timezone.now().strftime('%Y%m%d') + '.' + resume_extn
                    full_path = '%s/' % str(order.pk)
                    if not os.path.exists(settings.RESUME_DIR + full_path):
                        os.makedirs(settings.RESUME_DIR + full_path)
                    dest = open(
                        settings.RESUME_DIR + full_path + file_name, 'wb')
                    for chunk in file.chunks():
                        dest.write(chunk)
                    dest.close()
                except Exception as e:
                    logging.getLogger('error_log').error("%s-%s" % ('resume_upload', str(e))) 
                    return HttpResponseRedirect(reverse('payment:thank-you'))
                
                for obj in pending_resumes:
                    
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

        return HttpResponseRedirect(reverse('payment:thank-you'))


@Decorate(stop_browser_cache())
class PaymentOopsView(TemplateView):
    template_name = 'payment/payment-oops.html'

    def get(self, request, *args, **kwargs):
        return super(PaymentOopsView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        error_type = self.request.GET.get('error', '')
        txn_id = self.request.GET.get('txn_id', '')
        context = super(PaymentOopsView, self).get_context_data(**kwargs)
        context.update({'error_type': error_type, 'txn_id': txn_id})
        context.update({'is_payment': True, })
        return context
