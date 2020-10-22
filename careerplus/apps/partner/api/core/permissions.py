from rest_framework import permissions


class IsEmployeeOfVendor(permissions.BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user, 'vendor_set') and request.user.vendor_set.count():
            if hasattr(view, 'kwargs') and 'vendor_id' in view.kwargs:
                return int(view.kwargs['vendor_id']) == request.user.vendor_set.all()[0].id
            else:
                return True

class IsAdminOrEmployeeOfVendor(permissions.BasePermission):
    def has_permission(self, request, view):
        if hasattr(request.user, 'vendor_set') and request.user.vendor_set.count():
            if hasattr(view, 'kwargs') and 'vendor_id' in view.kwargs:
                return int(view.kwargs['vendor_id']) == request.user.vendor_set.all()[0].id
            else:
                return True
        if request.user.is_authenticated and request.user.is_staff:
            return True
