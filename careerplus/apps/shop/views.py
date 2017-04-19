import warnings

from django.contrib import messages
from django.core.paginator import InvalidPage
from django.http import Http404, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, TemplateView


class ProductDetailView(DetailView):
	pass
	
    # context_object_name = 'product'
    # model = Product
    # view_signal = product_viewed
    # template_folder = "catalogue"

    # # Whether to redirect to the URL with the right path
    # enforce_paths = True

    # # Whether to redirect child products to their parent's URL
    # enforce_parent = True

    # def get(self, request, **kwargs):
    #     """
    #     Ensures that the correct URL is used before rendering a response
    #     """
    #     self.object = product = self.get_object()

    #     redirect = self.redirect_if_necessary(request.path, product)
    #     if redirect is not None:
    #         return redirect

    #     response = super(ProductDetailView, self).get(request, **kwargs)
    #     self.send_signal(request, response, product)
    #     return response

    # def get_object(self, queryset=None):
    #     # Check if self.object is already set to prevent unnecessary DB calls
    #     if hasattr(self, 'object'):
    #         return self.object
    #     else:
    #         return super(ProductDetailView, self).get_object(queryset)

    # def redirect_if_necessary(self, current_path, product):
    #     if self.enforce_parent and product.is_child:
    #         return HttpResponsePermanentRedirect(
    #             product.parent.get_absolute_url())

    #     if self.enforce_paths:
    #         expected_path = product.get_absolute_url()
    #         if expected_path != urlquote(current_path):
    #             return HttpResponsePermanentRedirect(expected_path)

    # def get_context_data(self, **kwargs):
    #     ctx = super(ProductDetailView, self).get_context_data(**kwargs)
    #     ctx['alert_form'] = self.get_alert_form()
    #     ctx['has_active_alert'] = self.get_alert_status()
    #     return ctx

    # def get_alert_status(self):
    #     # Check if this user already have an alert for this product
    #     has_alert = False
    #     if self.request.user.is_authenticated():
    #         alerts = ProductAlert.objects.filter(
    #             product=self.object, user=self.request.user,
    #             status=ProductAlert.ACTIVE)
    #         has_alert = alerts.exists()
    #     return has_alert

    # def get_alert_form(self):
    #     return ProductAlertForm(
    #         user=self.request.user, product=self.object)

    # def send_signal(self, request, response, product):
    #     self.view_signal.send(
    #         sender=self, product=product, user=request.user, request=request,
    #         response=response)

    # def get_template_names(self):
    #     """
    #     Return a list of possible templates.

    #     If an overriding class sets a template name, we use that. Otherwise,
    #     we try 2 options before defaulting to catalogue/detail.html:
    #         1). detail-for-upc-<upc>.html
    #         2). detail-for-class-<classname>.html

    #     This allows alternative templates to be provided for a per-product
    #     and a per-item-class basis.
    #     """
    #     if self.template_name:
    #         return [self.template_name]

    #     return [
    #         '%s/detail-for-upc-%s.html' % (
    #             self.template_folder, self.object.upc),
    #         '%s/detail-for-class-%s.html' % (
    #             self.template_folder, self.object.get_product_class().slug),
    #         '%s/detail.html' % (self.template_folder)]


