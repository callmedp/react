from django.views.generic import TemplateView, ListView
from django.http import HttpResponseForbidden
from django.template.loader import render_to_string

from .mixins import BlogMixin
from .models import Category


class BlogLandingPageView(TemplateView, BlogMixin):
	model = Category
	template_name = "blog/blog-landing.html"
	page = 1
	paginated_by = 1

	def get(self, request, *args, **kwargs):
		self.page = self.request.GET.get('page', 1)
		context = super(BlogLandingPageView, self).get(request, *args, **kwargs)
		return context

	def get_context_data(self, **kwargs):
		context = super(BlogLandingPageView, self).get_context_data(**kwargs)
		categories = Category.objects.filter(is_active=True)
		article_list = render_to_string('include/top_article.html',
			self.scrollPagination(
				paginated_by=self.paginated_by,
				page=self.page, object_list=categories))
		context.update({
			'categories': categories,
			'article_list': article_list
		})

		return context


class BlogLandingAjaxView(ListView, BlogMixin):
    model = Category
    template_name = 'include/top_article.html'
    page = 1
    paginated_by = 1

    def get(self, request, *args, **kwargs):
    	if request.is_ajax():
    		self.page = int(self.request.GET.get('page', 1))
    		return super(self.__class__, self).get(request, args, **kwargs)
    	else:
    		return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        category_list = context['category_list']
        context.update(self.scrollPagination(
        	paginated_by=self.paginated_by, page=self.page,
        	object_list=category_list))
        return context

    def get_queryset(self):
        queryset = super(self.__class__, self).get_queryset()
        qs = queryset.filter(is_active=True)
        return qs