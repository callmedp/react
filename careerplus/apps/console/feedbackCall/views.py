from django.views.generic import ListView
from order.models import CustomerFeedback
from django.core.paginator import Paginator
from blog.mixins import PaginationMixin
from .feedback_form import FeedbackCallAssignedForm


class FeedbackQueueView(ListView,PaginationMixin):
    context_object_name = 'object_list'
    template_name = 'console/feedbackCall/feedback-queue.html'
    queryset = CustomerFeedback.objects.all()
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 30
        self.query = ''
        self.assigned = -1
        self.last_payment_date, self.added_on = '', ''
    
    def get_context_data(self, **kwargs):
        context = super(FeedbackQueueView, self).get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        context.update({
            "action_form": FeedbackCallAssignedForm(),
            "query": self.query,
        })

        return context