from django.views.generic import View, TemplateView, FormView

from wallet.models import (
    Wallet, RewardPoint, ECash,
    WalletTransaction, ECashTransaction, PointTransaction)
from .wallet_form import Walletform
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






class WalletView(FormView):
    template_name = 'console/wallet/walletrew.html'
    form_class = Walletform
    http_method_names = [u'get', u'post']
    model = Wallet
    success_url = "/console/wallet/"



    def get(self, request, *args, **kwargs):
        if request.user.is_superuser == True:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            return self.render_to_response(self.get_context_data(form=form))
        else:
            return HttpResponseForbidden("you are not allowed to view this page")



    def post(self, request, *args, **kwargs):

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():

            email = form.cleaned_data['email_id']
            owner = form.cleaned_data['owner_id']
            note = form.cleaned_data['notes']
            points = form.cleaned_data['point_value']
            action = form.cleaned_data['wallet_action']
            wal_obj = ""

            try:

                if email:
                    wal_obj = Wallet.objects.get(owner_email=email)
                if owner and not wal_obj:
                    wal_obj = Wallet.objects.get(owner=owner)
                if wal_obj:
                    expiry = timezone.now() + datetime.timedelta(days=30)
                    if action =='addpoints':

                        point_obj = wal_obj.point.create(
                            original=points,
                            current=points,
                            expiry=expiry,
                            status=1
                        )

                        # wal_obj.point.create(original=points, current=points, expiry=expiry, status=1)
                        wal_txn = wal_obj.wallettxn.create(txn_type=1, status=1, point_value=points)

                        point_obj.wallettxn.create(
                            transaction=wal_txn,
                            point_value=points,
                            txn_type=1
                        )

                        wal_txn.current_value = wal_obj.get_current_amount()
                        wal_txn.save()




                    else:
                        rew_points = wal_obj.point.filter(status=1, expiry__gt=timezone.now()).order_by('created')
                        wal_total = sum(rew_points.values_list('current',flat=True))
                        wallettxn = WalletTransaction.objects.create(wallet=wal_obj, txn_type=2, point_value=points,
                                                                     notes= note)
                        for pts in rew_points:
                            if pts.current >= points:
                                pts.current -= points
                                pts.last_used = timezone.now()
                                if pts.current == Decimal(0):
                                   pts.status = 1
                                pts.save()
                                PointTransaction.objects.create(transaction=wallettxn,
                                                                point=pts,point_value=points,txn_type=2)

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
                else:
                    return self.form_invalid(form)
            except Exception as e:
                logging.getLogger('error_log').error(str(e))


            return self.form_valid(form)
        else:
            return self.form_invalid(form)
