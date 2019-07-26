from django.views.generic import TemplateView
from users.mixins import UserGroupMixin
from order.models import CustomerFeedback
from users.mixins import UserMixin
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse,HttpResponseRedirect

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
            if customer_feedback.assigned_to == user or UserMixin().check_user_in_groups(user,settings.OPS_HEAD_GROUP_LIST):
                return super(CustomerFeedbackUpdate,self).get(request,*args, **kwargs)
        return HttpResponseRedirect('/console/feedbackcall/queue')
    

