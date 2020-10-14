from django.views.generic import (
    ListView,
    TemplateView,
)
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
import logging
from console.decorators import mobile_page_only

from .models import Category, Blog, Tag
from .mixins import PaginationMixin


@method_decorator(mobile_page_only(), name='dispatch')
class ArticleCategoryListMobile(ListView):
    model = Category
    template_name = 'blog/category-list.html'

    def get(self, request, *args, **kwargs):
        return super(ArticleCategoryListMobile, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArticleCategoryListMobile, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset = super(ArticleCategoryListMobile, self).get_queryset()
        qs = queryset.filter(is_active=True, visibility=1)
        return qs


class ArticleLoadMoreMobileView(TemplateView, PaginationMixin):
    model = Category
    template_name = 'include/loadmore-articles.html'

    def __init__(self):
        self.page = 1
        self.paginated_by = 10
        self.active_tab = 0
        self.cat_obj = None

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.page = int(request.GET.get('page', 1))
            try:
                self.active_tab = int(request.GET.get('tab', 0))
                if self.active_tab not in [0, 1]:
                    self.active_tab = 0
            except Exception as e:
                logging.getLogger('error_log').error("Unable to get active tab%s" % str(e))
                self.active_tab = 0
            self.cat_slug = self.request.GET.get('cat_slug', '')
            try:
                self.cat_obj = Category.objects.get(slug=self.cat_slug, is_active=True, visibility=1)
                return super(ArticleLoadMoreMobileView, self).get(request, args, **kwargs)
            except Exception as e:
                logging.getLogger('error_log').error("Unable to get category object%s" % str(e))
                return ''
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(ArticleLoadMoreMobileView, self).get_context_data(**kwargs)
        cat_obj = self.cat_obj
        main_articles = Blog.objects.filter(p_cat=cat_obj, status=1, visibility=1) | Blog.objects.filter(sec_cat__in=[cat_obj.pk], status=1, visibility=1)
        main_articles = main_articles.order_by('-publish_date').distinct().select_related('created_by')

        paginator = Paginator(main_articles, self.paginated_by)
        if self.active_tab == 0:
            page_data = self.pagination(paginator, self.page)
        else:
            main_articles = main_articles.order_by('-score', '-publish_date')
            paginator = Paginator(main_articles, self.paginated_by)
            page_data = self.pagination(paginator, self.page)

        context.update({
            "page_obj": page_data.get('page'),
            "category": cat_obj,
            "active_tab": self.active_tab,
        })
        return context


class ArticleLoadMoreTagView(TemplateView, PaginationMixin):
    model = Tag
    template_name = 'include/loadmore-tag-articles.html'

    def __init__(self):
        self.page = 1
        self.paginated_by = 10
        self.active_tab = 0
        self.tag_obj = None

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.page = int(request.GET.get('page', 1))
            try:
                self.active_tab = int(request.GET.get('tab', 0))
                if self.active_tab not in [0, 1]:
                    self.active_tab = 0
            except Exception as e:
                logging.getLogger('error_log').error("Unable to get active tab%s" % str(e))
                self.active_tab = 0
            self.tag_slug = self.request.GET.get('tag_slug', '')
            try:
                self.tag_obj = Tag.objects.get(slug=self.tag_slug, is_active=True, visibility=1)
                return super(ArticleLoadMoreTagView, self).get(request, args, **kwargs)
            except Exception as e:
                logging.getLogger('error_log').error("Unable to get tag object%s" % str(e))
                return ''
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(ArticleLoadMoreTagView, self).get_context_data(**kwargs)
        tag_obj = self.tag_obj
        article_list = tag_obj.blog_set.filter(status=1, visibility=1)
        article_list = article_list.order_by('-publish_date')

        if self.active_tab == 0:
            paginator = Paginator(article_list, self.paginated_by)
            page_data = self.pagination(paginator, self.page)
        else:
            article_list = article_list.order_by('-score', '-publish_date')
            paginator = Paginator(article_list, self.paginated_by)
            page_data = self.pagination(paginator, self.page)

        context.update({
            "page_obj": page_data.get('page'),
            "tag": tag_obj,
            "active_tab": self.active_tab,
        })
        return context
