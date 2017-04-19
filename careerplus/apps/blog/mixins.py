from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class BlogMixin(object):
	def scrollPagination(self, paginated_by=3, page=1, object_list=None):
		data = {}
		paginator = Paginator(object_list, paginated_by)
		try:
			page_obj = paginator.page(page)
		except PageNotAnInteger:
			page_obj = paginator.page(1)
		except EmptyPage:
			page_obj = paginator.page(paginator.num_pages)  # for out range deliver last page

		article_list = {}
		for p in page_obj:
			top_articles = p.primary_category.filter(status=1)
			if top_articles.count() > 3:
				top_articles = top_articles[: 3]
			elif top_articles.exists():
				top_articles = top_articles

			if top_articles:
				article_list.update({
					p: list(top_articles),
				})
		data.update({'page_obj': page_obj, 'article_list': article_list})
		return data


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