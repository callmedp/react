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