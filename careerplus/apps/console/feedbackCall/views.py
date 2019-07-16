from django.views.generic import TemplateView

class FeedbackQueueView(TemplateView):
    template_name = 'console/feedbackCall/feedback-queue.html'


class CustomerFeedbackUpdate(TemplateView):
    template_name='console/feedbackCall/feedback-call-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["id"] = kwargs.get('pk')
        return context
    

