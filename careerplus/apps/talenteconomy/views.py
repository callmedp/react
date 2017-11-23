import json
from django.shortcuts import render

from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    View)

from django.http import HttpResponseForbidden, Http404,\
    HttpResponsePermanentRedirect, HttpResponse
from django.db.models import Count
from django.core.paginator import Paginator
from django.urls import reverse

from django.conf import settings
from meta.views import Meta
from blog.mixins import BlogMixin, PaginationMixin
from blog.models import Category, Blog, Tag, Author

class TalentEconomyLandingView(TemplateView, BlogMixin):
    model = Blog
    template_name = "talenteconomy/landing.html"

    def __init__(self):
        self.page = 1
        self.paginated_by = 1

    def get(self, request, *args, **kwargs):
        self.page = self.request.GET.get('page', 1)
        context = super(self.__class__, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        categories = Category.objects.filter(is_active=True, visibility=2).order_by('-name')

        article_list = Blog.objects.filter(status=1, visibility=2).select_related('p_cat','author').order_by('-publish_date')
        top_article_list = Blog.objects.filter(status=1, visibility=2).select_related('p_cat','author')[:9]

        authors = Author.objects.filter(visibility=2).annotate(no_of_blog=Count('blog')).order_by('no_of_blog')

        top_3_cats = [article.p_cat.slug for article in top_article_list][:3]
        top_cats = ' '.join(top_3_cats)
        popular_courses = self.get_product(top_cats)

        context.update({
        'top_article_list':top_article_list,
        'categories': categories,
        'article_list': article_list,
        'popular_courses':popular_courses,
        'authors':authors,
        })

        context.update(self.get_breadcrumb_data())
        context.update(self.get_meta_details())
        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        breadcrumbs.append({"url": None, "name": "Talent Economy"})
        data = {"breadcrumbs": breadcrumbs}
        return data

    def get_meta_details(self):
        meta = Meta(
            title="Talent Economy: Career Skilling for a future ready India",
            description="Talent Economy - The best way to choose better career options. Get experts' advice & ideas for planning your future growth @ Shine Learning",
        )
        return {"meta": meta}

class TEBlogCategoryListView(TemplateView, PaginationMixin):
    template_name = "talenteconomy/category.html"

    def __init__(self):
        self.page = 1
        self.paginated_by = 8
        self.cat_obj = None

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        self.page = request.GET.get('page', 1)
        try:
            self.cat_obj = Category.objects.get(slug=slug, is_active=True, visibility=2)
        except Exception:
            raise Http404

        context = super(TEBlogCategoryListView, self).get(request, args, **kwargs)
        context = super(TEBlogCategoryListView, self).get(request, args, **kwargs)
        return context
        
    def get_context_data(self, **kwargs):
        context = super(TEBlogCategoryListView, self).get_context_data(**kwargs)
        cat_obj = self.cat_obj

        categories = Category.objects.filter(is_active=True, visibility=2).order_by('-name')

        authors = Author.objects.filter(visibility=2).annotate(no_of_blog=Count('blog')).order_by('no_of_blog')

        main_articles = Blog.objects.filter(p_cat=cat_obj, status=1, visibility=2) | Blog.objects.filter(sec_cat__in=[cat_obj.pk], status=1, visibility=2)
        main_articles = main_articles.order_by('-publish_date').distinct().select_related('author')

        paginator = Paginator(main_articles, self.paginated_by)
        page_data = self.pagination(paginator, self.page)

        popular_courses = BlogMixin().get_product(cat_obj.slug)

        context.update({
            "recent_page": page_data.get('page'),
            "recent_end": page_data.get('page_end'),
            "recent_middle": page_data.get('middle'),
            "recent_begin": page_data.get('begin'),
            "recent_articles": main_articles
        })
        context.update({
            "authors":authors,
            "category": cat_obj,
            "categories": categories,
            "popular_courses":popular_courses,
        })
        context.update(self.get_breadcrumb_data())
        context['meta'] = cat_obj.as_meta(self.request)
        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        breadcrumbs.append({"url": '/talenteconomy/', "name": "Talent Economy"})
        breadcrumbs.append({"url": None, "name": self.cat_obj.name})
        data = {"breadcrumbs": breadcrumbs}
        return data
