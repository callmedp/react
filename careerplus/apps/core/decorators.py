from django.http import Http404


def mobile_page_only(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.flavour == 'mobile':
            return view_func(request, *args, **kwargs)

        else:
            raise Http404
    return _wrapped_view_func