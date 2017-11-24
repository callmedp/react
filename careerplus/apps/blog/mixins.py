from collections import OrderedDict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.middleware.csrf import get_token
from core.library.haystack.query import SQS
from django.conf import settings

class BlogMixin(object):
	def scrollPagination(self, paginated_by=3, page=1, object_list=None):
		# data = {}
		paginator = Paginator(object_list, paginated_by)
		try:
			page_obj = paginator.page(page)
		except PageNotAnInteger:
			page_obj = paginator.page(1)
		except EmptyPage:
			page_obj = paginator.page(paginator.num_pages)  # for out range deliver last page
		return page_obj

	def get_product(self, query=''):
		if query:
			product = []
			slug = settings.COURSE_SLUG[0]
			results = SQS().filter(text=query, pPc=slug).extra({
			        'mm': '1',
			        'qt': 'edismax',
			        'qf': 'text pHd^10 pFA^6 pCtg^4 pCC^2 pAb^1',
			        'tie': 1,
			        'hl': 'false',
			        'spellcheck': 'false'
			    }).only(
				'pTt pURL pHd pAR pNJ pImA pImg pNm pBC pARx pPc , pStar')[:5]
			for prd in results:
				product.append(OrderedDict({
					'title': prd.pTt,
					'url': prd.pURL,
					'display_name':prd.pHd,
					'name': prd.pNm,
					'avg_rating_exact': prd.pARx,
					'avg_rating':prd.pAR,
					'num_jobs': prd.pNJ,
					'image': prd.pImg,
					'image_alt':prd.pImA,
					'buy_count':prd.pBC,
					'class':prd.pPc,
					'star': prd.pStar

					}))
			return product	
		return []


class LoadCommentMixin(object):
	def pagination_loadmore(self, page, paginated_by, comment_list):
		paginator = Paginator(comment_list, paginated_by)
		try:
			comments = paginator.page(page)
		except PageNotAnInteger:
			comments = paginator.page(1)
		except EmptyPage:
			comments = paginator.page(paginator.num_pages)  # If page is out of range (e.g. 9999), deliver last page of results.
		return comments


class PaginationMixin(object):
	def pagination(self, paginator, page):
		try:
			page = paginator.page(page)
		except PageNotAnInteger:
			page = paginator.page(1)
		except EmptyPage:
			page = paginator.page(paginator.num_pages)

		begin_pages = 1
		end_pages = 1
		before_pages = 2
		after_pages = 2
		begin = list(page.paginator.page_range[:begin_pages])
		end = list(page.paginator.page_range[-end_pages:])
		middle = list(page.paginator.page_range[
			max(page.number - before_pages - 1, 0):page.number + after_pages])

		if set(begin) & set(middle):
			begin = sorted(set(begin + middle))
			middle = []

		elif begin[-1] + 1 == middle[0]:
			begin += middle
			middle = []
		elif middle[-1] + 1 == end[0]:
			end = middle + end
			middle = []
		elif set(middle) & set(end):
			end = sorted(set(middle + end))
			middle = []

		if set(begin) & set(end):
			begin = sorted(set(begin + end))
			middle, end = [], []
		elif begin[-1] + 1 == end[0]:
			begin += end
			middle, end = [], []

		context = {}
		context['page'] = page
		context['begin'] = begin
		context['middle'] = middle
		context['page_end'] = end
		return context