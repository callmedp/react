from django.views.generic import TemplateView

from .models import Page


class CMSPageView(TemplateView):
	model = Page
	template_name = "cms/cms_page.html"

	def get(self, request, *args, **kwargs):
		context = super(CMSPageView, self).get(request, *args, **kwargs)
		return context
