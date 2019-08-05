#python imports

#django imports
from django.conf import settings

#local imports

#inter app imports

#third party imports
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsObjectOwner(BasePermission):
    """
    Works for all RUD views.
    Generic permission for handling single objects.
    """
    def has_permission(self,request,view):

        user = request.user

        if request.method in list(SAFE_METHODS):
            return True

        if not user.is_authenticated():
            return False

        if request.method == "POST":
            return True

        return True

    def has_object_permission(self,request,view,obj):
        owner_fields = getattr(view,'owner_fields',['owner_id','candidate_id'])
        permission_granted = False

        user = request.user

        if not user.is_authenticated():
            return False

        for field in owner_fields:
            object_data = getattr(obj,field,'')
            if object_data == str(user.id):
                permission_granted = True
                break

        return permission_granted


class IsActiveUser(BasePermission):

    def has_permission(self,request,view):
        return request.user.is_active


class InFeedbackGroup(BasePermission):

    def has_permission(self,request,view):
        user = request.user
        if user.is_superuser:
            return True
        ops_head_group = settings.OPS_HEAD_GROUP_LIST
        feedback_call_group = settings.WELCOMECALL_GROUP_LIST
        if user.groups.filter(name__in=ops_head_group).exists():
            return True
        elif user.groups.filter(name__in=feedback_call_group).exists():
            return True
        return False

class CanShowProducts(BasePermission):
    """allow to view product list and its details  """

    def has_permission(self, request,view):
        user = request.user

        if not user.is_authenticated():
            return False

        if user.is_superuser:
            return True
        elif user.get_vendor_list():
            return True
        elif not (getattr(view,'permission_code_name') or getattr(view,'permission_groups')):
            return False
        elif any(perms for perms in view.permission_code_name if perms in user.get_all_permissions()):
            return True
        elif any(group for group in view.permission_groups if group in user.groups.all()):
            return True
        return False

    def has_object_permission(self, request,view,obj):
        """check user is trying to fetch the products """

        user = request.user
        if not user.is_authenticated():
            return False
        if user.is_superuser:
            return True
        elif user.get_vendor_list():
            return True
        elif not (getattr(view, 'permission_code_name') or getattr(view, 'permission_groups')):
            return False
        elif any(perms for perms in view.permission_code_name if perms in user.get_all_permissions()):
            return True
        elif any(group for group in view.permission_groups if group in user.groups.all()):
            return True
        return False


