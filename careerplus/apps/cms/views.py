#python imports
import datetime
import json
import logging

#django imports
from django.views.generic import View, DetailView, TemplateView
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse,\
    HttpResponseForbidden, HttpResponsePermanentRedirect
from django.http import Http404
from django.utils import timezone
from django.conf import settings
from django.utils.http import urlquote
from django.db.models import Q
from django.middleware.csrf import get_token
from django.shortcuts import render

from geolocation.models import Country

#inter app imorts
from users.forms import (
    ModalLoginApiForm,
    ModalRegistrationApiForm,
    PasswordResetRequestForm,
)

#local imports
from .models import Page, Comment
from .mixins import LoadMoreMixin


#third party imports

class CMSPageView(DetailView, LoadMoreMixin):
    model = Page
    #template_name = "cms/cms_page.html"
    page_obj = None
    page = 1

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('slug')

        if queryset is None:
            queryset = self.get_queryset()

        if pk is not None:
            queryset = queryset.filter(pk=pk, is_active=True).first()
        elif slug is not None:
            queryset = queryset.filter(slug=slug, is_active=True).first()
        if not queryset:
            raise Http404
        return queryset

    def get_template_names(self):
        template_names = ["cms/" + settings.CMS_STATIC_TEMP_DICT.get(
                self.object.id, 'cms_page.html')]
        if not self.request.amp:
            return template_names
        return [x.split(".html")[0]+"-amp.html" for x in template_names]
        

    def redirect_if_necessary(self, current_path, article):
        expected_path = article.get_absolute_url()
        if expected_path != urlquote(current_path):
            return HttpResponsePermanentRedirect(expected_path)
        return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.amp and settings.CMS_STATIC_TEMP_DICT.get(self.object.id):
            template_to_render = 'mobile/cms/'+settings.CMS_STATIC_TEMP_DICT.get(self.object.id).split(".")[0] + "-amp.html"
            return render(request,template_name=template_to_render)

        self.slug = kwargs.get('slug', None)
        self.page = request.GET.get('page', 1)
        self.object = self.get_object()
        redirect = self.redirect_if_necessary(request.path, self.object)
        if redirect:
            return redirect
        self.object.total_view += 1
        self.object.save()
        today = timezone.now()
        today_date = datetime.date(day=1, month=today.month, year=today.year)
        pg_counter, created = self.object.pagecounter_set.get_or_create(count_period=today_date)
        pg_counter.no_views += 1
        pg_counter.save()
        response = super(CMSPageView, self).get(request, *args, **kwargs)
        return response

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data_dict = {"status": 0, }
            message = request.POST.get('message', '').strip()
            # slug = kwargs.get('slug', None)
            pk = kwargs.get('pk')
            try:
                self.page_obj = Page.objects.get(pk=pk, is_active=True)
            except Exception as e:
                logging.getLogger('error_log').error('unable to get page object %s'%str(e))
                raise Http404
            if request.session.get('candidate_id') and message and self.page_obj:
                name = ''
                if request.session.get('first_name'):
                    name = request.session.get('first_name')
                if request.session.get('last_name'):
                    name += ' ' + request.session.get('last_name')
                Comment.objects.create(candidate_id=request.session.get('candidate_id'), message=message, name=name, page=self.page_obj)
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
        page_obj = self.get_object()
        left_widgets = page_obj.pagewidget_set.filter(section='left', widget__is_active=True).select_related('widget')
        right_widgets = page_obj.pagewidget_set.filter(section='right', widget__is_active=True).select_related('widget')

        if self.request.amp:
            context['amp'] = self.request.amp
            left_widgets = left_widgets.filter(widget__widget_type__in=[1, 8, 5, 2])
            right_widgets = right_widgets.filter(widget__widget_type__in=[1, 8, 5, 2])

           
        context['left_widgets'] = ''
        context['right_widgets'] = ''
        context['page_obj'] = page_obj
        context['page_heading'] = page_obj.get_display_name

        country_choices = [(m.phone, m.name) for m in
                           Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
        initial_country = Country.objects.filter(phone='91')[0].phone

        download_docs = page_obj.document_set.filter(is_active=True)
        csrf_token_value = get_token(self.request)
        download_doc = None
        if download_docs.exists():
            download_doc = download_docs[0]
            context.update({
                'download_doc': download_doc
            })

        for left in left_widgets:
            if self.request.flavour == 'mobile' and left.widget.widget_type in [6, 7]:
                continue

            widget_context = {}
            widget_context.update({
                'page_obj': page_obj,
                'widget': left.widget,
                'download_doc': download_doc,
                'csrf_token_value': csrf_token_value,
                'country_choices': country_choices,
                'initial_country': initial_country,
                'wid': left.widget.id
            })

            if self.request.amp:
                widget_context['amp'] = True


            widget_context.update(left.widget.get_widget_data())
            context['left_widgets'] += render_to_string('include/' + left.widget.get_template(), widget_context, request=self.request)

        for right in right_widgets:
            if self.request.flavour == 'mobile' and right.widget.widget_type in [6, 7]:
                continue
            widget_context = {}
            widget_context.update({
                'page_obj': page_obj,
                'widget': right.widget,
                'download_doc': download_doc,
                'csrf_token_value': csrf_token_value,
                'country_choices': country_choices,
                'initial_country': initial_country,
                'request': self.request,
            })

            if self.request.amp:
                widget_context['amp'] = True


            widget_context.update(right.widget.get_widget_data())
            context['right_widgets'] += render_to_string('include/' + right.widget.get_template(), widget_context)

        comments = page_obj.comment_set.filter(is_published=True, is_removed=False)
        if self.request.amp:
            context['comment_listing'] =self.pagination_method(page=self.page, comment_list=comments, page_obj=page_obj,page_size=5)
        else:
            context['comment_listing'] =self.pagination_method(page=self.page, comment_list=comments, page_obj=page_obj)
        context['total_comment'] = comments.count()
        context.update({
            "hostname": settings.SITE_DOMAIN,
            'country_choices': country_choices,
            'initial_country': initial_country,
        })
        context['show_chat'] = True
        context.update({
            "loginform": ModalLoginApiForm(),
            "registerform": ModalRegistrationApiForm(),
            "reset_form": PasswordResetRequestForm(),
        })
        context['meta'] = page_obj.as_meta(self.request)
        year = datetime.datetime.now().year
        context.update({'year':year})

        return context

class CMSStaticView(TemplateView):
    template_name = "resignation_static.html"

    def get_template_names(self):
        static_kwarg = self.kwargs.get("static_kwarg")
        return ["cms/static_%s_page.html" % static_kwarg]

    def get_context_data(self, **kwargs):
        context = super(CMSStaticView, self).get_context_data(**kwargs)
        context.update({
            "hostname": settings.SITE_DOMAIN, })
        return context

# class LeadManagementView(View, UploadInFile):
#     http_method_names = [u'post', ]

#     def post(self, request, *args, **kwargs):
#         if request.is_ajax():
#             data_dict = {}
#             name = request.POST.get('name', '').strip()
#             email = request.POST.get('email', '').strip()
#             country_code = request.POST.get('country_code')
#             mobile = request.POST.get('mobile_number', '').strip()
#             message = request.POST.get('message_box', '').strip()
#             term_condition = request.POST.get('term_condition')
#             path = request.path

#             try:
#                 country_obj = Country.objects.get(phone=country_code)
#             except:
#                 country_obj = Country.objects.get(phone='91')

#             data_dict = {
#                 "name": name,
#                 "country": country_obj,
#                 "phn_number": mobile,
#                 "email": email,
#                 "message": message,
#                 "path": path,
#                 'lead_source': 7,
#             }
#             query_obj = UserQuries(**data_dict)
#             query_obj.save()
#             data_dict.update({
#                 'term_condition': term_condition,
#                 "country": country_obj.phone,
#             })
#             self.write_in_file(data_dict=data_dict)
#             data = {"status": 1, }
#             return HttpResponse(
#                 json.dumps(data), content_type="application/json")
#         return HttpResponseForbidden()


# class DownloadPdfView(View, UploadInFile):

#     def post(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         page_obj = None
#         try:
#             action_type = int(request.POST.get('action_type', '0'))
#         except:
#             action_type = 0
#         name = request.POST.get('name', '').strip()
#         email = request.POST.get('email', '').strip()
#         country_code = request.POST.get('country_code')
#         mobile = request.POST.get('mobile_number', '').strip()
#         message = request.POST.get('message', '').strip()
#         term_condition = request.POST.get('term_condition')
#         path = request.POST.get('path', '')
#         try:
#             country_obj = Country.objects.get(phone=country_code)
#         except:
#             country_obj = Country.objects.get(phone='91')

#         if action_type == 1:
#             data_dict = {
#                 "name": name,
#                 "country": country_obj,
#                 "phn_number": mobile,
#                 "email": email,
#                 "message": message,
#                 "path": path,
#                 'lead_source': 7,
#             }
#             if mobile:
#                 query_obj = UserQuries(**data_dict)
#                 query_obj.save()
#                 data_dict.update({
#                     'term_condition': term_condition,
#                     "country": country_obj.phone,
#                 })
#                 self.write_in_file(data_dict=data_dict)

#         elif action_type == 2:
#             if request.session.get('candidate_id'):
#                 country_code = request.session.get('country_code')
#                 try:
#                     country_obj = Country.objects.get(phone=country_code)
#                 except:
#                     country_obj = Country.objects.get(phone='91')

#                 data_dict = {
#                     "name": request.session.get('full_name'),
#                     "country": country_obj,
#                     "phn_number": request.session.get('mobile_no'),
#                     "email": request.session.get('email'),
#                     "path": path,
#                     'lead_source': 7,
#                 }
#                 query_obj = UserQuries(**data_dict)
#                 query_obj.save()
#                 data_dict.update({
#                     "country": country_obj.phone,
#                 })
#                 self.write_in_file(data_dict=data_dict)
#         try:
#             page_obj = Page.objects.get(pk=pk, is_active=True)
#         except Exception:
#             raise Http404
#         return HttpResponseRedirect(page_obj.get_absolute_url())
