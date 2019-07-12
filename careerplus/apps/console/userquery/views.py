import json
import datetime
import logging
from io import StringIO
import csv
import mimetypes

from datetime import datetime

from django.utils import timezone
from django.views.generic import ListView, View
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from django.http import (
    HttpResponseRedirect, HttpResponseForbidden,HttpResponse)


from blog.mixins import PaginationMixin
from crmapi.models import UserQuries
from crmapi.tasks import create_lead_crm
from console.decorators import (
    Decorate,
    check_group, stop_browser_cache)


from .forms import (
    UserQueryFilterForm, UserQueryActionForm)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.CMS_GROUP_LIST]))
class CMSUserQueryView(ListView, PaginationMixin):
    context_object_name = 'cms_query_list'
    template_name = 'console/userquery/user-query-list.html'
    model = UserQuries

    def __init__(self):
        self.page = 1
        self.paginated_by = 20
        self.query = ''
        self.created = ''

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.created = request.GET.get('created', '')
        return super(CMSUserQueryView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CMSUserQueryView, self).get_context_data(**kwargs)
        paginator = Paginator(context['cms_query_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial_filter = {"created": self.created, }
        context.update({
            "messages": alert,
            "query": self.query,
            "filter_form": UserQueryFilterForm(initial_filter),
            "action_form": UserQueryActionForm(),
            "queue_name": "cms-query",
            "queue_title": "Cms Queries",
        })
        return context

    def get_queryset(self):
        queryset = super(CMSUserQueryView, self).get_queryset()
        queryset = queryset.filter(
            lead_created=False,
            inactive=False, lead_source=7)

        try:
            if self.query:
                queryset = queryset.filter(
                    Q(id__iexact=self.query) |
                    Q(name__iexact=self.query) |
                    Q(email__iexact=self.query) |
                    Q(phn_number__iexact=self.query) |
                    Q(product__iexact=self.query) |
                    Q(product_id__iexact=self.query) |
                    Q(campaign_slug__iexact=self.query))
        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset %s' % str(e))
            pass

        try:
            if self.created:
                date_range = self.created.split('-')
                start_date = date_range[0].strip()
                start_date = datetime.strptime(
                    start_date + " 00:00:00", "%d/%m/%Y %H:%M:%S")
                end_date = date_range[1].strip()
                end_date = datetime.strptime(
                    end_date + " 23:59:59", "%d/%m/%Y %H:%M:%S")
                queryset = queryset.filter(
                    created__range=[start_date, end_date])
        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset with the daterange %s' % str(e))
            pass

        return queryset.select_related('country').order_by('-modified')


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.SKILL_GROUP_LIST]))
class SkillQueryView(ListView, PaginationMixin):
    context_object_name = 'skill_query_list'
    template_name = 'console/userquery/user-query-list.html'
    model = UserQuries

    def __init__(self):
        self.page = 1
        self.paginated_by = 20
        self.query = ''
        self.created = ''

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.created = request.GET.get('created', '')
        return super(SkillQueryView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SkillQueryView, self).get_context_data(**kwargs)
        paginator = Paginator(context['skill_query_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial_filter = {"created": self.created, }
        context.update({
            "messages": alert,
            "query": self.query,
            "filter_form": UserQueryFilterForm(initial_filter),
            "action_form": UserQueryActionForm(),
            "queue_name": "skill-query",
            "queue_title": "Skill Queries",
        })
        return context

    def get_queryset(self):
        queryset = super(SkillQueryView, self).get_queryset()
        queryset = queryset.filter(
            lead_created=False,
            inactive=False, lead_source=1)

        try:
            if self.query:
                queryset = queryset.filter(
                    Q(id__iexact=self.query) |
                    Q(name__iexact=self.query) |
                    Q(email__iexact=self.query) |
                    Q(phn_number__iexact=self.query) |
                    Q(product__iexact=self.query) |
                    Q(product_id__iexact=self.query) |
                    Q(campaign_slug__iexact=self.query))
        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset %s' % str(e))
            pass

        try:
            if self.created:
                date_range = self.created.split('-')
                start_date = date_range[0].strip()
                start_date = datetime.datetime.strptime(
                    start_date + " 00:00:00", "%d/%m/%Y %H:%M:%S")
                end_date = date_range[1].strip()
                end_date = datetime.datetime.strptime(
                    end_date + " 23:59:59", "%d/%m/%Y %H:%M:%S")
                queryset = queryset.filter(
                    created__range=[start_date, end_date])
        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset within date range %s' % str(e))

            pass

        return queryset.select_related('country').order_by('-modified')


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.COURSE_GROUP_LIST]))
class CourseQueryView(ListView, PaginationMixin):
    context_object_name = 'course_query_list'
    template_name = 'console/userquery/user-query-list.html'
    model = UserQuries

    def __init__(self):
        self.page = 1
        self.paginated_by = 20
        self.query = ''
        self.created = ''

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.created = request.GET.get('created', '')
        return super(CourseQueryView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CourseQueryView, self).get_context_data(**kwargs)
        paginator = Paginator(context['course_query_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial_filter = {"created": self.created, }
        context.update({
            "messages": alert,
            "query": self.query,
            "filter_form": UserQueryFilterForm(initial_filter),
            "action_form": UserQueryActionForm(),
            "queue_name": "course-query",
            "queue_title": "Course Queries",
        })
        return context

    def get_queryset(self):
        queryset = super(CourseQueryView, self).get_queryset()
        queryset = queryset.filter(
            lead_created=False,
            inactive=False, lead_source=2)

        try:
            if self.query:
                queryset = queryset.filter(
                    Q(id__iexact=self.query) |
                    Q(name__iexact=self.query) |
                    Q(email__iexact=self.query) |
                    Q(phn_number__iexact=self.query) |
                    Q(product__iexact=self.query) |
                    Q(product_id__iexact=self.query) |
                    Q(campaign_slug__iexact=self.query))
        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset %s' % str(e))
            pass

        try:
            if self.created:
                date_range = self.created.split('-')
                start_date = date_range[0].strip()
                start_date = datetime.datetime.strptime(
                    start_date + " 00:00:00", "%d/%m/%Y %H:%M:%S")
                end_date = date_range[1].strip()
                end_date = datetime.datetime.strptime(
                    end_date + " 23:59:59", "%d/%m/%Y %H:%M:%S")
                queryset = queryset.filter(
                    created__range=[start_date, end_date])
        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset within date range %s' % str(e))
            pass

        return queryset.select_related('country').order_by('-modified')

@Decorate(stop_browser_cache())
@Decorate(check_group([settings.COURSE_GROUP_LIST]))
class HumanResourceQueryView(ListView, PaginationMixin):
    context_object_name = 'course_query_list'
    template_name = 'console/userquery/user-query-list.html'
    model = UserQuries

    def __init__(self):
        self.page = 1
        self.paginated_by = 20
        self.query = ''
        self.created = ''

    def create_csv(self,date_range,queryset):
        start_date = date_range.split('-'
                                      '')[0].strip()
        start_date = datetime.strptime(
            start_date + " 00:00:00", "%d/%m/%Y %H:%M:%S")
        end_date = date_range.split('-')[1].strip()
        end_date = datetime.strptime(
            end_date + " 23:59:59", "%d/%m/%Y %H:%M:%S")
        queryset = queryset.filter(
            created__range=[start_date, end_date])
        file_name = 'HR Leads'
        try:
            csvfile = StringIO()
            csv_writer = csv.writer(
                csvfile, delimiter=',', quotechar="'",
                quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([
             'Date','Name','Mobile','Message'
            ])

            for query in queryset:
                try:
                    csv_writer.writerow([
                        str(query.created.strftime('%d-%b-%Y')),
                        str(query.name),
                        str(query.phn_number),
                        str(query.message)
                    ])
                except Exception as e:
                    logging.getLogger('error_log').error("%s " % str(e))
                    continue
            file_name = file_name + timezone.now().date().strftime("%Y-%m-%d")
            response = HttpResponse(csvfile.getvalue(), content_type=mimetypes.guess_type('%s.csv' % file_name))
            response["Content-Disposition"] = "attachment; filename=%s.csv" % (file_name)
            return response

        except Exception as e:
            messages.add_message(self.request, messages.ERROR, str(e))
        return HttpResponseRedirect(reverse('console:product-audit-history'))

    def post(self,request, *args,**kwargs):
        date_range = self.request.POST.get('date_range','')
        queryset = self.get_queryset()
        if not date_range:
            return HttpResponseForbidden()
        return self.create_csv(date_range,queryset)



    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.created = request.GET.get('created', '')
        return super(HumanResourceQueryView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HumanResourceQueryView, self).get_context_data(**kwargs)
        paginator = Paginator(context['course_query_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial_filter = {"created": self.created, }
        context.update({
            "messages": alert,
            "query": self.query,
            "filter_form": UserQueryFilterForm(initial_filter),
            "hrqueryform": True,
            "queue_name": "Human Resource-query",
            "queue_title": "Human Resource Queries",
        })
        return context

    def get_queryset(self):
        queryset = super(HumanResourceQueryView, self).get_queryset()
        queryset = queryset.filter(
            lead_created=False,
            inactive=False, lead_source=29)

        try:
            if self.query:
                queryset = queryset.filter(
                    Q(id__iexact=self.query) |
                    Q(name__iexact=self.query) |
                    Q(email__iexact=self.query) |
                    Q(phn_number__iexact=self.query) |
                    Q(product__iexact=self.query) |
                    Q(product_id__iexact=self.query) |
                    Q(campaign_slug__iexact=self.query))
        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset %s' % str(e))
            pass

        try:
            if self.created:
                date_range = self.created.split('-')
                start_date = date_range[0].strip()
                start_date = datetime.datetime.strptime(
                    start_date + " 00:00:00", "%d/%m/%Y %H:%M:%S")
                end_date = date_range[1].strip()
                end_date = datetime.datetime.strptime(
                    end_date + " 23:59:59", "%d/%m/%Y %H:%M:%S")
                queryset = queryset.filter(
                    created__range=[start_date, end_date])
        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset within date range %s' % str(e))
            pass

        return queryset.select_related('country').order_by('-modified')


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.SERVICE_GROUP_LIST]))
class ServiceQueryView(ListView, PaginationMixin):
    context_object_name = 'service_query_list'
    template_name = 'console/userquery/user-query-list.html'
    model = UserQuries

    def __init__(self):
        self.page = 1
        self.paginated_by = 20
        self.query = ''
        self.created = ''

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.created = request.GET.get('created', '')
        return super(ServiceQueryView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ServiceQueryView, self).get_context_data(**kwargs)
        paginator = Paginator(context['service_query_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        initial_filter = {"created": self.created, }
        context.update({
            "messages": alert,
            "query": self.query,
            "filter_form": UserQueryFilterForm(initial_filter),
            "action_form": UserQueryActionForm(),
            "queue_name": "service-query",
            "queue_title": "Service Queries",
        })
        return context

    def get_queryset(self):
        queryset = super(ServiceQueryView, self).get_queryset()
        queryset = queryset.filter(
            lead_created=False,
            inactive=False, lead_source__in=[8,9])

        try:
            if self.query:
                queryset = queryset.filter(
                    Q(id__iexact=self.query) |
                    Q(name__iexact=self.query) |
                    Q(email__iexact=self.query) |
                    Q(phn_number__iexact=self.query) |
                    Q(product__iexact=self.query) |
                    Q(product_id__iexact=self.query) |
                    Q(campaign_slug__iexact=self.query))
        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset %s' % str(e))
            pass

        try:
            if self.created:
                date_range = self.created.split('-')
                start_date = date_range[0].strip()
                start_date = datetime.datetime.strptime(
                    start_date + " 00:00:00", "%d/%m/%Y %H:%M:%S")
                end_date = date_range[1].strip()
                end_date = datetime.datetime.strptime(
                    end_date + " 23:59:59", "%d/%m/%Y %H:%M:%S")
                queryset = queryset.filter(
                    created__range=[start_date, end_date])
        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset within date range %s' % str(e))
            pass

        return queryset.select_related('country').order_by('-modified')


class UserQueryActionView(View):
    def post(self, request, *args, **kwargs):
        try:
            action = int(request.POST.get('action', '0'))
        except Exception as e:
            logging.getLogger('error_log').error('unable to get action %s' % str(e))
            action = 0

        selected = request.POST.get('selected_id', '')
        selected_id = json.loads(selected)
        queue_name = request.POST.get('queue_name', '')

        if action == 1:
            try:
                query_list = UserQuries.objects.filter(
                    id__in=selected_id, lead_created=False, inactive=False).select_related('country')
                action_success = 0
                for obj in query_list:
                    flag = create_lead_crm(pk=obj.pk)
                    if flag:
                        action_success += 1
                msg = str(action_success) + ' lead created on crm out of ' + str(len(selected_id))
                messages.add_message(request, messages.SUCCESS, msg)
                if action_success != len(selected_id):
                    msg = 'Remaining leads may be already exist on the crm.'
                    messages.add_message(request, messages.SUCCESS, msg)
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
            return HttpResponseRedirect(reverse('console:userquery:' + queue_name))
        elif action == 2:
            try:
                query_list = UserQuries.objects.filter(
                    id__in=selected_id, lead_created=False, inactive=False).select_related('country')
                action_success = 0
                for obj in query_list:
                    obj.inactive = True
                    obj.save()
                    action_success += 1
                msg = str(action_success) + ' lead marked in-active out of ' + str(len(selected_id))
                messages.add_message(request, messages.SUCCESS, msg)
                if action_success != len(selected_id):
                    msg = 'Remaining leads may be already inactive in the system.'
                    messages.add_message(request, messages.SUCCESS, msg)
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
            return HttpResponseRedirect(reverse('console:userquery:' + queue_name))

        messages.add_message(request, messages.ERROR, "Select Valid Action")
        try:
            return HttpResponseRedirect(reverse('console:userquery:' + queue_name))
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
            return HttpResponseForbidden()