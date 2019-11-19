#python imports

#django imports

from django.db.models.query_utils import Q

#local imports

#inter app imports
from order.models import OrderItem,Order
from partner.models import VendorHierarchy


#third party imports
from rest_framework.permissions import BasePermission, SAFE_METHODS


class OrderAccessPermission(BasePermission):
    """
        Works for all RUD views.
        Generic permission for handling single objects.
        """

    def has_permission(self, request, view):

        user = request.user

        if user and user.is_superuser:
            return True

        if not user or not user.has_perm(
                'order.can_view_order_detail'):
            return False

        order = view.kwargs.get('pk')

        if not order:
            return False

        order = Order.objects.filter(id=order).first()

        if not order:
            return False

        order_items = order.orderitems.all()

        vendor_ids = [x.vendee.id for x in VendorHierarchy.objects.filter(employee=user, active=True)]
        if vendor_ids:
            order_items = order_items.filter(Q(partner_id__in=vendor_ids) | \
                                            Q(product__vendor_id__in=vendor_ids))

        # Handle Writers
        if user.is_writer:
            order_items = order_items.filter(assigned_to=request.user)

        if not order_items:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user and user.is_superuser:
            return True

        if not user or not user.has_perm(
                'order.can_view_order_detail'):
            return False

        order_items = obj.orderitems.all()
        vendor_ids = [x.vendee.id for x in
                      VendorHierarchy.objects.filter(employee=user,
                                                     active=True)]
        if vendor_ids:
            order_items = order_items.filter(Q(partner_id__in=vendor_ids) | \
                                             Q(product__vendor_id__in=vendor_ids))

        # Handle Writers
        if user.is_writer:
            order_items = order_items.filter(assigned_to=request.user)

        if not order_items:
            return False
        return True


class OrderItemAccessPermission(BasePermission):
    """
    Works for all RUD views.
    Generic permission for handling single objects.
    """
    def has_permission(self,request, view):
        user = request.user

        if user and user.is_superuser:
            return True

        if not user or not user.has_perm(
                'order.can_view_order_detail'):
            return False

        oi = view.kwargs.get('oi_id')

        if not oi:
            return False

        oi = OrderItem.objects.filter(id=oi).first()

        if not oi:
            return False

        order_items = oi.order.orderitems.all()

        vendor_ids = [x.vendee.id for x in VendorHierarchy.objects.filter( \
            employee=user, active=True)]
        if vendor_ids:
            order_items = order_items.filter(Q(partner_id__in=vendor_ids) | \
                                        Q(product__vendor_id__in=vendor_ids))

        # Handle Writers
        if user.is_writer:
            order_items = order_items.filter(assigned_to=request.user)

        if not order_items:
            return False
        return True

    def has_object_permission(self,request,view,obj):
        user = request.user
        if user and user.is_superuser:
            return True

        if not user or not user.has_perm(
                'order.can_view_order_detail'):
            return False

        order_items = obj.order.orderitems.all()
        vendor_ids = [x.vendee.id for x in VendorHierarchy.objects.filter(employee=user, active=True)]
        if vendor_ids:
            order_items = order_items.filter(Q(partner_id__in=vendor_ids) | \
                                             Q(product__vendor_id__in=vendor_ids))

        # Handle Writers
        if user.is_writer:
            order_items = order_items.filter(assigned_to=request.user)

        if not order_items:
            return False
        return True


class IsObjectOwnerOrConsoleUser(BasePermission):
    """
    Permission to check if it is a console user or a shine candidate
    """
    def has_permission(self,request,view):
        user = request.user
        pdetail = getattr(user,'personal_detail',None)
        candidate_id = pdetail[0].get('id') if pdetail else None
        if candidate_id:
            return True

        if user and user.is_superuser:
            return True
        if not user or not user.has_perm(
                'order.can_view_order_detail'):
            return False

        oi = view.kwargs.get('oi_id')

        if not oi:
            return False

        oi = OrderItem.objects.filter(id=oi).first()

        if not oi:
            return False

        order_items = oi.order.orderitems.all()

        vendor_ids = [x.vendee.id for x in VendorHierarchy.objects.filter(employee=user, active=True)]
        if vendor_ids:
            order_items = order_items.filter(Q(partner_id__in=vendor_ids) | \
                                            Q(product__vendor_id__in=vendor_ids))
        # Handle Writers
        if user.is_writer:
            order_items = order_items.filter(assigned_to=request.user)

        if not order_items:
            return False
        return True

    def has_object_permission(self,request,view,obj):
        user = request.user
        pdetail = getattr(user, 'personal_detail',None)
        candidate_id = pdetail[0].get('id') if pdetail else None
        if candidate_id:
            return True
        if user and user.is_superuser:
            return True

        if not user or not user.has_perm(
                'order.can_view_order_detail'):
            return False

        order_items = obj.order.orderitems.all()
        vendor_ids = [x.vendee.id for x in
                      VendorHierarchy.objects.filter(employee=user,
                                                     active=True)]
        if vendor_ids:
            order_items = order_items.filter(Q(partner_id__in=vendor_ids) | \
                                            Q(product__vendor_id__in=vendor_ids))

        # Handle Writers
        if user.is_writer:
            order_items = order_items.filter(assigned_to=request.user)

        if not order_items:
            return False
        return True
