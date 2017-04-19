import json
import logging
import datetime

from django.views.generic import View
from django.http import HttpResponse
from django.utils import timezone

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


class CmsShareView(View):
	
	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			page_id = request.GET.get('page_id')
			try:
				obj = Page.objects.get(id=page_id)
				obj.total_share += 1
				obj.save()
				today = timezone.now()
				today_date = datetime.date(day=1, month=today.month, year=today.year)
				pg_counter, created = self.page_obj.pagecounter_set.get_or_create(count_period=today_date)
				pg_counter.no_shares += 1
				pg_counter.save()

			except:
				pass
			data = ["Success"]
			return HttpResponse(json.dumps(list(data)), content_type="application/json")


class CheckLoginStatus(View):
	
	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			action = request.GET.get('action', '')
			if action == 'login_status':
				data = {}
				if request.user.is_authenticated():
					data['status'] = 1
				else:
					data['status'] = 0
				return HttpResponse(json.dumps(data), content_type="application/json")
