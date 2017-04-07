import json
import logging

from django.views.generic import View
from django.http import HttpResponse
from cms.models import Page
from cms.mixins import LoadMoreMixin


class AjaxCommentLoadMoreView(View, LoadMoreMixin):

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			slug = request.POST.get('slug', '')
			page = int(request.POST.get('page', 1))
			try:
				page_obj = Page.objects.get(slug=slug, is_active=True)
				comments = page_obj.comment_set.filter(is_published=True,
					is_removed=False)
				comment_list = self.pagination_method(page=page,
					comment_list=comments, page_obj=page_obj)
				return HttpResponse(json.dumps({'comment_list': comment_list}))
			except Exception as e:
				logging.getLogger('error_log').error("%s " % str(e))
