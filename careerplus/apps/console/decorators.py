from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator


from functools import wraps


def Decorate(decorator):
    def _inner(view_cls):
        old_dispatch = view_cls.dispatch

        @method_decorator(decorator)
        def new_dispatch(self, request, *args, **kwargs):
            return old_dispatch(self, request, *args, **kwargs)
        view_cls.dispatch = new_dispatch
        return view_cls
    return _inner


def check_permission(perm_name):
    def _check_group(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user:
                if request.user.is_anonymous:
                    return HttpResponseRedirect(reverse_lazy('console:login'))
                if request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
                if request.user.has_perm(perm_name):
                    return view_func(request, *args, **kwargs)
                return HttpResponseForbidden()
            return HttpResponseRedirect(reverse_lazy('console:login'))
        return wrapper
    return _check_group


