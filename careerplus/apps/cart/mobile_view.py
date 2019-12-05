import json

from django.views.generic import View
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from decimal import Decimal

from .mixins import CartMixin
from .models import Cart
from wallet.models import Wallet, WalletTransaction, PointTransaction


class RemoveFromCartMobileView(View, CartMixin):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = {"status": -1}
            product_reference = request.POST.get('product_reference')
            child_list = request.POST.getlist('child_list', [])
            try:
                if not self.request.session.get('cart_pk'):
                    self.getCartObject()

                cart_pk = self.request.session.get('cart_pk')
                if cart_pk:
                    cart_obj = Cart.objects.get(pk=cart_pk)
                    owner = cart_obj.owner_id
                    wal_obj = Wallet.objects.get(owner=owner)
                    if child_list:
                        for child_ref in child_list:
                            line_obj = cart_obj.lineitems.get(reference=child_ref)
                            if line_obj.parent_deleted:
                                parent = line_obj.parent
                                childs = cart_obj.lineitems.filter(
                                    parent=parent, parent_deleted=True)
                                if childs.count() > 1:
                                    line_obj.delete()
                                else:
                                    parent.delete()
                            else:
                                line_obj.delete()
                    elif product_reference:
                        line_obj = cart_obj.lineitems.get(
                            reference=product_reference)
                        if line_obj.parent_deleted:
                            parent = line_obj.parent
                            childs = cart_obj.lineitems.filter(
                                parent=parent, parent_deleted=True)
                            if childs.count() > 1:
                                line_obj.delete()
                            else:
                                parent.delete()
                        else:
                            line_obj.delete()
                    data['status'] = 1
    
                    cart_dict = self.get_solr_cart_items(cart_obj=cart_obj)
                    total_amount = cart_dict.get('total_amount', Decimal(0))  
                    # payment_dict = self.getPayableAmount(cart_obj, cart_dict.get('total_amount'))
                    # point = payment_dict["redeemed_reward_point"]
                    wal_txn = cart_obj.wallettxn.filter(
                            txn_type=2).order_by('-created').select_related('wallet')
                    if wal_txn:
                        wal_txn = wal_txn[0]
                        intial_redeemed_points = wal_txn.point_value
                    if intial_redeemed_points > total_amount:
                        points_used = wal_txn.usedpoint.all().order_by('point__pk')
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
                        points = wal_obj.point.filter(status=1).order_by('created')
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