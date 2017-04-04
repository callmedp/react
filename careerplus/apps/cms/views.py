from django.views.generic import TemplateView
from django.template.loader import render_to_string


from .models import Page


class CMSPageView(TemplateView):
	model = Page
	template_name = "cms/cms_page.html"

	def get(self, request, *args, **kwargs):
		context = super(CMSPageView, self).get(request, *args, **kwargs)
		return context

	def get_context_data(self, **kwargs):
		context = super(CMSPageView, self).get_context_data(**kwargs)
		page_obj = Page.objects.all().first()
		left_widgets = page_obj.pagewidget_set.filter(section='left').select_related('widget')
		right_widgets = page_obj.pagewidget_set.filter(section='right').select_related('widget')
		context['left_widgets'] = ''
		context['right_widgets'] = ''
		context['page_heading'] = page_obj.title
		download_docs = page_obj.document_set.filter(is_active=True)
		if download_docs.exists():
			download_doc = download_docs[0]
			context.update({
				'download_doc': download_doc
			})
		for left in left_widgets:
			widget_context = {}
			widget_context.update({
				'object': page_obj,
				'widget': left.widget,
				'download_doc': download_doc
			})
			widget_context.update(left.widget.get_widget_data())
			if left.widget.template_name:
				context['left_widgets'] += render_to_string('include/' + left.widget.template_name, widget_context)

		for right in right_widgets:
			widget_context = {}
			widget_context.update({
				'object': page_obj,
				'widget': left.widget,
				'download_doc': download_doc
			})
			widget_context.update(right.widget.get_widget_data())
			if right.widget.template_name:
				context['right_widgets'] += render_to_string('include/' + right.widget.template_name, widget_context)

		return context
