from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsVendorAssociated(BasePermission):
    """Will check if user whether user is vendor or vendor id is
     passed into the query parameters """

    def has_permission(self,request,view):
        user = request.user
        if not user.is_authenticated():
            return False
        if user.is_superuser:
            return True
        if request.query_params.get('vendor'):
            return True
        if user.get_vendor():
            return True
        return False

    def has_object_permission(self, request,view,obj):
        user = request.user
        if not user.is_authenticated():
            return False
        if user.is_superuser:
            return True
        if request.query_params.get('vendor'):
            return True
        if user.get_vendor():
            return True
        return False
