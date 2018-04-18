import json
from itertools import zip_longest
        
from django.views.generic import (
    TemplateView,
    DetailView,
    View)

from django.http import HttpResponseForbidden, Http404,\
    HttpResponsePermanentRedirect, HttpResponse
from django.conf import settings
from django.utils import timezone
from meta.views import Meta
from django.db.models import Count
from django.urls import reverse

from users.forms import (
    ModalLoginApiForm,
    ModalRegistrationApiForm,
    PasswordResetRequestForm)
from blog.mixins import BlogMixin
from blog.models import Category, Blog, Author


class HRLandingView(TemplateView, BlogMixin):
    model = Blog
    template_name = "hrinsider/hrindex.html"

    def __init__(self):
        self.search = ''

    def get(self, request, *args, **kwargs):
        self.search = request.GET.get('search', '').strip()
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
            if self.search:
                article_list = Blog.objects.filter(
                    name__icontains=self.search,
                    status=1,
                    visibility=3).select_related(
                    'p_cat', 'author').order_by('-no_views')[:48]
                context.update({
                    'search': self.search})
                if not article_list.exists():
                    article_list = Blog.objects.filter(
                        status=1,
                        visibility=3).select_related(
                        'p_cat', 'author').order_by('-publish_date')[:15]
                    context.update({
                        "no_results": True})
            else:
                article_list = Blog.objects.filter(
                    status=1,
                    visibility=3).select_related(
                    'p_cat', 'author').order_by('-publish_date')[:15]

        top_article_list = Blog.objects.filter(
            status=1, visibility=3).select_related(
                'p_cat', 'author').order_by('-score')[:9]

        authors = Author.objects.filter(
            is_active=True,
            blog__visibility=3,
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

        context.update({
            "loginform": ModalLoginApiForm(),
            "registerform": ModalRegistrationApiForm(),
            "reset_form": PasswordResetRequestForm()
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


class HrConclaveLandingView(TemplateView):
    model = Blog
    template_name = "hrinsider/conclave.html"

    def __init__(self):
        pass

    def get(self, request, *args, **kwargs):
        context = super(self.__class__, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        obj = None
        today_date = timezone.now()
        conclave_type = ''
        conclaves = Blog.objects.filter(
            visibility=4, status=1,
            start_date__gte=today_date).order_by('start_date')
        if conclaves.exists():
            conclave_type = 'Upcoming'
            obj = conclaves[0]

        past_conclaves = Blog.objects.filter(
            visibility=4, status=1,
            start_date__lte=today_date).order_by('-start_date')

        if not obj and past_conclaves.exists():
            conclave_type = 'Past'
            obj = past_conclaves[0]
            past_conclaves = past_conclaves[1:7]

        speakers = []
        if obj:
            speakers = obj.speakers.filter(is_active=True)[: 5]
        past_speakers = Author.objects.prefetch_related('speakers').filter(
            is_active=True, speakers__status=1,
            speakers__visibility=4).annotate(
            count=Count('speakers')).order_by('-count')

        if self.request.flavour != 'mobile':
            past_speakers = list(zip_longest(*[iter(past_speakers)] * 6, fillvalue=None))

        context.update({
            'obj': obj,
            'conclave_type': conclave_type,
            'speakers': speakers,
            'past_speakers': past_speakers,
            'past_conclaves': past_conclaves,
        })
        context['SITEDOMAIN'] = settings.SITE_DOMAIN
        context.update(self.get_breadcrumb_data())
        context.update(self.get_meta_details())
        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": reverse('hrinsider:hr-landing'), "name": "HR Insider"})
        breadcrumbs.append({"url": None, "name": "HR Conclave"})
        data = {"breadcrumbs": breadcrumbs}
        return data

    def get_meta_details(self):
        meta = Meta(
            title="HR insider: Career Skilling for a future ready India",
            description="HR insider - The best way to choose better career options. Get experts' advice & ideas for planning your future growth @ Shine Learning",
        )
        return {"meta": meta}


class HrConclaveDetailView(DetailView):
    template_name = "hrinsider/conclave-detail.html"
    model = Blog

    def get_queryset(self):
        qs = Blog.objects.filter(status=1, visibility=4)
        return qs

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        if queryset is None:
            queryset = self.get_queryset()

        if slug is not None:
            queryset = queryset.filter(
                slug=slug, status=1, visibility=4)
        try:
            obj = queryset.get()
        except:
            raise Http404
        return obj

    def get(self, request, *args, **kwargs):
        self.obj = self.get_object()
        self.obj.no_views += 1
        self.obj.update_score()
        self.obj.save()

        context = super(self.__class__, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        obj = self.obj
        today_date = timezone.now()
        conclave_type = ''
        if obj.start_date > today_date:
            conclave_type = 'Upcoming'
        else:
            conclave_type = 'Past'

        past_conclaves = Blog.objects.filter(
            visibility=4, status=1,
            start_date__lte=today_date).exclude(
            pk=obj.pk).order_by('-start_date')
        past_conclaves = past_conclaves[0:6]

        speakers = []
        if obj:
            speakers = obj.speakers.filter(is_active=True)[: 5]

        past_speakers = Author.objects.prefetch_related('speakers').filter(
            is_active=True, speakers__status=1,
            speakers__visibility=4).annotate(
            count=Count('speakers')).order_by('-count')
        if self.request.flavour != 'mobile':
            past_speakers = list(zip_longest(*[iter(past_speakers)] * 6, fillvalue=None))

        context.update({
            'obj': obj,
            'speakers': speakers,
            'past_speakers': past_speakers,
            'conclave_type': conclave_type,
            'past_conclaves': past_conclaves
        })

        context.update(self.get_meta_details())
        context.update(self.get_breadcrumb_data())
        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": reverse('hrinsider:hr-landing'), "name": "HR Insider"})
        breadcrumbs.append({"url": reverse('hrinsider:hr-conclave'), "name": "HR Conclave"})
        breadcrumbs.append({"url": None, "name": self.obj.display_name})
        data = {"breadcrumbs": breadcrumbs}
        return data

    def get_meta_details(self):
        heading = self.obj.heading
        des = self.obj.get_description()
        meta = Meta(
            title=heading + "- HR Insider",
            description=des,
        )
        return {"meta": meta}


class HrJobFairLandingView(TemplateView):
    model = Blog
    template_name = "hrinsider/jobfair.html"

    def __init__(self):
        pass

    def get(self, request, *args, **kwargs):
        context = super(self.__class__, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        obj = None

        jobfair_type = ''
        today_date = timezone.now()
        jobfairs = Blog.objects.filter(
            visibility=5, status=1,
            start_date__gte=today_date).order_by('start_date')
        if jobfairs.exists():
            obj = jobfairs[0]
            jobfair_type = 'Upcoming'

        if not obj:
            past_jobfairs = Blog.objects.filter(
                visibility=5, status=1,
                start_date__lte=today_date).order_by('-start_date')
            if past_jobfairs.exists():
                obj = past_jobfairs[0]
                jobfair_type = 'Past'

        context.update({
            'obj': obj,
            'jobfair_type': jobfair_type
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
            title="HR jobfair: Career Skilling for a future ready India",
            description="HR jobfair - The best way to choose better career options. Get experts' advice & ideas for planning your future growth @ Shine Learning",
        )
        return {"meta": meta}


class HrJobFairDetailView(DetailView):
    template_name = "hrinsider/jobfair-detail.html"
    model = Blog

    def get_queryset(self):
        qs = Blog.objects.filter(status=1, visibility=5)
        return qs

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        if queryset is None:
            queryset = self.get_queryset()

        if slug is not None:
            queryset = queryset.filter(
                slug=slug, status=1, visibility=5)
        try:
            obj = queryset.get()
        except:
            raise Http404
        return obj

    def get(self, request, *args, **kwargs):
        self.obj = self.get_object()
        self.obj.no_views += 1
        self.obj.update_score()
        self.obj.save()

        context = super(self.__class__, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        obj = self.obj
        today_date = timezone.now()

        jobfair_type = ''
        if obj.start_date > today_date:
            jobfair_type = 'Upcoming'
        else:
            jobfair_type = 'Past'

        context.update({
            'obj': obj,
            'jobfair_type': jobfair_type
        })

        context.update(self.get_meta_details())
        context.update(self.get_breadcrumb_data())
        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": reverse('hrinsider:hr-landing'), "name": "HR Insider"})
        breadcrumbs.append({"url": reverse('hrinsider:jobfair'), "name": "Job Fair"})
        breadcrumbs.append({"url": None, "name": self.obj.display_name})
        data = {"breadcrumbs": breadcrumbs}
        return data

    def get_meta_details(self):
        heading = self.obj.heading
        des = self.obj.get_description()
        meta = Meta(
            title=heading + "- HR Job Fair",
            description=des,
        )
        return {"meta": meta}