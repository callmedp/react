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

