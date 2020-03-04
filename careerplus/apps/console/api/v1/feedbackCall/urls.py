# from django.conf.urls import url, include
from django.urls import re_path, include

#internal imports
from .views import FeedbackQueueView,FeedbackCallsAssignUserView,CustomerFeedbackDetailView,FeedbackCategoryChoicesView,OrderItemFeedbackView,OrderItemFeedbackOperationView,SaveFeedbackIdData,FeedbackResolutionChoicesView

#third party imports
from rest_framework import routers

router = routers.DefaultRouter()
app_name = 'console'
urlpatterns = [
    # re_path(r'^customer-list/(?P<pk>\d+)/$', ProductSkillUpdateView.as_view()),
    re_path(r'^customer-list/$', FeedbackQueueView.as_view()),
    re_path(r'^assign-feedback-call/$', FeedbackCallsAssignUserView.as_view()),
    re_path(r'^feedback-detail/(?P<pk>\d+)/$', CustomerFeedbackDetailView.as_view()),
    re_path(r'^category-choices/$', FeedbackCategoryChoicesView.as_view()),
    re_path(r'^resolution-choices/$', FeedbackResolutionChoicesView.as_view()),
    re_path(r'^feedback/(?P<pk>\d+)/order-items/$', OrderItemFeedbackView.as_view()),
    re_path(r'^feedback/(?P<pk>\d+)/save-data/$', SaveFeedbackIdData.as_view()),
    re_path(r'^feedback/(?P<pk>\d+)/operations/$', OrderItemFeedbackOperationView.as_view()),
]