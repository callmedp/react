import json
from django.shortcuts import render
from itertools import zip_longest
import logging

from django.views.generic import (
    TemplateView,
    DetailView,
    View)

from django.http import HttpResponseForbidden, Http404,\
    HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.db.models import Count
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.http import urlquote

from django.template.loader import render_to_string
from django.db.models import Q


from django.conf import settings
from meta.views import Meta
from blog.mixins import BlogMixin, PaginationMixin
from blog.models import Category, Blog, Tag, Author
from shop.models import ProductSkill, Product

from geolocation.models import Country


from users.forms import (
    ModalLoginApiForm,
    ModalRegistrationApiForm,
    PasswordResetRequestForm
)

class CategoryUrl():
    def get_category_url(self, popular_courses):
        cat_url = '/'
        
        if len(popular_courses):
            pd_id = popular_courses[0].get('pid')
            category = Product.objects.get(id=pd_id).get_category_main()
            if(category):
                cat_url = category.get_absolute_url()

        return cat_url

class TalentEconomyLandingView(TemplateView, BlogMixin):
    model = Blog
    template_name = "talenteconomy/landing.html"

    def __init__(self):
        self.page = 1
        self.paginated_by = 10

    def get(self, request, *args, **kwargs):
        self.page = self.request.GET.get('page', 1)
        context = super(self.__class__, self).get(request, args, **kwargs)
        return context


    def get_countries(self):
        country_choices = [(m.phone, m.name) for m in
            Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
        initial_country = Country.objects.filter(phone='91')[0].phone
        return country_choices,initial_country



    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)

        # we are fetching categories from the articles instead of
        # checking if article exists for each categories.
        article_list = Blog.objects.filter(
            status=1, visibility=2).select_related(
            'p_cat', 'author').order_by('-last_modified_on')
        p_cat = [p for p in article_list.values_list('p_cat', flat=True)]
        sec_cat = [sec for sec in article_list.values_list('sec_cat', flat=True)]
        categories_id = set(p_cat + sec_cat)
        categories = Category.objects.filter(
            is_active=True, visibility=2, id__in=categories_id
        ).order_by('-name')
        article_list = article_list

        page_obj = self.scrollPagination(
            paginated_by=self.paginated_by, page=self.page,
            object_list=article_list)

        list_article = None
        if article_list:
            list_article = render_to_string('include/article-load-more.html', {
                "page_obj": page_obj,
                "SITEDOMAIN": settings.SITE_DOMAIN})
        top_article_list = list(Blog.objects.filter(
            status=1, visibility=2).select_related('p_cat', 'author').exclude(position__gt=0))[:9]
        # use position of page
        top_article_list_with_position = list(Blog.objects.filter(
            status=1, visibility=2, position__gt=0).order_by('position').select_related('p_cat', 'author'))[:9]
        if len(top_article_list_with_position) > 0:
            [top_article_list.insert((article.position - 1), article)
                for article in top_article_list_with_position]
        top_article_list = top_article_list[:9]
        authors = Author.objects.filter(
            is_active=True, blog__visibility=2,
            blog__status=1).annotate(
            no_of_blog=Count('blog')).order_by('-no_of_blog')
        author_list = zip_longest(*[iter(authors)] * 5, fillvalue=None)

        top_3_cats = [article.p_cat.slug for article in top_article_list][:3]
        top_cats = '+'.join(top_3_cats)

        # popular courses..
        top_blog_ids = [b.id for b in article_list[: 5]]
        skills = Tag.objects.prefetch_related('blog_set').filter(
            blog__id__in=top_blog_ids, is_active=True).distinct()

        skills = [sk.name for sk in skills]

        popular_courses = self.get_product(top_cats, skills)
        category_url = CategoryUrl().get_category_url(popular_courses)

        country_choices, initial_country = self.get_countries()
        context.update({'country_choices': country_choices, 'initial_country': initial_country, })

        context.update({
            'top_article_list': [
                top_article_list[:3], top_article_list[3:6],
                top_article_list[6:9]],
            'categories': categories,
            'article_list': list_article,
            'article_listing': article_list[: 5],
            'popular_courses': popular_courses,
            'authors': authors,
            'authors_list': list(author_list),
            'show_chat': True,
            'page_url': category_url
        })

        context.update(self.get_breadcrumb_data())
        context.update(self.get_meta_details())
        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home", "position": "1"})
        breadcrumbs.append({"url": None, "name": "Talent Economy", "position": "2"})
        data = {"breadcrumbs": breadcrumbs}
        return data

    def get_meta_details(self):
        meta = Meta(
            title="Talent Economy: Career Skilling for a future ready India",
            description="Talent Economy - The best way to choose better career options. Get experts' advice & ideas for planning your future growth @ Shine Learning",
        )
        return {"meta": meta}


class TalentEconomyLoadMoreView(TemplateView, BlogMixin):

    model = Blog
    template_name = 'include/article-load-more.html'

    def __init__(self):

        self.page = 1
        self.paginated_by = 10
        self.article_obj=None

    def get(self, request, *args, **kwargs):
        self.page = self.request.GET.get('page', 1)
        context = super(self.__class__, self).get(request, args, **kwargs)
        if request.is_ajax:
            self.article_obj = Blog.objects.filter(
                status=1, visibility=2).select_related(
                'p_cat', 'author').order_by('-publish_date')

            page_obj = self.scrollPagination(
                paginated_by=self.paginated_by, page=self.page,
                object_list=self.article_obj)

            article_list = render_to_string(
                'include/article-load-more.html', {
                    "page_obj": page_obj,
                    "SITEDOMAIN": settings.SITE_DOMAIN, })

            data = {
                'article_list': article_list,
            }

            return HttpResponse(
                json.dumps(data), content_type="application/json")


class TETagArticleView(TemplateView, BlogMixin):

    template_name = "talenteconomy/tag_article.html"

    def __init__(self):
        self.page = 1
        self.paginated_by = 10
        self.tag_obj = None

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        self.page = request.GET.get('page', 1)
        try:
            self.tag_obj = Tag.objects.get(slug=slug, is_active=True)
        except Exception:
            raise Http404

        context = super(TETagArticleView, self).get(request, args, **kwargs)
        return context

    def get_countries(self):
        country_choices = [(m.phone, m.name) for m in
            Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
        initial_country = Country.objects.filter(phone='91')[0].phone
        return country_choices,initial_country



    def get_context_data(self, **kwargs):
        context = super(
            TETagArticleView, self).get_context_data(**kwargs)
        tag_obj = self.tag_obj

        categories = Category.objects.filter(
            is_active=True, visibility=2).order_by('-name')

        authors = Author.objects.filter(
            is_active=1, blog__visibility=2,
            blog__status=1).annotate(
            no_of_blog=Count('blog')).order_by('-no_of_blog')

        author_list = zip_longest(*[iter(authors)] * 5, fillvalue=None)

        main_articles = tag_obj.blog_set.filter(
            status=1, visibility=2).order_by('-publish_date')

        recent_articles = self.scrollPagination(
            paginated_by=self.paginated_by, page=self.page,
            object_list=main_articles)

        # paginator = Paginator(main_articles, self.paginated_by)
        # page_data = self.pagination(paginator, self.page)

        # popular courses..
        top_blog_ids = [b.id for b in main_articles[: 5]]
        skills = Tag.objects.prefetch_related('blog_set').filter(
            blog__id__in=top_blog_ids, is_active=True).distinct()

        skills = [sk.name for sk in skills]

        popular_courses = BlogMixin().get_product(
            tag_obj.slug, skills)

        category_url = CategoryUrl().get_category_url(popular_courses)

        detail_article = None
        if recent_articles:
            detail_article = render_to_string('include/talent_page.html', {
                "page_obj": recent_articles,
                "slug": tag_obj.slug, "SITEDOMAIN": settings.SITE_DOMAIN})
        context.update({
            # "recent_page": page_data.get('page'),
            # "recent_end": page_data.get('page_end'),
            # "recent_middle": page_data.get('middle'),
            # "recent_begin": page_data.get('begin'),
            # "recent_articles": detail_obj
            "detail_article": detail_article,
        })
        context.update({
            "authors": authors,
            'authors_list': list(author_list),
            "tag": tag_obj,
            "categories": categories,
            "popular_courses": popular_courses,
            "show_chat": True,
            "page_url": category_url
        })
        country_choices, initial_country = self.get_countries()
        context.update({'country_choices': country_choices, 'initial_country': initial_country, })
        context.update(self.get_breadcrumb_data())
        context['meta'] = tag_obj.as_meta(self.request)
        context.update(self.get_meta_details())

        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home", "position": "1"})
        breadcrumbs.append({"url": reverse('talent:talent-landing'), "name": "Talent Economy", "position": "2"})
        breadcrumbs.append({"url": None, "name": self.tag_obj.name, "position": "3"})
        data = {"breadcrumbs": breadcrumbs}
        return data

    def get_meta_details(self):
        name = self.tag_obj.name
        meta = Meta(
            title=name + " - Career & Certification Guidance @ Shine Learning",
            description="Read Latest Articles on %s. Find the Most Relevant Information, News and other career guidance for %s at Shine Learning" %(name,name),
        )
        return {"meta": meta}


class TETagLoadmoreArticleView(TemplateView, BlogMixin):

    template_name = "include/talent_page.html"

    def __init__(self):
        self.page = 1
        self.paginated_by = 10
        self.tag_obj = None

    def get(self, request, *args, **kwargs):
        slug = request.GET.get('slug', None)
        self.page = request.GET.get('page', 1)
        if request.is_ajax():
            try:
                self.tag_obj = Tag.objects.get(slug=slug, is_active=True)
            except Exception:
                return ''

            context = super(TETagLoadmoreArticleView, self).get(request, args, **kwargs)
            return context
        return ''

    def get_context_data(self, **kwargs):
        context = super(
            TETagLoadmoreArticleView, self).get_context_data(**kwargs)
        tag_obj = self.tag_obj

        tag_articles = tag_obj.blog_set.filter(
            status=1, visibility=2).order_by('-publish_date')

        tag_articles = self.scrollPagination(
            paginated_by=self.paginated_by, page=self.page,
            object_list=tag_articles)

        # detail_article = None
        # if recent_articles:
        #     detail_article = render_to_string('include/talent_page.html', {
        #         "page_obj": recent_articles,
        #         "slug": tag_obj.slug, "SITEDOMAIN": settings.SITE_DOMAIN})
        context.update({
            'page_obj': tag_articles,
            'slug': tag_obj.slug,
            "SITEDOMAIN": settings.SITE_DOMAIN
        })
        return context


class TEBlogCategoryListView(TemplateView, BlogMixin):
    template_name = "talenteconomy/category.html"

    def __init__(self):
        self.page = 1
        self.paginated_by = 8
        self.cat_obj = None

    def get_template_names(self):
        slug =self.kwargs.get('slug')
        if slug == 'human-resources':
            return "talenteconomy/category1.html"
        return self.template_name

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)

        self.page = request.GET.get('page', 1)
        try:
            self.cat_obj = Category.objects.get(slug=slug, is_active=True)
            if not self.cat_obj.article_exists():
                return HttpResponseRedirect(reverse('talent:talent-landing'))
        except Exception as e:
            logging.getLogger('error_log').error('unable to get category object %s' % str(e))
            raise Http404

        redirect = self.redirect_if_necessary(request.path, self.cat_obj)

        if redirect:
            return redirect
        context = super(TEBlogCategoryListView, self).get(request, args, **kwargs)
        return context

    def get_countries(self):
        country_choices = [(m.phone, m.name) for m in
            Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
        initial_country = Country.objects.filter(phone='91')[0].phone
        return country_choices,initial_country


    def redirect_if_necessary(self, current_path, category):
        expected_path = category.get_absolute_url()
        if expected_path != urlquote(current_path):
            return HttpResponsePermanentRedirect(expected_path)
        return None

    def get_context_data(self, **kwargs):
        context = super(
            TEBlogCategoryListView, self).get_context_data(**kwargs)
        cat_obj = self.cat_obj

        # we are fetching categories from the articles instead of
        # checking if article exists for each categories.
        article_for_category = Blog.objects.filter(
            status=1, visibility=2).select_related(
            'p_cat', 'author').order_by('-last_modified_on')
        p_cat = [p for p in article_for_category.values_list('p_cat', flat=True)]
        sec_cat = [sec for sec in article_for_category.values_list('sec_cat', flat=True)]
        categories_id = set(p_cat + sec_cat)
        categories = Category.objects.filter(
            is_active=True, visibility=2, id__in=categories_id
        ).order_by('-name')

        authors = Author.objects.filter(
            is_active=1, blog__visibility=2,
            blog__status=1).annotate(
            no_of_blog=Count('blog')).order_by('-no_of_blog')
        author_list = zip_longest(*[iter(authors)] * 5, fillvalue=None)
        main_articles = Blog.objects.filter(
            p_cat=cat_obj,
            status=1,
            visibility=2) | Blog.objects.filter(
            sec_cat__in=[cat_obj.pk], status=1, visibility=2)
        main_articles = main_articles.order_by(
            '-last_modified_on').distinct().select_related('author')

        recent_articles = self.scrollPagination(
            paginated_by=self.paginated_by, page=self.page,
            object_list=main_articles)

        # popular courses..
        top_blog_ids = [b.id for b in main_articles[: 5]]
        skills = Tag.objects.prefetch_related('blog_set').filter(
            blog__id__in=top_blog_ids, is_active=True).distinct()

        skills = [sk.name for sk in skills]

        popular_courses = BlogMixin().get_product(
            cat_obj.slug, skills)

        category_url = CategoryUrl().get_category_url(popular_courses)

        article_list = None
        if recent_articles:
            article_list = render_to_string(
                'include/category-article-list.html', {
                "page_obj": recent_articles,
                "slug": cat_obj.slug, "SITEDOMAIN": settings.SITE_DOMAIN})
        context.update({
            "article_list": article_list,
        })
        context.update({
            "authors": authors,
            'authors_list': list(author_list),
            "category": cat_obj,
            "categories": categories,
            "popular_courses": popular_courses,
            'show_chat': True,
            "page_url": category_url
        })
        context.update(self.get_breadcrumb_data())
        context['meta'] = cat_obj.as_meta(self.request)
        context.update(self.get_meta_details())
        country_choices, initial_country = self.get_countries()
        context.update({'country_choices': country_choices, 'initial_country': initial_country, })
        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home", "position": "1"})
        breadcrumbs.append({"url": reverse('talent:talent-landing'), "name": "Talent Economy", "position": "2"})
        breadcrumbs.append({"url": None, "name": self.cat_obj.name, "position": "3"})
        data = {"breadcrumbs": breadcrumbs}
        return data

    def get_meta_details(self):
        name = self.cat_obj.name
        meta = Meta(
            # title=name + " - Career & Certification Guidance @ Shine Learning",
            # description="Read Latest Articles on %s. Find the Most Relevant Information, News and other career guidance for %s at Shine Learning" %(name,name),
            title = self.cat_obj.get_title,
            description = self.cat_obj.get_description if self.cat_obj.get_description else ("Read Latest Articles on %s. Find the Most Relevant Information, News and other career guidance for %s at Shine Learning" %(name,name)),
        )
        return {"meta": meta}


class TECategoryArticleLoadView(View, BlogMixin):

    def __init__(self):
        self.page = 1
        self.paginated_by = 8
        self.slug = None
        self.cat_obj = None

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.page = self.request.GET.get('page', 1)
            self.slug = self.request.GET.get('slug')
            try:
                self.cat_obj = Category.objects.get(
                    slug=self.slug, is_active=True, visibility=2)
                main_articles = Blog.objects.filter(
                    p_cat=self.cat_obj,
                    status=1,
                    visibility=2) | Blog.objects.filter(
                    sec_cat__in=[self.cat_obj.pk], status=1, visibility=2)
                main_articles = main_articles.order_by(
                    '-publish_date').distinct().select_related('author')
                page_obj = self.scrollPagination(
                    paginated_by=self.paginated_by, page=self.page,
                    object_list=main_articles)

                article_list = render_to_string(
                    'include/category-article-list.html', {
                    "page_obj": page_obj,
                    "slug": self.cat_obj.slug,
                    "SITEDOMAIN": settings.SITE_DOMAIN, })

                data = {
                    'article_list': article_list,
                }

                return HttpResponse(
                    json.dumps(data), content_type="application/json")
            except:
                pass
        return HttpResponseForbidden()


class TEBlogDetailView(DetailView, BlogMixin):
    template_name = "talenteconomy/article-detail1.html"
    model = Blog

    def __init__(self):
        self.article = None
        self.paginated_by = 1
        self.page = 1

    def get_queryset(self):
        qs = Blog.objects.filter(status=1)
        return qs

    def get_object(self, queryset=None):
        cat_slug = self.kwargs.get('cat_slug')
        slug = self.kwargs.get('slug')
        if queryset is None:
            queryset = self.get_queryset()

        if slug is not None:
            queryset = queryset.filter(slug=slug, status=1)
        try:
            obj = queryset.get()
        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset %s' % str(e))
            raise Http404
        return obj

    def get_countries(self):
        country_choices = [(m.phone, m.name) for m in
            Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
        initial_country = Country.objects.filter(phone='91')[0].phone
        return country_choices,initial_country



    def get_template_names(self):
        if not self.request.amp and self.object.p_cat.slug == 'human-resources':
            return ["talenteconomy/article-detail1"
                    ".html"]
        if not self.request.amp:
            return ["talenteconomy/article-detail.html"]

        if not settings.DEBUG:
            from newrelic import agent
            agent.disable_browser_autorum()
        return ["talenteconomy/article-detail-amp.html"]

    def redirect_if_necessary(self, current_path, article):
       expected_path = article.get_absolute_url()
       if expected_path != urlquote(current_path):
           return HttpResponsePermanentRedirect(expected_path)
       return None

    def get(self, request, *args, **kwargs):
        self.slug = kwargs.get('slug', None)
        self.page = request.GET.get('page', 1)
        self.object = self.get_object()
        self.object.no_views += 1
        self.object.update_score()
        # self.object.save()
        redirect = self.redirect_if_necessary(request.path, self.object)
        if redirect:
           return redirect

        context = super(self.__class__, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        blog = self.object
        p_cat = blog.p_cat
        articles = p_cat.primary_category.filter(
            status=1, visibility=2).exclude(pk=blog.pk)
        articles = articles.order_by('-publish_date')
        context['meta'] = blog.as_meta(self.request)
        context.update({
            "reset_form": PasswordResetRequestForm()
        })
        context.update(self.get_breadcrumb_data())
        context['SITEDOMAIN'] = settings.SITE_DOMAIN

        main_obj = Blog.objects.filter(slug=blog.slug, status=1, visibility=2)
        main_obj_list = list(main_obj)
        article_list = Blog.objects.filter(
            p_cat=p_cat, status=1, visibility=2).order_by(
            '-publish_date') | Blog.objects.filter(
            sec_cat__in=[p_cat], status=1,
            visibility=2).order_by('-publish_date')
        article_list = article_list.exclude(pk=blog.pk)
        article_list = article_list.distinct().select_related(
            'created_by', 'author').prefetch_related('tags')

        article_list = list(article_list)

        object_list = main_obj_list + article_list
        country_choices,initial_country = self.get_countries()
        detail_obj = self.scrollPagination(
            paginated_by=self.paginated_by, page=self.page,
            object_list=object_list)
        
        # Related Articles...
        related_articles=[]
        related_articles_ids_list = json.loads(self.object.related_arts)
        related_articles = Blog.objects.filter(id__in=related_articles_ids_list)[:3]

        if self.request.flavour == 'mobile':
            detail_article = render_to_string(
                'talenteconomy/include/detail-article-list.tmpl.html',
                {
                    "page_obj": detail_obj,
                    "slug": blog.slug,
                    "visibility": blog.visibility,
                    "SITEDOMAIN": settings.SITE_DOMAIN,
                    "login_status": 1 if self.request.session.get('candidate_id') else 0,
                    "related_articles": related_articles
                })
        else:
            detail_article = render_to_string(
                'talenteconomy/include/detail-article-list.tmpl.html',
                {
                    "page_obj": detail_obj,
                    "slug": blog.slug,
                    "visibility": blog.visibility,
                    "SITEDOMAIN": settings.SITE_DOMAIN,
                    "STATIC_URL": settings.STATIC_URL,
                    "related_articles": related_articles
                })

        context.update({
            "detail_article": detail_article,
            "main_article": main_obj[0],
            'country_choices': country_choices,
            'initial_country':initial_country,
        })

        context.update({
            "loginform": ModalLoginApiForm(),
            "registerform": ModalRegistrationApiForm(),
            "amp": self.request.amp
        })

        # popular courses..
        skills = blog.tags.filter(is_active=True)

        skills = [sk.name for sk in skills]

        popular_courses = self.get_product(
            p_cat.slug, skills)

        category_url = CategoryUrl().get_category_url(popular_courses)
        
        context.update({
            "popular_courses": popular_courses,
            "show_chat": True,
            "page_url": category_url
        })

        context.update(self.get_meta_details())
        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home", "position": "1"})
        breadcrumbs.append({
            "url": reverse('talent:talent-landing'), "name": "Talent Economy", "position": "2"})
        breadcrumbs.append({
            "url": reverse(
                'talent:te-articles-by-category',
                kwargs={'slug': self.object.p_cat.slug}),
            "name": self.object.p_cat.name, "position": "3"})
        breadcrumbs.append({"url": None, "name": self.object.display_name, "position": "4"})
        data = {"breadcrumbs": breadcrumbs}
        return data

    def get_meta_details(self):
        heading = self.object.heading
        des = self.object.get_description()
        meta = Meta(
            title=heading + "- Talent Economy",
            description=des,
        )
        return {"meta": meta}


class AuthorListingView(TemplateView):
    model = Author
    template_name = "talenteconomy/author-listing.html"

    def get(self, request, *args, **kwargs):
        context = super(self.__class__, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)

        categories = Category.objects.filter(
            is_active=True, visibility=2).order_by('-name')

        authors = Author.objects.filter(
            is_active=1,
            blog__visibility=2, blog__status=1).annotate(
            no_of_blog=Count('blog')).order_by('-no_of_blog')
        author_list = zip_longest(*[iter(authors)] * 5, fillvalue=None)

        top_article_list = Blog.objects.filter(
            status=1, visibility=2).select_related('p_cat')[:9]
        top_3_cats = [article.p_cat.slug for article in top_article_list][:3]
        top_cats = '+'.join(top_3_cats)

        # popular courses..
        top_blog_ids = [b.id for b in top_article_list[: 5]]
        skills = Tag.objects.prefetch_related('blog_set').filter(
            blog__id__in=top_blog_ids, is_active=True).distinct()

        skills = [sk.name for sk in skills]

        popular_courses = BlogMixin().get_product(
            top_cats, skills)

        category_url = CategoryUrl().get_category_url(popular_courses)

        country_choices, initial_country = self.get_countries()
        context.update({'country_choices': country_choices, 'initial_country': initial_country, })

        context.update({
            'authors': authors,
            'authors_list': list(author_list),
            'categories': categories,
            'popular_courses': popular_courses,
            'show_chat': True,
            'page_url' : category_url
        })

        context.update(self.get_breadcrumb_data())
        context.update(self.get_meta_details())
        return context


    def get_countries(self):
        country_choices = [(m.phone, m.name) for m in
            Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
        initial_country = Country.objects.filter(phone='91')[0].phone
        return country_choices,initial_country


    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home", "position": "1"})
        breadcrumbs.append({
            "url": reverse('talent:talent-landing'), "name": "Talent Economy", "position": "2"})
        breadcrumbs.append({"url": None, "name": "Authors", "position": "3"})
        data = {"breadcrumbs": breadcrumbs}
        return data

    def get_meta_details(self):
        meta = Meta(
            title="Career & Certification Guidance Top Authors\
            @ Shine Learning",
            description="Use experts’ advice & guidance to decide your career path.\
            Get the list of authors and related articles written by experts\
            @ Shine Learning",
        )
        return {"meta": meta}


class AuthorDetailView(DetailView):
    # template_name = "talenteconomy/author-detail-amp.html"
    model = Author

    def get_template_names(self):
        if not self.request.amp:
            return ["talenteconomy/author-detail.html"]
        return ["talenteconomy/author-detail-amp.html"]

    def get(self, request, *args, **kwargs):
        context = super(self.__class__, self).get(request, args, **kwargs)
        return context

    def get_queryset(self):
        qs = Author.objects.filter(is_active=1)
        return qs

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        if queryset is None:
            queryset = self.get_queryset()

        if slug is not None:
            queryset = queryset.filter(
                slug=slug, is_active=1,
                blog__visibility=2,
                blog__status=1).annotate(no_of_blog=Count('blog'))
        try:
            obj = queryset.get()
        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset %s' % str(e))
            raise Http404
        return obj

    def get_countries(self):
        country_choices = [(m.phone, m.name) for m in
            Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
        initial_country = Country.objects.filter(phone='91')[0].phone
        return country_choices,initial_country


    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        author = self.object

        context['meta'] = author.as_meta(self.request)
        context.update(self.get_breadcrumb_data())
        context['SITEDOMAIN'] = settings.SITE_DOMAIN

        article_list = Blog.objects.filter(
            status=1, visibility=2, author=author).order_by('-last_modified_on')
        most_recent_cat = article_list[0].p_cat.slug if article_list else ''

        # popular courses..
        top_blog_ids = [b.id for b in article_list[: 5]]
        skills = Tag.objects.prefetch_related('blog_set').filter(
            blog__id__in=top_blog_ids, is_active=True).distinct()
        skills = [sk.name for sk in skills]

        popular_courses = BlogMixin().get_product(
            most_recent_cat, skills)

        category_url = CategoryUrl().get_category_url(popular_courses)

        authors = Author.objects.filter(
            is_active=1,
            blog__visibility=2, blog__status=1).annotate(
            no_of_blog=Count('blog')).order_by('-no_of_blog').exclude(
            id=author.id)
        author_list = zip_longest(*[iter(authors)] * 5, fillvalue=None)
        country_choices, initial_country = self.get_countries()
        context.update({'country_choices': country_choices, 'initial_country': initial_country, })

        context.update({
            "author": author,
            "authors": authors,
            'authors_list': list(author_list),
            "article_list": article_list,
            "popular_courses": popular_courses,
            "amp": self.request.amp,
            "show_chat": True,
            "page_url": category_url
        })

        context.update(self.get_meta_details())

        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home", "position": "1"})
        breadcrumbs.append({
            "url": reverse('talent:talent-landing'), "name": "Talent Economy", "position": "2"})
        breadcrumbs.append({
            "url": reverse('talent:authors-listing'), "name": "Authors", "position": "3"})
        breadcrumbs.append({"url": None, "name": self.object.name, "position": "4"})
        data = {"breadcrumbs": breadcrumbs}
        return data

    def get_meta_details(self):
        auth = self.object
        desc = ''
        if auth:
            about = auth.about
            desc = '.'.join(about.split('.')[:2])
            name = auth.name
        meta = Meta(
            description=desc,
            title="%s - Career Guidance Author @ Shine Learning" %name,
        )
        return {"meta": meta}