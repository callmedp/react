import json
# import datetime
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
from users.mixins import UserPermissionMixin,UserGroupMixin




class UserQueryView(UserGroupMixin,UserPermissionMixin,ListView):
    
    USERQUERY_DICT = {
        'cms-leads': {'queue_name': 'cms-query', 'queue_title': 'Cms Queries', 'lead_source': {'lead_source': 7}},
        'skill-leads': {'queue_name': 'skill-query', 'queue_title': 'Skill Queries', 'lead_source': {'lead_source': 1}},
        'course-leads': {"queue_name": "course-query", "queue_title": "Course Queries",
                         'lead_source': {'lead_source': 2}},
        'human-resource-leads': {"queue_name": "human-resource-query", "queue_title": "Human Resource Queries",
                                 'lead_source': {'lead_source': 29}},
        'service-leads': {"queue_name": "service-query", "queue_title": "Service Queries",
                          'lead_source': {'lead_source__in': [8, 9]}}
    }

    USERQUERY_GROUP_PERMS_DICT = {
        'cms-leads': [settings.CMS_GROUP_LIST],
        'skill-leads': [settings.SKILL_GROUP_LIST],
        'course-leads': [settings.COURSE_GROUP_LIST],
    }

    USERQUERY_FILTER_DICT = {
        'cms-leads': 'userqueryform',
        'skill-leads': 'userqueryform',
        'course-leads': 'userqueryform',
        'service-leads': 'userqueryform',
        'human-resource-leads': '',
    }

    context_object_name = 'userquery'
    template_name = 'console/userquery/user-query-list.html'
    model = UserQuries
    paginate_by = 20
    page_kwarg = 'page'


    @property
    def group_names(self):
        query_list_name = self.kwargs.get('query_listing')
        get_group_name = self.USERQUERY_GROUP_PERMS_DICT.get(query_list_name)
        if query_list_name == 'human-resource-leads':
            return []
        return get_group_name

    @property
    def permission_to_check(self):
        query_list_name = self.kwargs.get('query_listing')
        if query_list_name == 'human-resource-leads':
            return ['Can View Hr Queries']
        return []

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.created = request.GET.get('created', '')
        self.user_query_list = self.kwargs.get('query_listing')
        return super(UserQueryView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserQueryView, self).get_context_data(**kwargs)
        if self.USERQUERY_FILTER_DICT.get(self.user_query_list):
            context.update({
            "action_form": UserQueryActionForm(),
            })
        context.update({
            "query": self.query,
            "filter_form": UserQueryFilterForm({"created": self.created,}),
            "queue_name": self.user_query_list,
            "queue_title": self.USERQUERY_DICT.get(self.user_query_list).get('queue_title'),
        })
        return context

    def get_queryset(self):
        queryset = super(UserQueryView, self).get_queryset()
        queryset = queryset.filter(
            lead_created=False,
            inactive=False)
        queryset = queryset.filter(**(self.USERQUERY_DICT.get(self.user_query_list).get('lead_source')))

        if self.query:
            queryset = queryset.filter(
                Q(id__iexact=self.query) |
                Q(name__iexact=self.query) |
                Q(email__iexact=self.query) |
                Q(phn_number__iexact=self.query) |
                Q(product__iexact=self.query) |
                Q(product_id__iexact=self.query) |
                Q(campaign_slug__iexact=self.query))

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
            logging.getLogger('error_log').error('unable to get queryset within date range %s' % str(e))
            pass

        return queryset.select_related('country').order_by('-modified')

class DownloadHrQueryView(UserPermissionMixin,View):
    permission_to_check = ['Can View Hr Queries']

    def create_csv(self, date_range, queryset):
        start_date = date_range.split('-')[0].strip()
        start_date = datetime.strptime(
            start_date + " 00:00:00", "%d/%m/%Y %H:%M:%S")
        end_date = date_range.split('-')[1].strip()
        end_date = datetime.strptime(
            end_date + " 23:59:59", "%d/%m/%Y %H:%M:%S")
        queryset = queryset.filter(
            created__range=[start_date, end_date])
        file_name = 'HR Leads'
        csvfile = StringIO()
        csv_writer = csv.writer(
            csvfile, delimiter=',', quotechar="'",
            quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([
            'Date', 'Name', 'Mobile', 'Message'
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

    def post(self, request, *args, **kwargs):
        date_range = self.request.POST.get('date_range', '')
        queue_name = self.request.POST.get('queue_name', '')

        if not date_range:
            messages.add_message(request, messages.ERROR, "Select the valid date")
            return HttpResponseRedirect(reverse('console:userquery:user-query',kwargs={'query_listing':queue_name}))
        queryset = UserQuries.objects.filter(
            lead_created=False,
            inactive=False,lead_source=29)
        return self.create_csv(date_range,queryset)


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
            return HttpResponseRedirect( reverse('console:userquery:user-query',kwargs={'query_listing':queue_name}))
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
            return HttpResponseRedirect( reverse('console:userquery:user-query',kwargs={'query_listing':queue_name}))

        messages.add_message(request, messages.ERROR, "Select Valid Action")
        try:
            return HttpResponseRedirect(reverse('console:userquery:user-query',kwargs={'query_listing':queue_name}))
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
            return HttpResponseForbidden()

