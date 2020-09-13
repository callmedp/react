# python imports
import logging
from datetime import datetime, date
from decimal import Decimal
from django.utils import timezone
from django.conf import settings

# django imports

# local imports

# inter app imports
from cart.mixins import CartMixin
from cart.models import Cart
from cart.tasks import cart_product_removed_mail
from wallet.models import (Wallet,
                           PointTransaction, WalletTransaction)

from wallet.api.core.serializers import (
    WalletSerializer, WalletTransactionSerializer)

# third party imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class RemoveFromCartAPIView(CartMixin, APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = None

    def post(self, request, *args, **kwargs):
        data = {"status": -1}
        reference = request.data.get('reference_id', None)
        resume_shine_cart = request.data.get('resume_shine', False)
        cart_pk = request.data.get('cart_pk', None)
        child_list = request.data.get('child_list', [])
        product_reference = request.data.get('product_reference', None)
        tracking_id = request.data.get('tracking_id', '')
        domain = 3
        cart_obj = None

        if cart_pk is None:
            return Response({"error_message": 'Please Provide cart_pk'},
                            status=status.HTTP_400_BAD_REQUEST)
        if reference is None:
            return Response({"error_message": 'Please provide reference id'},
                            status=status.HTTP_400_BAD_REQUEST)

        cart_obj = Cart.objects.filter(pk=cart_pk).first()
        if not cart_obj:
            return Response({"error_message": 'No cart  available with cart id ' + str(cart_pk)},
                            status=status.HTTP_400_BAD_REQUEST)

        if child_list:
            for child_ref in child_list:
                line_obj = cart_obj.lineitems.filter(
                    reference=child_ref).first()

                if not line_obj:
                    return Response({"error_message": 'No line obj available \
                         with child reference ' + str(child_ref)},
                                    status=status.HTTP_400_BAD_REQUEST)

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
            line_obj = cart_obj.lineitems.filter(
                reference=product_reference).first()
            if not line_obj:
                return Response({"error_message": 'No line obj available \
                   with  product reference id ' + str(product_refernece)},
                                status=status.HTTP_400_BAD_REQUEST)
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

        line_obj = cart_obj.lineitems.filter(reference=reference).first()

        if not line_obj:
            return Response({"error_message": 'No line obj available \
                   with reference id ' + str(reference)},
                            status=status.HTTP_400_BAD_REQUEST)
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

        if tracking_id:
            email = request.data.get('email', '')
            name = request.data.get('name', '')
            u_id = request.data.get('u_id', '')
            trigger_point = request.data.get('trigger_point', '')
            position = request.data.get('position', '')
            utm_campaign = request.data.get('utm_campaign', '')
            product_id = request.data.get('product_id', '')
            product_tracking_mapping_id = request.data.get('product_tracking_mapping_id', '')
            cart_product_removed_mail.apply_async(
                    (product_id, tracking_id, u_id, email, name, 
                        product_id, product_tracking_mapping_id,
                        trigger_point, position, utm_campaign, domain), 
                    countdown=settings.CART_DROP_OUT_EMAIL)

        cart_dict = self.get_solr_cart_items(cart_obj=cart_obj)
        total_amount = Decimal(cart_dict.get('total_amount', Decimal(0)))
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
            if not owner:
                return Response({"error_message": 'No cart owner available'},
                                status=status.HTTP_400_BAD_REQUEST)

            wal_obj = Wallet.objects.filter(owner=owner).first()

            if not wal_obj:
                return Response({"error_message": 'No Wallet object available \
                    for candidate id ' + str(owner)},
                                status=status.HTTP_400_BAD_REQUEST)

            for pts in points_used:
                r_point = pts.point
                r_point.current += pts.point_value
                r_point.last_used = timezone.now()
                pts.txn_type = 5
                if r_point.expiry <= timezone.now():
                    r_point.status = 3
                else:
                    r_point.status = 1
                try:
                    r_point.save()
                except Exception as e:
                    logging.getLogger('error_log').error(
                        "unable to update wallet txn %s " % str(e))
                    return Response({"error_message": "unable to save rewards points %s" % str(e)},
                                    status=status.HTTP_400_BAD_REQUEST)
                try:
                    pts.save()
                except Exception as e:
                    logging.getLogger('error_log').error(
                        "unable to save wallet points %s " % str(e))
                    return Response({"error_message": "unable to save wallet points %s" % str(e)},
                                    status=status.HTTP_400_BAD_REQUEST)

            wal_txn.txn_type = 5
            wal_txn.notes = 'Reverted From Cart'
            wal_txn.status = 1
            wal_txn.current_value = wal_txn.wallet.get_current_amount()
            try:
                wal_txn.save()
            except Exception as e:
                logging.getLogger('error_log').error(
                    "unable to update wallet txn %s " % str(e))
                return Response({"error_message": "unable to update wallet txn %s" % str(e)},
                                status=status.HTTP_400_BAD_REQUEST)

            point = total_amount
            points = wal_obj.point.filter(status=1).order_by(
                'created') if wal_obj else []
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
                            try:
                                pts.save()
                            except Exception as e:
                                logging.getLogger('error_log').error(
                                    "unable to update wallet points %s " % str(e))
                                return Response({"error_message": "unable to update wallet points %s" % str(e)},
                                                status=status.HTTP_400_BAD_REQUEST)

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
                            try:
                                pts.save()
                            except Exception as e:
                                logging.getLogger('error_log').error(
                                    "unable to update wallet points %s " % str(e))
                                return Response({"error_message": "unable \
                                    to update wallet points %s" % str(e)},
                                                status=status.HTTP_400_BAD_REQUEST)

            wallettxn.status = 1
            wallettxn.notes = 'Redeemed from cart'
            wallettxn.current_value = wal_obj.get_current_amount()
            try:
                wallettxn.save()
            except Exception as e:
                logging.getLogger('error_log').error(
                    "unable to update wallet txn %s " % str(e))
                return Response({"error_message": "unable \
                                    to update wallet txn %s" % str(e)},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_200_OK)
