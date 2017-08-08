from django.views.generic import (
    ListView,
    TemplateView,
)
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator

from core.decorators import mobile_page_only

from .models import Category, Blog
from .mixins import PaginationMixin


@method_decorator(mobile_page_only, name='dispatch')
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
        qs = queryset.filter(is_active=True)
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
            except:
                self.active_tab = 0
            self.cat_slug = self.request.GET.get('cat_slug', '')
            try:
                self.cat_obj = Category.objects.get(slug=self.cat_slug, is_active=True)
                return super(ArticleLoadMoreMobileView, self).get(request, args, **kwargs)
            except:
                return ''
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(ArticleLoadMoreMobileView, self).get_context_data(**kwargs)
        cat_obj = self.cat_obj
        main_articles = Blog.objects.filter(p_cat=cat_obj, status=1) | Blog.objects.filter(sec_cat__in=[cat_obj.pk], status=1)
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
