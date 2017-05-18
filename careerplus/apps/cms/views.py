import datetime
import json

from django.views.generic import View, TemplateView
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.http import Http404
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from django.middleware.csrf import get_token

from geolocation.models import Country
from users.forms import LoginApiForm, RegistrationForm

from .models import Page, Comment
from .mixins import UploadInFile, LoadMoreMixin


class CMSPageView(TemplateView, LoadMoreMixin):
    model = Page
    template_name = "cms/cms_page.html"

    def __init__(self):
        self.page_obj = None
        self.page = 1

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        self.page = request.GET.get('page', 1)
        try:
            self.page_obj = Page.objects.get(slug=slug, is_active=True)
        except Exception:
            raise Http404
        self.page_obj.total_view += 1
        self.page_obj.save()
        today = timezone.now()
        today_date = datetime.date(day=1, month=today.month, year=today.year)
        pg_counter, created = self.page_obj.pagecounter_set.get_or_create(count_period=today_date)
        pg_counter.no_views += 1
        pg_counter.save()
        context = super(CMSPageView, self).get(request, *args, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data_dict = {"status": 0, }
            message = request.POST.get('message', '').strip()
            slug = kwargs.get('slug', None)
            try:
                self.page_obj = Page.objects.get(slug=slug, is_active=True)
            except Exception:
                raise Http404
            if request.session.get('candidate_id') and message and self.page_obj:
                Comment.objects.create(candidate_id=request.session.get('candidate_id'), message=message, page=self.page_obj)
                self.page_obj.comment_count += 1
                self.page_obj.save()
                today = timezone.now()
                today_date = datetime.date(day=1, month=today.month, year=today.year)
                pg_counter, created = self.page_obj.pagecounter_set.get_or_create(count_period=today_date)
                pg_counter.comment_count += 1
                pg_counter.save()
                data_dict['status'] = 1

            return HttpResponse(json.dumps(data_dict), content_type="application/json")
        return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(CMSPageView, self).get_context_data(**kwargs)
        page_obj = self.page_obj
        left_widgets = page_obj.pagewidget_set.filter(section='left').select_related('widget')
        right_widgets = page_obj.pagewidget_set.filter(section='right').select_related('widget')
        context['left_widgets'] = ''
        context['right_widgets'] = ''
        context['page_obj'] = page_obj
        context['page_heading'] = page_obj.name
        country_choices = [(m.id, m.phone + '-' + '(' + m.code3 + ')') for m in Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
        initial_country = Country.objects.filter(name='India', phone='91')[0].pk
        
        if self.request.session.get('candidate_id'):
            download_pop_up = "no"
        else:
            download_pop_up = "yes"

        download_docs = page_obj.document_set.filter(is_active=True)
        csrf_token_value = get_token(self.request)
        download_doc = None
        if download_docs.exists():
            download_doc = download_docs[0]
            context.update({
                'download_doc': download_doc
            })

        for left in left_widgets:
            widget_context = {}
            widget_context.update({
                'page_obj': page_obj,
                'widget': left.widget,
                'download_doc': download_doc,
                'csrf_token_value': csrf_token_value,
                'download_pop_up': download_pop_up,
                'country_choices': country_choices,
                'initial_country': initial_country,
            })
            widget_context.update(left.widget.get_widget_data())
            context['left_widgets'] += render_to_string('include/' + left.widget.get_template(), widget_context)

        for right in right_widgets:
            widget_context = {}
            widget_context.update({
                'page_obj': page_obj,
                'widget': right.widget,
                'download_doc': download_doc,
                'csrf_token_value': csrf_token_value,
                'download_pop_up': download_pop_up,
                'country_choices': country_choices,
                'initial_country': initial_country,
            })
            widget_context.update(right.widget.get_widget_data())
            context['right_widgets'] += render_to_string('include/' + right.widget.get_template(), widget_context)

        comments = page_obj.comment_set.filter(is_published=True, is_removed=False)
        context['comment_listing'] = self.pagination_method(page=self.page, comment_list=comments, page_obj=self.page_obj)
        context['total_comment'] = comments.count()
        context.update({
            "hostname": settings.SITE_DOMAIN,
            'country_choices': country_choices,
            'initial_country': initial_country,
        })
        context.update({
            "loginform": LoginApiForm(),
            "registerform": RegistrationForm()
        })
        context['meta'] = page_obj.as_meta(self.request)
        # if self.request.user.is_authenticated():
        #   comment_mod = page_obj.comment_set.filter(created_by=self.request.user,
        #       is_published=False, is_removed=False)

        #   if comment_mod.exists():
        #       under_mod = True
        #   else:
        #       under_mod = False

        #   context.update({'under_mod': under_mod})

        return context


class LeadManagementView(View, UploadInFile):
    http_method_names = [u'post', ]

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data_dict = {}
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            country_code = request.POST.get('country_code', '105').strip()
            mobile = request.POST.get('mobile_number', '').strip()
            message = request.POST.get('message', '').strip()
            term_condition = request.POST.get('term_condition')
            path = request.path

            try:
                country_obj = Country.objects.get(id=country_code)
            except:
                country_obj = Country.objects.get(id='105')

            data_dict = {
                "name": name,
                "country_code": country_obj.phone,
                "mobile": mobile,
                "email": email,
                "message": message,
                "path": path,
                "term_condition": term_condition
            }
            self.write_in_file(data_dict=data_dict)
            data = {"status": 1, }
            return HttpResponse(json.dumps(data), content_type="application/json")
        return HttpResponseForbidden()


class DownloadPdfView(View, UploadInFile):
    http_method_names = [u'post', ]
    
    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        page_obj = None
        action_type = int(request.POST.get('action_type', '0'))
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        country_code = request.POST.get('country_code', '105').strip()
        mobile = request.POST.get('mobile_number', '').strip()
        message = request.POST.get('message', '').strip()
        term_condition = request.POST.get('term_condition')
        try:
            country_obj = Country.objects.get(id=country_code)
        except:
            country_obj = Country.objects.get(id='105')
        path = request.path

        if action_type == 1:
            data_dict = {
                "name": name,
                "country_code": country_obj.phone,
                "mobile": mobile,
                "email": email,
                "message": message,
                "path": path,
                "term_condition": term_condition
            }
            if mobile:
                self.write_in_file(data_dict=data_dict)

        elif action_type == 2:
            pass
            # user = request.user
            # if request.session.get('candidate_id'):
            #     data_dict = {
            #         "name": user.name,
            #         "country_code": country_code,
            #         "mobile": mobile,
            #         "email": user.email,
            #         "message": message,
            #         "term_condition": term_condition
            #     }
            #     self.write_in_file(data_dict=data_dict)

        try:
            page_obj = Page.objects.get(slug=slug, is_active=True)
        except Exception:
            raise Http404

        return HttpResponseRedirect(
            reverse('cms:page', kwargs={'slug': page_obj.slug}))