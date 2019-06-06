#python imports

#django imports

#local imports

#inter app imports

#third party imports
from rest_framework.permissions import BasePermission, SAFE_METHODS

class OrderAccessPermission(BasePermission):
    """
    Works for all RUD views.
    Generic permission for handling single objects.
    """
    def has_permission(self,request,view):
        user = request.user
        if user and user.is_superuser or user.has_perm('order.can_view_order_detail'):
            return True
        return False

    def has_object_permission(self,request,view,obj):
        user = request.user
        if user and user.is_superuser or user.has_perm('order.can_view_order_detail'):
            return True
        return False

