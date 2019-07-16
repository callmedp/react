from rest_framework.generics import (ListAPIView, CreateAPIView,RetrieveAPIView)
from django.views.generic.detail import DetailView
from rest_framework.views import APIView
from order.models import CustomerFeedback,OrderItemFeedback
from console.api.v1.feedbackCall.serializers import FeedbackQueueSerializer,CustomerFeedbackSerializer,OrderItemFeedbackSerializer
from shared.rest_addons.pagination import LearningCustomPagination 
from django.http import HttpResponse
from console.feedbackCall.choices import FEEDBACK_CATEGORY_CHOICES,FEEDBACK_RESOLUTION_CHOICES

import json



class FeedbackQueueView(ListAPIView):
    queryset = CustomerFeedback.objects.filter(status=1)
    serializer_class = FeedbackQueueSerializer
    authentication_classes = ()
    permission_classes = ()
    pagination_class = LearningCustomPagination


class FeedbackCallsAssignUserView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self,*args, **kwargs):
        feedback_ids = eval(self.request.POST.get('feedback_ids'))
        user_id =self.request.POST.get('user_id')
        CustomerFeedback.objects.filter(id__in=feedback_ids).update(assigned_to=user_id,status=2)
        return HttpResponse(json.dumps({'result':'updated'}), content_type="application/json")


class CustomerFeedbackDetailView(RetrieveAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = CustomerFeedbackSerializer
    lookup_field = 'pk'
    queryset = CustomerFeedback.objects.all()
    
    
class FeedbackCategoryResolutionChoicesView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self,*args, **kwargs):
        result = {
            'category':dict(FEEDBACK_CATEGORY_CHOICES),
            'resolution':dict(FEEDBACK_RESOLUTION_CHOICES)
        }
        return HttpResponse(json.dumps(result), content_type="application/json")


class OrderItemFeedbackView(ListAPIView):
    serializer_class = OrderItemFeedbackSerializer
    authentication_classes = ()
    permission_classes = ()
    pagination_class = LearningCustomPagination
    queryset = OrderItemFeedback.objects.all()

    def get_queryset(self,*args, **kwargs):
        queryset = super(OrderItemFeedbackView, self).get_queryset()
        id = self.kwargs.get('pk')
        queryset = queryset.filter(customer_feedback=id)
        return queryset
    
 

