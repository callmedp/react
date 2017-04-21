from django.views.generic import (
	TemplateView,
	ListView,
	DetailView,
	View)

from django.http import HttpResponseForbidden, Http404, HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.urls import reverse
from django.conf import settings
from django.db.models import Q

from meta.views import Meta

from .mixins import BlogMixin, PaginationMixin, LoadCommentMixin
from .models import Category, Blog


class LoginToCommentView(View):
    http_method_names = [u'post', ]

    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        obj = None
        try:
        	obj = Blog.objects.get(slug=slug, status=1)
        except Exception:
            raise Http404
        user_email = request.POST.get('user_email', None)
        user_password = request.POST.get('user_password', None)
        remember_me = request.POST.get('remember_me')
        user = authenticate(username=user_email, password=user_password)
        if user is not None:
            login(request, user)

        return HttpResponseRedirect(
            reverse('blog:articles-deatil', kwargs={'slug': obj.slug}))


class BlogDetailView(DetailView, BlogMixin):
    template_name = "blog/article-detail.html"
    model = Blog

    def __init__(self):
    	self.article = None
    	self.paginated_by = 1
    	self.page = 1

    def get(self, request, *args, **kwargs):
        self.slug = kwargs.get('slug', None)
        self.page = request.GET.get('page', 1)
        self.article = self.get_object()
        try:
            self.article = Blog.objects.get(slug=self.slug, status=1)
        except Exception:
            raise Http404

        self.article.no_views += 1
        self.article.update_score()
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
        
        context['meta'] = blog.as_meta(self.request)
        context.update({
            "categories": categories,
            "pop_articles": pop_aricles,
            "recent_articles": articles[: 5],
            "tags": tags,
            "allow_comment": blog.allow_comment,
        })
        context.update(self.get_breadcrumb_data())
        context['meta'] = self.article.as_meta(self.request)
        context['SITEDOMAIN'] = settings.SITE_DOMAIN


        article_list = Blog.objects.filter(Q(slug=blog.slug) | Q(p_cat=p_cat, status=1)).order_by('-score')


        page_obj = self.scrollPagination(
        		paginated_by=self.paginated_by, page=self.page,
        		object_list=article_list)

        context.update({
        	"detail_article": render_to_string('include/detail-article-list.html',
        		{"page_obj": page_obj,
        		"slug": blog.slug, "SITEDOMAIN": settings.SITE_DOMAIN})
        })

        return context

    def get_breadcrumb_data(self):
    	breadcrumbs = []
    	breadcrumbs.append({"url": '/', "name": "Home"})
    	breadcrumbs.append({"url": reverse('blog:blog-landing'), "name": "Career Guidance"})
    	breadcrumbs.append({"url": reverse('blog:articles-by-category', kwargs={'slug': self.article.p_cat.slug}), "name": self.article.p_cat.name})
    	breadcrumbs.append({"url": None, "name": self.article.name})
    	data = {"breadcrumbs": breadcrumbs}
    	return data


class BlogCategoryListView(TemplateView, PaginationMixin):
    template_name = "blog/articles-by-category.html"

    def __init__(self):
    	self.page = 1
    	self.paginated_by = 1
    	self.cat_obj = None

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        self.page = request.GET.get('page', 1)
        try:
        	self.active_tab = int(request.GET.get('tab', 0))
        except:
        	self.active_tab = 0
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
        article_list = Blog.objects.filter(Q(sec_cat__in=[cat_obj.pk], status=1) | Q(p_cat=cat_obj, status=1))   #| Blog.objects.filter(p_cat=cat_obj, status=1)
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
		categories = Category.objects.filter(is_active=True)

		page_obj = self.scrollPagination(paginated_by=self.paginated_by,
			page=self.page, object_list=categories)

		article_list = {}
		for p in page_obj:
			top_articles = p.primary_category.filter(status=1)
			if top_articles.count() > 3:
				top_articles = top_articles[: 3]
			elif top_articles.exists():
				top_articles = top_articles

			if top_articles:
				article_list.update({
					p: list(top_articles),
				})

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
		    title="Career Guidance & Advice – Articles @ Learning.Shine",
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
        	top_articles = p.primary_category.filter(status=1)
        	if top_articles.count() > 3:
        		top_articles = top_articles[: 3]
        	elif top_articles.exists():
        		top_articles = top_articles

        if top_articles:
        	article_list.update({
        		p: list(top_articles),
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


class BlogDetailAjaxView(TemplateView, BlogMixin):
    template_name = 'include/detail-article-list.html'

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
    			self.blog = Blog.objects.get(slug=self.slug)
    		except:
    			return ''
    		return super(self.__class__, self).get(request, args, **kwargs)
    	else:
    		return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        article_list = Blog.objects.filter(Q(p_cat=self.blog.p_cat, status=1))
        # article_list = article_list.exclude(pk=self.blog.pk)
        article_list = article_list.order_by('-score')

        page_obj = self.scrollPagination(
        		paginated_by=self.paginated_by, page=self.page,
        		object_list=article_list)

        context.update({
        	"page_obj": page_obj,
        	"slug": self.blog.slug,
        	"SITEDOMAIN": settings.SITE_DOMAIN
        })
        
        return context


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

		if self.request.user.is_authenticated():
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