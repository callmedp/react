import warnings

from django.contrib import messages
from django.core.paginator import InvalidPage
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, TemplateView
from .models import Product


class ProductDetailView(DetailView):
    context_object_name = 'product'
    http_method_names = ['get', 'post']

    model = Product
    __view_signal__ = None
    # # Whether to redirect to the URL with the right path
    # __enforce_paths__ = True
    # # Whether to redirect child products to their parent's URL
    # __enforce_parent__ = True

    def __init__(self, *args, **kwargs):
        # __view_signal__ = product_viewed

        super(ProductDetailView, self).__init__(*args, **kwargs)

    def get_template_names(self):
        return ['product/detail.html']
    
    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(ProductDetailView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        ctx = super(ProductDetailView, self).get_context_data(**kwargs)
        return ctx

    # def send_signal(self, request, response, product):
    #     self.view_signal.send(
    #         sender=self, product=product, user=request.user, request=request,
    #         response=response)

    # def redirect_if_necessary(self, current_path, product):
    #     if self.enforce_parent and product.is_child:
    #         return HttpResponsePermanentRedirect(
    #             product.parent.get_absolute_url())

    #     if self.enforce_paths:
    #         expected_path = product.get_absolute_url()
    #         if expected_path != urlquote(current_path):
    #             return HttpResponsePermanentRedirect(expected_path)

    def get(self, request, **kwargs):
        self.object = product = self.get_object()

        # redirect = self.redirect_if_necessary(request.path, product)
        # if redirect is not None:
        #     return redirect

        response = super(ProductDetailView, self).get(request, **kwargs)
        # self.send_signal(request, response, product)
        return response

