from rest_framework.generics import (ListAPIView)
from order.models import CustomerFeedback
from console.api.v1.feedbackCall.serializers import FeedbackQueueSerializer
from shared.rest_addons.pagination import LearningCustomPagination 




class FeedbackQueueView(ListAPIView):
    queryset = CustomerFeedback.objects.filter(status=1)
    serializer_class = FeedbackQueueSerializer
    authentication_classes = ()
    permission_classes = ()
    pagination_class = LearningCustomPagination


