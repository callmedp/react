from collections import Iterable

from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views.decorators.cache import patch_cache_control

from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from functools import wraps


def flatlist(fatlist):
    for element in fatlist:
        if isinstance(element, Iterable) and not isinstance(element, (str, bytes)):
            yield from flatlist(element)
        else:
            yield element

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
    def _check_perm(view_func):
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
    return _check_perm


def check_group(grp_list):
    def _check_group(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user:
                flat_list = [ll for ll in flatlist(grp_list)]
                if request.user.is_anonymous:
                    return HttpResponseRedirect(reverse_lazy('console:login'))
                if request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
                if request.user.groups.filter(name__in=flat_list).exists():
                    return view_func(request, *args, **kwargs)
                return HttpResponseForbidden()
            return HttpResponseRedirect(reverse_lazy('console:login'))
        return wrapper
    return _check_group


def stop_browser_cache():
    def _stop_browser_cache(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            patch_cache_control(
                response, no_cache=True, no_store=True, must_revalidate=True,
                max_age=0)
            return response
        return wrapper
    return _stop_browser_cache
