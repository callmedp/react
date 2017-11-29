import json

from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    View)

from django.http import HttpResponseForbidden, Http404,\
    HttpResponsePermanentRedirect, HttpResponse
from django.utils.http import urlquote
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.urls import reverse
from django.conf import settings

from meta.views import Meta

from shine.core import ShineCandidateDetail
from users.forms import (
    ModalLoginApiForm,
    ModalRegistrationApiForm,
    PasswordResetRequestForm
)
from users.mixins import RegistrationLoginApi

from .mixins import BlogMixin, PaginationMixin, LoadCommentMixin
from .models import Category, Blog, Tag


class LoginToCommentView(View):
    http_method_names = [u'post', ]

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = ModalLoginApiForm(request.POST)
            login_resp = {}
            if form.is_valid():
                login_dict = {}
                remember_me = request.POST.get('remember_me')
                login_dict = {}
                login_dict.update({
                    "email": self.request.POST.get('email'),
                    "password": self.request.POST.get('password')
                })

                user_exist = RegistrationLoginApi.check_email_exist(login_dict['email'])

                if user_exist.get('exists'):
                    login_resp = RegistrationLoginApi.user_login(login_dict)

                    if login_resp.get('response') == 'login_user':
                        resp_status = ShineCandidateDetail().get_status_detail(email=None, shine_id=login_resp['candidate_id'])
                        self.request.session.update(resp_status)
                        if remember_me:
                            self.request.session.set_expiry(365 * 24 * 60 * 60)  # 1 year

                    elif login_resp.get('response') == 'error_pass':
                        login_resp['error_message'] = login_resp.get("non_field_errors")[0]

                elif not user_exist.get('exists'):
                    login_resp['response'] = 'error_pass'
                    login_resp['error_message'] = "This email is not registered. Please register."
            else:
                login_resp['response'] = 'form_validation_error'
            return HttpResponse(json.dumps(login_resp), content_type="application/json")
        return HttpResponseForbidden()


class RegisterToCommentView(View):
    http_method_names = [u'post', ]

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = ModalRegistrationApiForm(request.POST)
            user_resp = {}
            if form.is_valid():
                login_dict, post_data = {}, {}
                post_data.update({
                    "email": request.POST.get('email'),
                    "raw_password": request.POST.get('raw_password'),
                    "cell_phone": request.POST.get('cell_phone'),
                    "country_code": request.POST.get('country_code'),
                    "vendor_id": settings.CP_VENDOR_ID,
                })
                user_resp = RegistrationLoginApi.user_registration(post_data)

                if user_resp['response'] == 'new_user':
                    login_dict.update({
                        "email": request.POST.get('email'),
                        "password": request.POST.get('password') if request.POST.get('password') else request.POST.get('raw_password'),
                    })
                    resp = RegistrationLoginApi.user_login(login_dict)

                    if resp['response'] == 'login_user':
                        resp_status = ShineCandidateDetail().get_status_detail(email=None, shine_id=resp['candidate_id'])
                        request.session.update(resp_status)
                        user_resp['response'] = 'login_user'

                    elif resp['response'] == 'error_pass':
                        user_resp['error_message'] = user_resp["non_field_errors"][0]
                        user_resp['response'] = 'error_pass'

                elif user_resp['response'] == 'exist_user':
                    user_resp['error_message'] = user_resp["non_field_errors"][0]

                elif user_resp['response'] == 'form_error':
                    pass
            else:
                user_resp['response'] = 'form_validation_error'
            return HttpResponse(json.dumps(user_resp), content_type="application/json")

        return HttpResponseForbidden()


class BlogDetailView(DetailView, BlogMixin):
    template_name = "blog/article-detail.html"
    model = Blog

    def __init__(self):
        self.article = None
        self.paginated_by = 1
        self.page = 1

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('slug')
        if queryset is None:
            queryset = self.get_queryset()

        if pk is not None:
            queryset = queryset.filter(pk=pk, status=1, visibility=1)
        elif slug is not None:
            queryset = queryset.filter(slug=slug, status=1, visibility=1)
        try:
            obj = queryset.get()
        except:
            raise Http404
        return obj

    def redirect_if_necessary(self, current_path, article):
        expected_path = article.get_absolute_url()
        if expected_path != urlquote(current_path):
            return HttpResponsePermanentRedirect(expected_path)
        return None

    def get(self, request, *args, **kwargs):
        self.slug = kwargs.get('slug', None)
        self.page = request.GET.get('page', 1)
        self.object = self.get_object()
        # try:
        #     self.article = Blog.objects.get(slug=self.slug, status=1)
        # except Exception:
        #     raise Http404
        self.object.no_views += 1
        self.object.save()
        self.object.update_score()
        redirect = self.redirect_if_necessary(request.path, self.object)
        if redirect:
            return redirect
        context = super(self.__class__, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        categories = Category.objects.filter(is_active=True, visibility=1)
        blog = self.object
        p_cat = blog.p_cat
        articles = p_cat.primary_category.filter(status=1, visibility=1).exclude(pk=blog.pk)
        pop_aricles = articles[: 5]
        articles = articles.order_by('-publish_date')
        
        context['meta'] = blog.as_meta(self.request)
        context.update({
            "categories": categories,
            "pop_articles": pop_aricles,
            "recent_articles": articles[: 5],
            "reset_form": PasswordResetRequestForm()
        })
        context.update(self.get_breadcrumb_data())
        context['SITEDOMAIN'] = settings.SITE_DOMAIN

        main_obj = Blog.objects.filter(slug=blog.slug, status=1, visibility=1)
        main_obj_list = list(main_obj)

        article_list = Blog.objects.filter(p_cat=p_cat, status=1, visibility=1).order_by('-publish_date') | Blog.objects.filter(sec_cat__in=[p_cat], status=1, visibility=1).order_by('-publish_date')
        article_list = article_list.exclude(pk=blog.pk)
        article_list = article_list.distinct().select_related('created_by').prefetch_related('tags')

        article_list = list(article_list)

        object_list = main_obj_list + article_list

        detail_obj = self.scrollPagination(
                paginated_by=self.paginated_by, page=self.page,
                object_list=object_list)
        
        if self.request.flavour == 'mobile':
            detail_article = render_to_string('include/detail-article-list.html',
                {"page_obj": detail_obj,
                "slug": blog.slug,
                "SITEDOMAIN": settings.SITE_DOMAIN,
                "main_article": main_obj[0]})
        else:
            detail_article = render_to_string('include/detail-article-list.html',
                {"page_obj": detail_obj,
                "slug": blog.slug, "SITEDOMAIN": settings.SITE_DOMAIN})

        context.update({
            "detail_article": detail_article,
            "main_article": main_obj[0],
        })

        context.update({
            "loginform": ModalLoginApiForm(),
            "registerform": ModalRegistrationApiForm()
        })

        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        breadcrumbs.append({"url": reverse('blog:blog-landing'), "name": "Career Guidance"})
        breadcrumbs.append({"url": reverse('articles-by-category', kwargs={'slug': self.object.p_cat.slug}), "name": self.object.p_cat.name})
        breadcrumbs.append({"url": None, "name": self.object.display_name})
        data = {"breadcrumbs": breadcrumbs}
        return data


class BlogCategoryListView(TemplateView, PaginationMixin):
    template_name = "blog/articles-by-category.html"

    def __init__(self):
        self.page = 1
        self.paginated_by = 10
        self.cat_obj = None

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        self.page = request.GET.get('page', 1)
        try:
            self.active_tab = int(request.GET.get('tab', 0))
            if self.active_tab not in [0, 1]:
                self.active_tab = 0
        except:
            self.active_tab = 0
        try:
            self.cat_obj = Category.objects.get(slug=slug, is_active=True, visibility=1)
        except Exception:
            raise Http404
        context = super(BlogCategoryListView, self).get(request, args, **kwargs)
        return context
        
    def get_context_data(self, **kwargs):
        context = super(BlogCategoryListView, self).get_context_data(**kwargs)
        cat_obj = self.cat_obj
        categories = Category.objects.filter(is_active=True, visibility=1)
        article_list = Blog.objects.filter(status=1, visibility=1)
        top_5_pop = article_list[: 5]
        article_list = article_list.order_by('-publish_date')
        top_5_recent = article_list[: 5]
        main_articles = Blog.objects.filter(p_cat=cat_obj, status=1, visibility=1) | Blog.objects.filter(sec_cat__in=[cat_obj.pk], status=1, visibility=1)
        main_articles = main_articles.order_by('-publish_date').distinct().select_related('user')

        paginator = Paginator(main_articles, self.paginated_by)
        if self.active_tab == 0:
            page_data = self.pagination(paginator, self.page)
        else:
            page_data = self.pagination(paginator, 1)
        context.update({
            "recent_page": page_data.get('page'),
            "recent_end": page_data.get('page_end'),
            "recent_middle": page_data.get('middle'),
            "recent_begin": page_data.get('begin'),
            "recent_articles": top_5_recent
        })
        main_articles = main_articles.order_by('-score', '-publish_date')
        paginator = Paginator(main_articles, self.paginated_by)
        if self.active_tab == 1:
            page_data = self.pagination(paginator, self.page)
        else:
            page_data = self.pagination(paginator, 1)
        context.update({
            "pop_page": page_data.get('page'),
            "pop_end": page_data.get('page_end'),
            "pop_middle": page_data.get('middle'),
            "pop_begin": page_data.get('begin'),
            "pop_articles": top_5_pop,
        })
        context.update({
            "category": cat_obj,
            "categories": categories,
            "active_tab": self.active_tab,
            "left_tab": 0,
            "right_tab": 1,
        })
        context.update(self.get_breadcrumb_data())
        context['meta'] = cat_obj.as_meta(self.request)
        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        breadcrumbs.append({"url": reverse('blog:blog-landing'), "name": "Career Guidance"})
        breadcrumbs.append({"url": None, "name": self.cat_obj.name})
        data = {"breadcrumbs": breadcrumbs}
        return data


class BlogTagListView(TemplateView, PaginationMixin):
    template_name = "blog/articles-by-tag.html"

    def __init__(self):
        self.page = 1
        self.paginated_by = 10
        self.tag_obj = None

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        self.page = request.GET.get('page', 1)
        try:
            self.active_tab = int(request.GET.get('tab', 0))
        except:
            self.active_tab = 0
        try:
            self.tag_obj = Tag.objects.get(slug=slug, is_active=True, visibility=1)
        except Exception:
            raise Http404
        context = super(BlogTagListView, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(BlogTagListView, self).get_context_data(**kwargs)
        tag_obj = self.tag_obj
        categories = Category.objects.filter(is_active=True, visibility=1)
        article_list = tag_obj.blog_set.filter(status=1, visibility=1)
        article_list = article_list.order_by('-publish_date')

        paginator = Paginator(article_list, self.paginated_by)
        if self.active_tab == 0:
            page_data = self.pagination(paginator, self.page)
        else:
            page_data = self.pagination(paginator, 1)
        context.update({
            "recent_page": page_data.get('page'),
            "recent_end": page_data.get('page_end'),
            "recent_middle": page_data.get('middle'),
            "recent_begin": page_data.get('begin'),
            "recent_articles": article_list[:5]
        })

        article_list = article_list.order_by('-score', '-publish_date')
        paginator = Paginator(article_list, self.paginated_by)
        if self.active_tab == 1:
            page_data = self.pagination(paginator, self.page)
        else:
            page_data = self.pagination(paginator, 1)
        context.update({
            "pop_page": page_data.get('page'),
            "pop_end": page_data.get('page_end'),
            "pop_middle": page_data.get('middle'),
            "pop_begin": page_data.get('begin'),
            "pop_articles": article_list[: 5]
        })
        context.update({
            "tag": tag_obj,
            "categories": categories,
            "active_tab": self.active_tab,
            "left_tab": 0,
            "right_tab": 1,
        })
        context.update(self.get_breadcrumb_data())
        context['meta'] = tag_obj.as_meta(self.request)
        return context
    
    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        breadcrumbs.append({"url": reverse('blog:blog-landing'), "name": "Career Guidance"})
        breadcrumbs.append({"url": None, "name": self.tag_obj.name})
        data = {"breadcrumbs": breadcrumbs}
        return data


class BlogLandingPageView(TemplateView, BlogMixin):
    model = Category
    template_name = "blog/blog-landing.html"

    def __init__(self):
        self.page = 1
        self.paginated_by = 1

    def get(self, request, *args, **kwargs):
        self.page = self.request.GET.get('page', 1)
        context = super(self.__class__, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        categories = Category.objects.filter(is_active=True, visibility=1)
        exc_cat = []
        for cat in categories:
            if not cat.primary_category.filter(status=1, visibility=1).exists():
                exc_cat.append(cat.pk)

        categories = categories.exclude(pk__in=exc_cat)

        page_obj = self.scrollPagination(paginated_by=self.paginated_by,
            page=self.page, object_list=categories)

        article_list = {}
        for p in page_obj:
            top_articles = p.primary_category.filter(status=1, visibility=1)
            if top_articles.count() > 3:
                top_articles = top_articles[: 3]
            else:
                top_articles = top_articles

            article_list.update({
                p: top_articles.select_related('p_cat', 'user'),
            })

        if self.request.flavour == 'mobile':
            article_list = render_to_string('include/top_article.html',
            {'page_obj': page_obj,
            'article_list': article_list,
            'heading': True, })
        else:
            article_list = render_to_string('include/top_article.html',
            {'page_obj': page_obj, 'article_list': article_list})
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
            title="Career Guidance & Advice - Articles @ Learning.Shine",
            description='Planning to change career - Get advice and tips for better growth. Read latest articles for interview preparation, competitive exams, government jobs, resume writing tips & other career guidance at learning.shine',
        )
        return {"meta": meta}


class BlogLandingAjaxView(ListView, BlogMixin):
    model = Category
    template_name = 'include/top_article.html'

    def __init__(self):
        self.page = 1
        self.paginated_by = 1

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.page = int(self.request.GET.get('page', 1))
            return super(self.__class__, self).get(request, args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        category_list = context['category_list']
        page_obj = self.scrollPagination(paginated_by=self.paginated_by,
            page=self.page, object_list=category_list)

        article_list = {}
        for p in page_obj:
            top_articles = p.primary_category.filter(status=1, visibility=1)
            if top_articles.count() > 3:
                top_articles = top_articles[: 3]
            elif top_articles.exists():
                top_articles = top_articles

            article_list.update({
                p: top_articles.select_related('p_cat', 'user'),
            })
        context.update({
            "page_obj": page_obj,
            "article_list": article_list

        })
        return context

    def get_queryset(self):
        queryset = super(self.__class__, self).get_queryset()
        qs = queryset.filter(is_active=True)
        return qs


class BlogDetailAjaxView(View, BlogMixin):
    # template_name = 'include/detail-article-list.html'

    def __init__(self):
        self.page = 1
        self.paginated_by = 1
        self.slug = None
        self.blog = None

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.page = self.request.GET.get('page', 1)
            self.slug = self.request.GET.get('slug')
            try:
                self.blog = Blog.objects.get(slug=self.slug, status=1, visibility=1)
                main_objs = Blog.objects.filter(slug=self.blog.slug, status=1, visibility=1)

                article_list = Blog.objects.filter(p_cat=self.blog.p_cat, status=1, visibility=1).order_by('-publish_date') | Blog.objects.filter(sec_cat__in=[self.blog.p_cat], status=1).order_by('-publish_date')
                article_list = article_list.exclude(slug=self.blog.slug)
                article_list = article_list.distinct().select_related('created_by').prefetch_related('tags')

                object_list = list(main_objs) + list(article_list)

                page_obj = self.scrollPagination(
                    paginated_by=self.paginated_by, page=self.page,
                    object_list=object_list)

                detail_article = render_to_string('include/detail-article-list.html',
                    {"page_obj": page_obj,
                    "slug": self.blog.slug,
                    "SITEDOMAIN": settings.SITE_DOMAIN,
                    "main_article": main_objs[0]})

                data = {
                    'article_detail': detail_article,
                    'url': page_obj.object_list[0].get_absolute_url(),
                }

                return HttpResponse(json.dumps(data), content_type="application/json")
            except:
                pass
        return HttpResponseForbidden()


class ShowCommentBoxView(TemplateView, LoadCommentMixin):
    template_name = 'include/comment-box.html'

    def __init__(self):
        self.art_id = None
        self.article = None
        self.paginated_by = 2
        self.page = 1

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.art_id = request.GET.get('art_id')
            try:
                self.article = Blog.objects.get(id=self.art_id)
            except:
                return ''
            return super(self.__class__, self).get(request, args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)

        comments = self.article.comment_set.filter(is_published=True, is_removed=False)
        page_obj = self.pagination_loadmore(page=self.page,
            paginated_by=self.paginated_by, comment_list=comments)

        comment_load_context = {
            "comments": page_obj,
            "page_obj": self.article,
        }

        comment_list = render_to_string('include/article-load-comment.html',
            comment_load_context)

        if self.request.session.get('candidate_id'):
            login_status = 1
        else:
            login_status = 0

        context.update({
            "article": self.article,
            "comment_list": comment_list,
            "login_status": login_status
        })
        return context


class LoadMoreCommentView(TemplateView, LoadCommentMixin):
    template_name = 'include/article-load-comment.html'

    def __init__(self):
        self.slug = None
        self.article = None
        self.paginated_by = 2
        self.page = 1

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.page = request.GET.get('page')
            self.slug = request.GET.get('slug')
            try:
                self.article = Blog.objects.get(slug=self.slug)
            except:
                return ''
            return super(self.__class__, self).get(request, args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)

        comments = self.article.comment_set.filter(is_published=True, is_removed=False)
        page_obj = self.pagination_loadmore(page=self.page,
            paginated_by=self.paginated_by, comment_list=comments)

        context.update({
            "comments": page_obj,
            "page_obj": self.article,
        })
        return context
