#python imports

#django imports

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

