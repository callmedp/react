import json
from django.shortcuts import render

from django.views.generic import (
    TemplateView,
    DetailView,
    View)

from django.http import HttpResponseForbidden, Http404,\
    HttpResponsePermanentRedirect, HttpResponse
from django.db.models import Count
from django.core.paginator import Paginator
from django.urls import reverse
from django.template.loader import render_to_string

from django.conf import settings
from meta.views import Meta
from blog.mixins import BlogMixin, PaginationMixin
from blog.models import Category, Blog, Tag, Author

from users.forms import (
    ModalLoginApiForm,
    ModalRegistrationApiForm,
    PasswordResetRequestForm
)

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

        article_list = Blog.objects.filter(status=1, visibility=2).select_related('p_cat','author').order_by('-publish_date')[:10]
        top_article_list = Blog.objects.filter(status=1, visibility=2).select_related('p_cat','author')[:9]

        authors = Author.objects.filter(visibility=2).annotate(no_of_blog=Count('blog')).order_by('-no_of_blog')

        top_3_cats = [article.p_cat.slug for article in top_article_list][:3]
        top_cats = ' '.join(top_3_cats)
        popular_courses = self.get_product(top_cats)

        context.update({
        'top_article_list':[top_article_list[:3], top_article_list[3:6], top_article_list[6:9]],
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

        authors = Author.objects.filter(visibility=2,is_active=1).annotate(no_of_blog=Count('blog')).order_by('-no_of_blog')

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
        breadcrumbs.append({"url": reverse('talent:talent-landing'), "name": "Talent Economy"})
        breadcrumbs.append({"url": None, "name": self.cat_obj.name})
        data = {"breadcrumbs": breadcrumbs}
        return data

class TEBlogDetailView(DetailView, BlogMixin):
    template_name = "talenteconomy/article-detail.html"
    model = Blog

    def __init__(self):
        self.article = None
        self.paginated_by = 1
        self.page = 1

    def get_queryset(self):
        qs = Blog.objects.filter(status=1,visibility=2)
        return qs

    def get_object(self, queryset=None):
        cat_slug = self.kwargs.get('cat_slug')
        slug = self.kwargs.get('slug')
        if queryset is None:
            queryset = self.get_queryset()

        if slug is not None:
            queryset = queryset.filter(slug=slug, status=1, visibility=2)
        try:
            obj = queryset.get()
        except:
            raise Http404
        return obj

#    def redirect_if_necessary(self, current_path, article):
#        expected_path = article.get_absolute_url()
#        if expected_path != urlquote(current_path):
#            return HttpResponsePermanentRedirect(expected_path)
#        return None

    def get(self, request, *args, **kwargs):
        self.slug = kwargs.get('slug', None)
        self.page = request.GET.get('page', 1)
        self.object = self.get_object()
        self.object.no_views += 1
        self.object.update_score()
        self.object.save()
        #redirect = self.redirect_if_necessary(request.path, self.object)
        #if redirect:
        #    return redirect

        context = super(self.__class__, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        blog = self.object
        p_cat = blog.p_cat
        articles = p_cat.primary_category.filter(status=1, visibility=2).exclude(pk=blog.pk)
        articles = articles.order_by('-publish_date')

        context['meta'] = blog.as_meta(self.request)
        context.update({
            "reset_form": PasswordResetRequestForm()
        })
        context.update(self.get_breadcrumb_data())
        context['SITEDOMAIN'] = settings.SITE_DOMAIN

        main_obj = Blog.objects.filter(slug=blog.slug, status=1, visibility=2)

        detail_obj = self.scrollPagination(
                paginated_by=self.paginated_by, page=self.page,
                object_list=main_obj)
        #if self.request.flavour == 'mobile':
         #   detail_article = render_to_string('include/detail-article-list.html',
          #      {"page_obj": detail_obj,
           #     "slug": blog.slug,
            #    "SITEDOMAIN": settings.SITE_DOMAIN,
             #   "main_article": main_obj[0]})
        #else:
        detail_article = render_to_string('include/detail-article-list.html',
            {"page_obj": detail_obj,
            "slug": blog.slug, "SITEDOMAIN": settings.SITE_DOMAIN})

        context.update({
            "detail_article": detail_article,
            "main_article": main_obj[0],
        })

        article_list = Blog.objects.filter(p_cat=p_cat, status=1, visibility=2).order_by('-publish_date') | Blog.objects.filter(sec_cat__in=[p_cat], status=1, visibility=2).order_by('-publish_date')
        article_list = article_list.exclude(slug=blog.slug)
        article_list = article_list.distinct().select_related('created_by').prefetch_related('tags')

        page_obj = self.scrollPagination(
                paginated_by=self.paginated_by, page=self.page,
                object_list=article_list)

        context.update({
            "scroll_article": render_to_string('include/detail-article-list.html',
                {"page_obj": page_obj,
                "slug": blog.slug, "SITEDOMAIN": settings.SITE_DOMAIN})
        })

        context.update({
            "loginform": ModalLoginApiForm(),
            "registerform": ModalRegistrationApiForm()
        })

        popular_courses = self.get_product(p_cat.slug)
        context.update({
            "popular_courses": popular_courses,
        })

        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        breadcrumbs.append({"url": reverse('talent:talent-landing'), "name": "Talent Economy"})
        #breadcrumbs.append({"url": reverse('te-articles-by-category', kwargs={'slug': self.object.p_cat.slug}), "name": self.object.p_cat.name})
        breadcrumbs.append({"url": '/', "name": self.object.p_cat.name})
        breadcrumbs.append({"url": None, "name": self.object.display_name})
        data = {"breadcrumbs": breadcrumbs}
        return data

class AuthorListingView(TemplateView):
    model = Author
    template_name = "talenteconomy/author-listing.html"

    def get(self, request, *args, **kwargs):
        context = super(self.__class__, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)

        categories = Category.objects.filter(is_active=True, visibility=2).order_by('-name')

        authors = Author.objects.filter(is_active=1,visibility=2).annotate(no_of_blog=Count('blog')).order_by('-no_of_blog')

        top_article_list = Blog.objects.filter(status=1, visibility=2).select_related('p_cat')[:9]
        top_3_cats = [article.p_cat.slug for article in top_article_list][:3]
        top_cats = ' '.join(top_3_cats)
        popular_courses = BlogMixin().get_product(top_cats)

        context.update({
        'authors':authors,
        'categories': categories,
        'popular_courses':popular_courses,
        })

        context.update(self.get_breadcrumb_data())
        context.update(self.get_meta_details())
        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        breadcrumbs.append({"url": reverse('talent:talent-landing'), "name": "Talent Economy"})
        breadcrumbs.append({"url": None, "name": "Authors"})
        data = {"breadcrumbs": breadcrumbs}
        return data

    def get_meta_details(self):
        meta = Meta(
            title="Career & Certification Guidance Top Authors @ Shine Learning",
            description="Use experts’ advice & guidance to decide your career path. Get the list of authors and related articles written by experts @ Shine Learning",
        )
        return {"meta": meta}

class AuthorDetailView(DetailView):
    template_name = "talenteconomy/author-detail.html"
    model = Author

    def get(self, request, *args, **kwargs):
        context = super(self.__class__, self).get(request, args, **kwargs)
        return context

    def get_queryset(self):
        qs = Author.objects.filter(is_active=1,visibility=2)
        return qs

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        if queryset is None:
            queryset = self.get_queryset()

        if slug is not None:
            queryset = queryset.filter(slug=slug, is_active=1, visibility=2)
        try:
            obj = queryset.get()
        except:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        author = self.object

        context['meta'] = author.as_meta(self.request)
        context.update(self.get_breadcrumb_data())
        context['SITEDOMAIN'] = settings.SITE_DOMAIN

        article_list = Blog.objects.filter(status=1, visibility=2, author=author).order_by('-publish_date')
        most_recent_cat = article_list[0].p_cat.slug if article_list else ''

        popular_courses = BlogMixin().get_product(most_recent_cat)

        context.update({
            "author":author,
            "article_list":article_list,
            "popular_courses": popular_courses,
        })

        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        breadcrumbs.append({"url": reverse('talent:talent-landing'), "name": "Talent Economy"})
        breadcrumbs.append({"url": reverse('talent:authors-listing'), "name": "Authors"})
        breadcrumbs.append({"url": None, "name": self.object.name})
        data = {"breadcrumbs": breadcrumbs}
        return data

