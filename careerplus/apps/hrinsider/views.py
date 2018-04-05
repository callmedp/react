import json
from django.shortcuts import render
from itertools import zip_longest
        
from django.views.generic import (
    TemplateView,
    DetailView,
    View)

from django.http import HttpResponseForbidden, Http404,\
    HttpResponsePermanentRedirect, HttpResponse
from django.conf import settings
from meta.views import Meta
from django.db.models import Count
from django.urls import reverse
from django.template.loader import render_to_string
from blog.mixins import BlogMixin, PaginationMixin
from blog.models import Category, Blog, Tag, Author


class HRLandingView(TemplateView, BlogMixin):
    model = Blog
    template_name = "hrinsider/hrindex.html"

    def __init__(self):
        self.page = 1
        self.paginated_by = 1

    def get(self, request, *args, **kwargs):
        self.page = self.request.GET.get('page', 1)
        context = super(self.__class__, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        categories = Category.objects.filter(
            is_active=True, visibility=3).order_by('-name')

        if kwargs.get('list'):
            article_list = Blog.objects.filter(
                status=1, visibility=3).select_related('p_cat', 'author').order_by('-no_views')
            context.update({'list': True})
        else:
            article_list = Blog.objects.filter(
                status=1, visibility=3).select_related('p_cat', 'author').order_by('-publish_date')[:10]
        top_article_list = Blog.objects.filter(
            status=1, visibility=3).select_related('p_cat', 'author')[:9]

        authors = Author.objects.filter(
            visibility=3, blog__visibility=3,
            blog__status=1).annotate(no_of_blog=Count('blog')).order_by('-no_of_blog')
        author_list = zip_longest(*[iter(authors)] * 6, fillvalue=None)
        
        context.update({
            'top_article_list': [top_article_list[:3], top_article_list[3:6], top_article_list[6:9]],
            'categories': categories,
            'article_list': article_list,
            'authors': authors,
            'authors_list': list(author_list)
        })

        context.update(self.get_breadcrumb_data())
        context.update(self.get_meta_details())
        return context

    def get_template_names(self):
        if self.kwargs.get('list'):
            temp = "hrinsider/hr_listing.html"
        else:
            temp = self.template_name
        return temp

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({
            "url": reverse('hrinsider:hr-landing'),
            "name": "HR Insider"})
        breadcrumbs.append({"url": None, "name": "All Articles"})
        data = {"breadcrumbs": breadcrumbs}
        return data

    def get_meta_details(self):
        meta = Meta(
            title="HR insider: Career Skilling for a future ready India",
            description="HR insider - The best way to choose better career options. Get experts' advice & ideas for planning your future growth @ Shine Learning",
        )
        return {"meta": meta}


class HRBlogDetailView(DetailView, BlogMixin):
    template_name = "hrinsider/hr_detail.html"
    model = Blog

    def __init__(self):
        self.article = None
        self.paginated_by = 1
        self.page = 1

    def get_queryset(self):
        qs = Blog.objects.filter(status=1, visibility=3)
        return qs

    def get_object(self, queryset=None):
        cat_slug = self.kwargs.get('cat_slug')
        slug = self.kwargs.get('slug')
        if queryset is None:
            queryset = self.get_queryset()

        if slug is not None:
            queryset = queryset.filter(slug=slug, status=1, visibility=3)
        try:
            obj = queryset.get()
        except:
            raise Http404
        return obj

    def get(self, request, *args, **kwargs):
        self.slug = kwargs.get('slug', None)
        self.page = request.GET.get('page', 1)
        self.object = self.get_object()
        self.object.no_views += 1
        self.object.update_score()
        self.object.save()

        context = super(self.__class__, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        blog = self.object
        p_cat = blog.p_cat
        articles = p_cat.primary_category.filter(
            status=1, visibility=3).exclude(pk=blog.pk)
        articles = articles.order_by('-publish_date')

        context['meta'] = blog.as_meta(self.request)

        context.update(self.get_breadcrumb_data())
        context['SITEDOMAIN'] = settings.SITE_DOMAIN

        main_obj = Blog.objects.filter(
            slug=blog.slug, status=1, visibility=3).prefetch_related('tags')

        article_list = Blog.objects.filter(
            p_cat=p_cat, status=1, visibility=3).order_by('-publish_date') | Blog.objects.filter(sec_cat__in=[p_cat], status=1, visibility=3).order_by('-publish_date')
        article_list = article_list.exclude(slug=blog.slug)
        article_list = article_list.distinct().select_related('created_by').prefetch_related('tags')

        context.update({
            "main_article": main_obj[0],
            "article_list": article_list,
        })

        context.update(self.get_meta_details())
        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": reverse('hrinsider:hr-landing'), "name": "HR Insider"})
        breadcrumbs.append({"url": reverse('hrinsider:hr-listing'), "name": "All Articles"})
        breadcrumbs.append({"url": None, "name": self.object.display_name})
        data = {"breadcrumbs": breadcrumbs}
        return data

    def get_meta_details(self):
        heading = self.object.heading
        des = self.object.get_description()
        meta = Meta(
            title=heading + "- HR Insider",
            description=des,
        )
        return {"meta": meta}


class HrConclaveView(TemplateView):
    model = Blog
    template_name = "hrinsider/conclave.html"

    def __init__(self):
        pass

    def get(self, request, *args, **kwargs):
        context = super(self.__class__, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        categories = Category.objects.filter(is_active=True, visibility=3).order_by('-name')

        if kwargs.get('list'):
            article_list = Blog.objects.filter(status=1, visibility=3).select_related('p_cat','author').order_by('-no_views')
            context.update({'list': True})
        else:
            article_list = Blog.objects.filter(status=1, visibility=3).select_related('p_cat','author').order_by('-publish_date')[:10]
        top_article_list = Blog.objects.filter(status=1, visibility=3).select_related('p_cat','author')[:9]

        authors = Author.objects.filter(visibility=3,blog__visibility=3,blog__status=1).annotate(no_of_blog=Count('blog')).order_by('-no_of_blog')
        author_list = zip_longest(*[iter(authors)]*6, fillvalue=None)
        
        context.update({
        'top_article_list': [top_article_list[:3], top_article_list[3:6], top_article_list[6:9]],
        'categories': categories,
        'article_list': article_list,
        'authors': authors,
        'authors_list': list(author_list)
        })

        context.update(self.get_breadcrumb_data())
        context.update(self.get_meta_details())
        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": reverse('hrinsider:hr-landing') , "name": "HR Insider"})
        breadcrumbs.append({"url": None, "name": "HR Conclave"})
        data = {"breadcrumbs": breadcrumbs}
        return data

    def get_meta_details(self):
        meta = Meta(
            title="HR insider: Career Skilling for a future ready India",
            description="HR insider - The best way to choose better career options. Get experts' advice & ideas for planning your future growth @ Shine Learning",
        )
        return {"meta": meta}


class HrJobFairView(TemplateView):
    model = Blog
    template_name = "hrinsider/jobfair.html"

    def __init__(self):
        pass

    def get(self, request, *args, **kwargs):
        context = super(self.__class__, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        categories = Category.objects.filter(is_active=True, visibility=3).order_by('-name')

        if kwargs.get('list'):
            article_list = Blog.objects.filter(status=1, visibility=3).select_related('p_cat','author').order_by('-no_views')
            context.update({'list': True})
        else:
            article_list = Blog.objects.filter(status=1, visibility=3).select_related('p_cat','author').order_by('-publish_date')[:10]
        top_article_list = Blog.objects.filter(status=1, visibility=3).select_related('p_cat','author')[:9]

        authors = Author.objects.filter(visibility=3,blog__visibility=3,blog__status=1).annotate(no_of_blog=Count('blog')).order_by('-no_of_blog')
        author_list = zip_longest(*[iter(authors)]*6, fillvalue=None)
        
        context.update({
        'top_article_list': [top_article_list[:3], top_article_list[3:6], top_article_list[6:9]],
        'categories': categories,
        'article_list': article_list,
        'authors': authors,
        'authors_list': list(author_list)
        })

        context.update(self.get_breadcrumb_data())
        context.update(self.get_meta_details())
        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": reverse('hrinsider:hr-landing'), "name": "HR Insider"})
        breadcrumbs.append({"url": None, "name": "Job Fair"})
        data = {"breadcrumbs": breadcrumbs}
        return data

    def get_meta_details(self):
        meta = Meta(
            title="HR insider: Career Skilling for a future ready India",
            description="HR insider - The best way to choose better career options. Get experts' advice & ideas for planning your future growth @ Shine Learning",
        )
        return {"meta": meta}
