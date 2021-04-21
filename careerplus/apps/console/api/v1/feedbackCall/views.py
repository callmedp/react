#rest imports
from rest_framework.generics import (ListAPIView, CreateAPIView,RetrieveAPIView)
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

#django imports
from django.views.generic import DetailView
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import get_user_model

#app imports
from order.models import CustomerFeedback,OrderItemFeedback,OrderItemFeedbackOperation
from console.api.v1.feedbackCall.serializers import FeedbackQueueSerializer,CustomerFeedbackSerializer,\
            OrderItemFeedbackSerializer,OrderItemFeedbackOperationSerializer
from shared.rest_addons.pagination import LearningCustomPagination 
from console.feedbackCall.choices import FEEDBACK_CATEGORY_CHOICES,FEEDBACK_RESOLUTION_CHOICES,\
                                            FEEDBACK_PARENT_CATEGORY_CHOICES
from shared.permissions import IsActiveUser,InFeedbackGroup,InFeedbackGroup


#python imports
from datetime import datetime,timedelta
import json,logging


User = get_user_model()



class FeedbackQueueView(ListAPIView):
    queryset = CustomerFeedback.objects.all()
    serializer_class = FeedbackQueueSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,IsActiveUser,InFeedbackGroup,)
    pagination_class = LearningCustomPagination

    def get_queryset(self):
        queryset = super(FeedbackQueueView, self).get_queryset()
        status = self.request.GET.get('status')
        feedback_type = self.request.GET.get('type') # fresh/follow-up type
        follow_up_date_range = self.request.GET.get('follow_up_date_range')
        added_on_range = self.request.GET.get('added_on_range')
        last_payment_range = self.request.GET.get('last_payment_range')
        min_ltv = self.request.GET.get('min_ltv')
        search_text = self.request.GET.get('search_text')
        category = self.request.GET.get('category')

        if status:
            queryset = queryset.filter(status=status)

        if search_text:
            queryset = queryset.filter(Q(full_name__icontains=search_text) | Q(email__icontains=search_text) | Q(mobile__icontains=search_text))
        
        if feedback_type == '1':
            queryset = queryset.filter(follow_up_date=None)
        elif feedback_type == '2':
            queryset = queryset.exclude(follow_up_date=None)

        if min_ltv:
            queryset = queryset.filter(ltv__gte = min_ltv)

        if last_payment_range:
            date_range = last_payment_range.split(' - ')
            start_date = datetime.strptime(date_range[0],'%Y-%m-%d')
            end_date = datetime.strptime(date_range[1],'%Y-%m-%d')
            queryset = queryset.filter(last_payment_date__range=(start_date,end_date+timedelta(days=1)))

        if follow_up_date_range:
            date_range = follow_up_date_range.split(' - ')
            start_date = datetime.strptime(date_range[0],'%Y-%m-%d')
            end_date = datetime.strptime(date_range[1],'%Y-%m-%d')
            queryset = queryset.filter(follow_up_date__range=(start_date,end_date+timedelta(days=1)))

        if added_on_range:
            date_range = added_on_range.split(' - ')
            start_date = datetime.strptime(date_range[0],'%Y-%m-%d')
            end_date = datetime.strptime(date_range[1],'%Y-%m-%d')
            queryset = queryset.filter(added_on__range=(start_date,end_date+timedelta(days=1)))

        if category:
            queryset = queryset.filter(category=category)

        user = self.request.user
        ops_head_group = settings.OPS_HEAD_GROUP_LIST
        feedback_call_group = settings.WELCOMECALL_GROUP_LIST
        if user.groups.filter(name__in=ops_head_group).exists() or user.is_superuser:
            user_filter = self.request.GET.get('user')
            if user_filter:
                queryset = queryset.filter(assigned_to=user_filter)
        elif user.groups.filter(name__in=feedback_call_group).exists():
            queryset = queryset.filter(assigned_to=user)
        else:
            queryset = queryset.none()

        queryset = queryset.prefetch_related('orderitemfeedback_set').order_by('-last_payment_date')

        return queryset


class FeedbackCallsAssignUserView(CreateAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,IsActiveUser,InFeedbackGroup,)

    def post(self,*args, **kwargs):
        feedback_ids = eval(self.request.POST.get('feedback_ids'))
        user_id =self.request.POST.get('user_id')
        user = User.objects.filter(id=user_id).first()

        feedbacks = CustomerFeedback.objects.filter(id__in=feedback_ids)
        for feedback in feedbacks:
            feedback.assigned_to=user
            feedback.status=2
            feedback.save()
        return HttpResponse(json.dumps({'result':'updated'}), content_type="application/json")


class CustomerFeedbackDetailView(RetrieveAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,IsActiveUser,InFeedbackGroup,)
    serializer_class = CustomerFeedbackSerializer
    lookup_field = 'pk'
    queryset = CustomerFeedback.objects.all()
    
    
class FeedbackCategoryChoicesView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,IsActiveUser,InFeedbackGroup,)

    def get(self,*args, **kwargs):
        results = []
        for parent_key,parent_text in dict(FEEDBACK_PARENT_CATEGORY_CHOICES).items():
            category_data = []
            for category_key,category_text in dict(FEEDBACK_CATEGORY_CHOICES).items():
                if category_key//100 == parent_key:
                    category_data.append({'id':category_key,'text':category_text})
            results.append({
                    'text':parent_text,
                    'children':category_data
                })
        return HttpResponse(json.dumps(results), content_type="application/json")

class FeedbackResolutionChoicesView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,IsActiveUser,InFeedbackGroup,)

    def get(self,*args, **kwargs):
        result = []
        for resolution_key,resolution_text in dict(FEEDBACK_RESOLUTION_CHOICES).items():
            result.append({'id':resolution_key,'text':resolution_text})
        return HttpResponse(json.dumps(result), content_type="application/json")


class OrderItemFeedbackView(ListAPIView):
    serializer_class = OrderItemFeedbackSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,IsActiveUser,InFeedbackGroup,)
    queryset = OrderItemFeedback.objects.all()

    def get_queryset(self,*args, **kwargs):
        queryset = super(OrderItemFeedbackView, self).get_queryset()
        id = self.kwargs.get('pk')
        queryset = queryset.filter(customer_feedback=id)
        return queryset


class OrderItemFeedbackOperationView(ListAPIView):
    queryset = OrderItemFeedbackOperation.objects.all()
    serializer_class = OrderItemFeedbackOperationSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,IsActiveUser,InFeedbackGroup,)
    pagination_class = LearningCustomPagination

    def get_queryset(self):
        queryset = super(OrderItemFeedbackOperationView, self).get_queryset()
        id = self.kwargs.get('pk')
        queryset = queryset.filter(customer_feedback=id)
        oi_type = self.request.GET.get('oi_type')
        if oi_type:
            queryset = queryset.filter(oi_type=oi_type)
        queryset = queryset.order_by('-id')
        return queryset

class SaveFeedbackIdData(CreateAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,IsActiveUser,InFeedbackGroup,)
    serializer_class = None

    def post(self,*args, **kwargs):
        feedback_id = kwargs.get('pk')
        form_data = json.loads(self.request.POST.get('form_data'))
        for value in form_data.values():
            if type(value) is dict:
                order_item_feedback = OrderItemFeedback.objects.filter(id=value.get('id')).first()
                order_item_feedback.category =value.get('category','')
                order_item_feedback.resolution =value.get('resolution','')
                order_item_feedback.comment =value.get('comment','')
                order_item_feedback.save()
        
        customer_feedback = CustomerFeedback.objects.get(id=feedback_id)
        customer_feedback.comment = form_data.get('comment','')
        customer_feedback.category = form_data.get('category','')
        customer_feedback.resolution = form_data.get('resolution','')

        if form_data['IsFollowUp']:
            customer_feedback.follow_up_date = form_data.get('follow-up')
        else:
            customer_feedback.status=3
            customer_feedback.follow_up_date = None
        customer_feedback.save()
        return HttpResponse(json.dumps({'result':'updated'}), content_type="application/json")


    
 

