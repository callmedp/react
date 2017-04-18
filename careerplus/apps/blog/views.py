from django.views.generic import TemplateView, ListView, DetailView
from django.http import HttpResponseForbidden, Http404
from django.template.loader import render_to_string
from django.core.paginator import Paginator

from meta.views import Meta

from .mixins import BlogMixin, PaginationMixin

from .models import Category, Blog


class BlogDetailView(DetailView):
    template_name = "blog/article-detail.html"
    model = Blog
    article = None

    def get(self, request, *args, **kwargs):
        self.slug = kwargs.get('slug', None)
        self.article = self.get_object()
        try:
            self.article = Blog.objects.get(slug=self.slug, status=1)
        except Exception:
            raise Http404

        self.article.no_views += 1
        self.article.save()
        context = super(self.__class__, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        categories = Category.objects.filter(is_active=True)
        blog = context['object']
        p_cat = blog.p_cat
        tags = blog.tags.filter(is_active=True)
        articles = p_cat.primary_category.filter(status=1)
        pop_aricles = articles[: 5]
        articles = articles.order_by('-publish_date')
        total_comment = blog.comment_set.filter(is_published=True,
            is_removed=False)
        context['meta'] = blog.as_meta(self.request)
        context.update({
            "categories": categories,
            "pop_articles": pop_aricles,
            "recent_articles": articles[: 5],
            "tags": tags,
            "total_comment": total_comment,
            "allow_comment": blog.allow_comment,
        })
        return context


class BlogCategoryListView(TemplateView, PaginationMixin):
    template_name = "blog/articles-by-category.html"
    cat_obj = None
    page = 1
    paginated_by = 1

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        self.page = request.GET.get('page', 1)
        self.active_tab = request.GET.get('tab', 0)
        try:
            self.cat_obj = Category.objects.get(slug=slug, is_active=True)
        except Exception:
            raise Http404
        context = super(self.__class__, self).get(request, args, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        pass
        
    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        cat_obj = self.cat_obj
        categories = Category.objects.filter(is_active=True)
        article_list = Blog.objects.filter(sec_cat__in=[cat_obj.pk], status=1) | Blog.objects.filter(p_cat=cat_obj, status=1)
        article_list = article_list.order_by('-publish_date')
        paginator = Paginator(article_list, self.paginated_by)
        page_data = self.pagination(paginator, self.page)
        context.update({
            "page_recent": page_data.get('page'),
            "recent_end": page_data.get('page_end'),
            "recent_middle": page_data.get('middle'),
            "recent_begin": page_data.get('begin'),
            "recent_articles": article_list[:5]
        })
        article_list = article_list.order_by('-score', '-publish_date')
        paginator = Paginator(article_list, self.paginated_by)
        page_data = self.pagination(paginator, self.page)
        context.update({
            "page_pop": page_data.get('page'),
            "pop_end": page_data.get('page_end'),
            "pop_middle": page_data.get('middle'),
            "pop_begin": page_data.get('begin'),
            "pop_articles": article_list[: 5]
        })
        context.update({
            "category": cat_obj,
            "categories": categories,
            "active_tab": self.active_tab,
        })
        return context


class BlogLandingPageView(TemplateView, BlogMixin):
	model = Category
	template_name = "blog/blog-landing.html"
	page = 1
	paginated_by = 1

	def get(self, request, *args, **kwargs):
		self.page = self.request.GET.get('page', 1)
		context = super(self.__class__, self).get(request, args, **kwargs)
		return context

	def get_context_data(self, **kwargs):
		context = super(self.__class__, self).get_context_data(**kwargs)
		categories = Category.objects.filter(is_active=True)
		article_list = render_to_string('include/top_article.html',
			self.scrollPagination(
				paginated_by=self.paginated_by,
				page=self.page, object_list=categories))
		context.update({
			'categories': categories,
			'article_list': article_list
		})

		context.update(self.get_breadcrumb_data())
		context.update(self.get_meta_details())
		return context

	def get_breadcrumb_data(self):
		breadcrumbs = []
		breadcrumbs.append({"url": '/', "name": "Home"})
		breadcrumbs.append({"url": None, "name": "Career Guidance"})
		data = {"breadcrumbs": breadcrumbs}
		return data

	def get_meta_details(self):
		meta = Meta(
		    title="Career Guidance & Advice – Articles @ Learning.Shine",
		    description='Planning to change career - Get advice and tips for better growth. Read latest articles for interview preparation, competitive exams, government jobs, resume writing tips & other career guidance at learning.shine',
		)
		return {"meta": meta}


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