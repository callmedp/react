from django.views.generic import TemplateView


class BlogAddView(TemplateView):
	template_name = "admin/base.html"

	def get(self, request, *args, **kwargs):
		context = super(BlogAddView, self).get(request, *args, **kwargs)
		return context

	def get_context_data(self, **kwargs):
		context = super(BlogAddView, self).get_context_data(**kwargs)

		return context