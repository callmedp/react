from django.views.generic import TemplateView


class CartView(TemplateView):
	template_name = "cart/cart.html"

	def get(self, request, *args, **kwargs):
		return super(self.__class__, self).get(request, *args, **kwargs)