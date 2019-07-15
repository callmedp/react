from django.views.generic import TemplateView
from order.models import CustomerFeedback
from django.core.paginator import Paginator
from blog.mixins import PaginationMixin
from .feedback_form import FeedbackCallAssignedForm
from django.http import Http404
from core.api_mixin import ShineCandidateDetail
from django.views import View


class FeedbackQueueView(TemplateView):
    template_name = 'console/feedbackCall/feedback-queue.html'
    # model = CustomerFeedback
    # http_method_names = [u'get', u'post']

    # def __init__(self):
    #     self.page = 1
    #     self.paginated_by = 10
    #     self.query = ''
    #     self.assigned = -1
    #     self.last_payment_date, self.added_on = '', ''

    # def get(self, request, *args, **kwargs):
    #     self.page = request.GET.get('page', 1)
    #     self.query = request.GET.get('query', '').strip()
    #     return super(FeedbackQueueView, self).get(request, args, **kwargs)
    
    # def get_context_data(self, **kwargs):
    #     context = super(FeedbackQueueView, self).get_context_data(**kwargs)
    #     paginator = Paginator(context['object_list'], self.paginated_by)
    #     context.update(self.pagination(paginator, self.page))
    #     context.update({
    #         "action_form": FeedbackCallAssignedForm(),
    #         "query": self.query,
    #     })

    #     return context
    
    # def get_queryset(self):
    #     queryset = super(FeedbackQueueView,self).get_queryset()
    #     queryset = queryset.filter(status__in =[1,2])
    #     return queryset


class CustomerFeedbackUpdate(TemplateView):
    template_name='console/feedbackCall/feedback-call-detail.html'

#     # def get_object(self, queryset=None):
#     #     pk = self.kwargs.get('pk')
#     #     if queryset is None:
#     #         queryset = self.get_queryset()

#     #     if pk is not None:

#     #         queryset = queryset.filter(
#     #             pk=pk)
#     #     try:
#     #         obj = queryset.get()
#     #         user = self.request.user
#     #     except:
#     #         raise Http404
#     #     return obj

#     # def get_context_data(self, **kwargs):
#     #     context = super(CustomerFeedbackUpdate, self).get_context_data(**kwargs)
#     #     import ipdb ; ipdb.set_trace()
#     #     customer_details = ShineCandidateDetail().get_candidate_detail(shine_id=context['object'].candidate_id)
#     #     if len(customer_details['personal_detail']) > 0:
#     #         customer_name = customer_details['personal_detail'][0]['first_name'] + customer_details['personal_detail'][0]['last_name']
#     #         mobile = customer_details['personal_detail'][0]['cell_phone']
#     #         email = customer_details['personal_detail'][0]['email']
#     #         context.update({
#     #             'customer_name':customer_name,
#     #             'email':email,
#     #             'mobile':mobile
#     #         })

#     #     return context

