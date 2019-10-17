#django imports
from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render

#app imports
from users.mixins import UserGroupMixin
from order.models import CustomerFeedback
from users.mixins import UserMixin
from scheduler.models import Scheduler
from console.schedule_tasks.tasks import generate_feedback_report

#python imports
from datetime import datetime
import logging


class FeedbackQueueView(UserGroupMixin, TemplateView):
    template_name = 'console/feedbackCall/feedback-queue.html'
    group_names = ['OPS_HEAD', 'WELCOME_CALL']


class FeedbackReportView(UserGroupMixin, TemplateView):
    template_name = 'console/feedbackCall/feedback-report.html'
    group_names = ['OPS_HEAD', ]

    def post(self,request,*args,**kwargs):
        start_date_str = self.request.POST.get('start_date')
        end_date_str = self.request.POST.get('end_date')

        if not start_date_str or not end_date_str:
            messages.add_message(self.request, messages.ERROR, "Please provide start and end date")
            return render(self.request,template_name=self.template_name)

        try:
            start_date = datetime.strptime(start_date_str,'%Y/%m/%d')
            end_date = datetime.strptime(end_date_str,'%Y/%m/%d')
        except Exception as e:
            logging.getLogger('error_log').error("Unable to parse date {}".format(e))
            messages.add_message(self.request, messages.ERROR, "Please provide start and end date") 
            return render(self.request,template_name=self.template_name)

        if start_date > end_date:
            messages.add_message(self.request, messages.ERROR, "Start Date must be smaller than End Date")
            return render(self.request,template_name=self.template_name)

        scheduler_obj = Scheduler()
        scheduler_obj.task_type = 8
        scheduler_obj.status = 3
        scheduler_obj.created_by = self.request.user
        scheduler_obj.save()

        generate_feedback_report.delay(scheduler_obj.id,start_date,end_date)
        return HttpResponseRedirect("/console/tasks/tasklist/")


class CustomerFeedbackUpdate(UserGroupMixin, TemplateView):
    template_name='console/feedbackCall/feedback-call-detail.html'
    group_names = ['OPS_HEAD', 'WELCOME_CALL']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["id"] = kwargs.get('pk')
        return context

    def get(self,request,*args, **kwargs):
        id = kwargs['pk']
        user = request.user
        customer_feedback = CustomerFeedback.objects.filter(id=id).first()
        if customer_feedback:
            if customer_feedback.assigned_to == user or user.groups.filter(name__in=settings.OPS_HEAD_GROUP_LIST).exists() or user.is_superuser:
                return super(CustomerFeedbackUpdate,self).get(request,*args, **kwargs)
        return HttpResponseRedirect('/console/feedbackcall/queue')
    

