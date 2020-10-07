from django.views.generic import View, TemplateView, FormView

from wallet.models import (
    Wallet, RewardPoint, ECash,
    WalletTransaction, ECashTransaction, PointTransaction)
from .wallet_form import Walletform
from order.models import Order
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponseForbidden
import logging
import datetime
from decimal import Decimal
from django.utils import timezone
from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required





@method_decorator(permission_required('wallet.console_add_remove_wallet_point', login_url='/console/login/'),  name='dispatch')
class WalletView(FormView):
    template_name = 'console/wallet/walletrew.html'
    form_class = Walletform
    http_method_names = [u'get', u'post']
    model = Wallet
    success_url = "/console/wallet/"

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({
            'messages': alert})
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            email = form.cleaned_data['email_id']
            owner = form.cleaned_data['owner_id']
            note = form.cleaned_data['notes']
            points = form.cleaned_data['point_value']
            action = form.cleaned_data['wallet_action']
            order = form.cleaned_data.get('order', None)
            wal_obj = ""

            if owner:
                try:
                    wal_obj = Wallet.objects.get(owner=owner)
                    if wal_obj:
                        pass
                except Exception as e:
                    logging.getLogger('error_log').error(str(e))
                    pass

            if email and not wal_obj:
                wal_obj = Wallet.objects.filter(owner_email=email).count()
                if wal_obj != 1:
                    wal_obj = None
                elif wal_obj == 1:
                    wal_obj = Wallet.objects.filter(owner_email=email)[0]
            if order:
                if email:
                    orders = Order.objects.filter(email=email, number=order)
                elif owner:
                    orders = Order.objects.filter(candidate_id=owner, number=order)
                if not orders.exists():
                    messages.add_message(
                        request, messages.ERROR,
                        'Unable TO Find Order')
                    return self.form_invalid(form)
                order = orders[0]

            if wal_obj:
                expiry = timezone.now() + datetime.timedelta(days=30)
                if action == 'addpoints':

                    point_obj = wal_obj.point.create(
                        original=points,
                        current=points,
                        expiry=expiry,
                        status=1
                    )

                    wal_txn = wal_obj.wallettxn.create(
                        txn_type=1,
                        status=1,
                        point_value=points,
                        added_by=request.user.id,
                        notes=note
                    )
                    if order:
                        wal_txn.order = order
                        wal_txn.save()

                    point_obj.wallettxn.create(
                        transaction=wal_txn,
                        point_value=points,
                        txn_type=1
                    )

                    wal_txn.current_value = wal_obj.get_current_amount()
                    wal_txn.save()
                    messages.add_message(request, messages.SUCCESS,
                                         'Successfull.')

                else:
                    rew_points = wal_obj.point.filter(status=1, expiry__gt=timezone.now()).order_by('created')
                    wal_total = sum(rew_points.values_list('current',flat=True))
                    if wal_total == 0:
                        messages.add_message(
                            request, messages.ERROR,
                            'Wallet has Zero Points')
                        return self.form_invalid(form)
                    if wal_total < points:
                        points = wal_total
                    wallettxn = WalletTransaction.objects.create(wallet=wal_obj, txn_type=2, point_value=points,
                                                                     notes=note, added_by=request.user.id)
                    if order:
                        wallettxn.order = order
                        wallettxn.save()
                    for pts in rew_points:
                        if pts.current >= points:
                            pts.current -= points
                            pts.last_used = timezone.now()
                            if pts.current == Decimal(0):
                               pts.status = 1
                            pts.save()
                            PointTransaction.objects.create(transaction=wallettxn,
                                                            point=pts,point_value=points,txn_type=2)

                            break

                        else:
                            points -= pts.current
                            pts.last_used = timezone.now()
                            pts.status = 2
                            PointTransaction.objects.create(
                                transaction=wallettxn,
                                point=pts,
                                point_value=pts.current,
                                txn_type=2)
                            pts.current = Decimal(0)
                            pts.save()

                    wallettxn.status = 1
                    wallettxn.current_value = wal_obj.get_current_amount()
                    wallettxn.save()
                    messages.add_message(request, messages.SUCCESS,
                                         'Successfull')

            else:
                messages.add_message(request, messages.ERROR,
                                     'UNABLE TO FIND WALLLET')
                return self.form_invalid(form)

            return self.form_valid(form)
        else:
            messages.add_message(request, messages.ERROR,
                                 'PLEASE CHECK/FILLUP THE DETAILS ')
            return self.form_invalid(form)


class WalletHistoryView(TemplateView):
    template_name = 'console/wallet/wallethistory.html'
    email = ''

    def get_context_data(self, **kwargs):
        email = self.request.GET.get('email', '')
        date_range = self.request.GET.get('date_range', '')
        filter_kwargs = {}
        if date_range:
            start_date, end_date = date_range.split(' - ')
            start_date = datetime.datetime.strptime(
                start_date + " 00:00:00", "%m/%d/%Y %H:%M:%S")
            end_date = datetime.datetime.strptime(
                end_date + " 23:59:59", "%m/%d/%Y %H:%M:%S")
            filter_kwargs['created__gte'] = start_date
            filter_kwargs['created__lte'] = end_date
        context = super(WalletHistoryView, self).get_context_data(**kwargs)
        wal_obj = None

        if email:
            wal_obj = Wallet.objects.filter(owner_email=email)
            wallet = wal_obj[0] if wal_obj.exists() else None
            if wallet:
                context['wallet'] = wallet
                context['wallet_data'] = wallet.wallettxn.filter(**filter_kwargs).order_by('-created')
                # if no date_range is given show last 20 transaction as per requirement
                if not date_range:
                    context['wallet_data'] = context['wallet_data'][:20]

        return context
