#django imports
from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse,HttpResponseRedirect

#app imports
from users.mixins import UserGroupMixin
from order.models import CustomerFeedback
from users.mixins import UserMixin


class FeedbackQueueView(UserGroupMixin, TemplateView):
    template_name = 'console/feedbackCall/feedback-queue.html'
    group_names = ['OPS_HEAD', 'WELCOME_CALL']


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
    

