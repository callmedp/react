import json
import logging
from django.conf import settings
from django.views.generic import View
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from decimal import Decimal

from .mixins import CartMixin
from .models import Cart
from .tasks import cart_product_removed_mail
from wallet.models import Wallet, WalletTransaction, PointTransaction
from payment.tasks import make_logging_request, make_logging_sk_request


class RemoveFromCartMobileView(View, CartMixin):

    def removeTracking(self, product_id, email_dict):
        tracking_id = self.request.session.get(
            'tracking_id', '')
        tracking_product_id = self.request.session.get(
            'tracking_product_id', '')
        product_tracking_mapping_id = self.request.session.get(
            'product_tracking_mapping_id', '')
        product_availability = self.request.session.get(
            'product_availability', '')
        trigger_point = self.request.session.get(
            'trigger_point','')
        u_id = self.request.session.get(
            'u_id','')
        position = self.request.session.get(
            'position',1)
        utm_campaign = self.request.session.get(
            'utm_campaign','')
        referal_product = self.request.session.get(
            'referal_product','')
        referal_subproduct = self.request.session.get(
            'referal_subproduct','')
        popup_based_product = self.request.session.get(
            'popup_based_product', '')
        if tracking_product_id == product_id and tracking_id:
            name = email_dict.get('name', '')
            email = email_dict.get('email', '')
            cart_product_removed_mail.apply_async(
                (product_id, tracking_id, u_id, email, name, 
                    tracking_product_id, product_tracking_mapping_id,
                    trigger_point, position, utm_campaign, 2, popup_based_product), 
                countdown=settings.CART_DROP_OUT_EMAIL)
            # cart_product_removed_mail(email_data)
            make_logging_sk_request.delay(
                tracking_product_id, product_tracking_mapping_id, tracking_id, 'remove_product',position, trigger_point,\
                 u_id, utm_campaign, 2, referal_product, referal_subproduct, popup_based_product)
            # for showing the user exits for that particular cart product
            make_logging_sk_request.delay(
                tracking_product_id, product_tracking_mapping_id, tracking_id, 'exit_cart',position, trigger_point, u_id, \
                utm_campaign, 2, referal_product, referal_subproduct, popup_based_product)
            if tracking_id:
                del self.request.session['tracking_id']
            if product_tracking_mapping_id:
                del self.request.session['product_tracking_mapping_id']
            if tracking_product_id:
                del self.request.session['tracking_product_id']
            if product_availability:
                del self.request.session['product_availability']

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {"status": -1}
            product_reference = request.POST.get('product_reference')
            child_list = request.POST.getlist('child_list', [])
            email_dict = {}
            try:
                if not self.request.session.get('cart_pk'):
                    self.getCartObject()

                cart_pk = self.request.session.get('cart_pk')
                if cart_pk:
                    cart_obj = Cart.objects.filter(pk=cart_pk).first()
                    if cart_obj:
                        email = cart_obj.email if cart_obj.email else ""
                        first_name = cart_obj.first_name if cart_obj.first_name else ""
                        last_name = cart_obj.last_name if cart_obj.last_name else ""
                        name = "{} {}".format(first_name, last_name)
                        email_dict.update({
                            'email' : email,
                            'name' : name
                        })
                    if child_list:
                        for child_ref in child_list:
                            line_obj = cart_obj.lineitems.get(
                                reference=child_ref)
                            if line_obj.parent_deleted:
                                parent = line_obj.parent
                                childs = cart_obj.lineitems.filter(
                                    parent=parent, parent_deleted=True)
                                if childs.count() > 1:
                                    self.removeTracking(line_obj.product.id, email_dict)
                                    line_obj.delete()

                                else:
                                    self.removeTracking(parent.product.id, email_dict)
                                    parent.delete()

                            else:
                                self.removeTracking(line_obj.product.id, email_dict)
                                line_obj.delete()

                    elif product_reference:
                        line_obj = cart_obj.lineitems.get(
                            reference=product_reference)
                        if line_obj.parent_deleted:
                            parent = line_obj.parent
                            childs = cart_obj.lineitems.filter(
                                parent=parent, parent_deleted=True)
                            if childs.count() > 1:
                                self.removeTracking(
                                    line_obj.product.id, email_dict)
                                line_obj.delete()

                            else:
                                self.removeTracking(parent.product.id, email_dict)
                                parent.delete()

                        else:
                            self.removeTracking(line_obj.product.id, email_dict)
                            line_obj.delete()

                    data['status'] = 1

                    cart_dict = self.get_solr_cart_items(cart_obj=cart_obj)
                    total_amount = Decimal(
                        cart_dict.get('total_amount', Decimal(0)))
                    initial_redeemed_points = Decimal(0)
                    # payment_dict = self.getPayableAmount(cart_obj, cart_dict.get('total_amount'))
                    # point = payment_dict["redeemed_reward_point"]
                    wal_txn = cart_obj.wallettxn.filter(
                        txn_type=2).order_by('-created').select_related('wallet')
                    if wal_txn:
                        wal_txn = wal_txn[0]
                        initial_redeemed_points = wal_txn.point_value
                    if initial_redeemed_points > total_amount:
                        points_used = wal_txn.usedpoint.all().order_by('point__pk')
                        owner = cart_obj.owner_id
                        wal_obj = Wallet.objects.get(owner=owner)
                        for pts in points_used:
                            r_point = pts.point
                            r_point.current += pts.point_value
                            r_point.last_used = timezone.now()
                            pts.txn_type = 5
                            if r_point.expiry <= timezone.now():
                                r_point.status = 3
                            else:
                                r_point.status = 1
                            r_point.save()
                            pts.save()
                        wal_txn.txn_type = 5
                        wal_txn.notes = 'Reverted From Cart'
                        wal_txn.status = 1
                        wal_txn.current_value = wal_txn.wallet.get_current_amount()
                        wal_txn.save()

                        point = total_amount
                        points = wal_obj.point.filter(
                            status=1).order_by('created')
                        wallettxn = WalletTransaction.objects.create(
                            wallet=wal_obj, cart=cart_obj, txn_type=2, point_value=point)
                        for pts in points:
                            if pts.expiry >= timezone.now():
                                if point > Decimal(0):
                                    if pts.current >= point:
                                        pts.current -= point
                                        pts.last_used = timezone.now()
                                        if pts.current == Decimal(0):
                                            pts.status = 1
                                        pts.save()
                                        PointTransaction.objects.create(
                                            transaction=wallettxn,
                                            point=pts,
                                            point_value=point,
                                            txn_type=2)
                                        point = Decimal(0)

                                    else:
                                        point -= pts.current
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
                        wallettxn.notes = 'Redeemed from cart'
                        wallettxn.current_value = wal_obj.get_current_amount()
                        wallettxn.save()

                else:
                    data['error_message'] = 'this cart item alredy removed.'

            except Exception as e:
                data['error_message'] = str(e)

            return HttpResponse(json.dumps(data), content_type="application/json")

        return HttpResponseForbidden()
