from django.conf.urls import url, include

#internal imports
from .views import FeedbackQueueView,FeedbackCallsAssignUserView,CustomerFeedbackDetailView,FeedbackCategoryChoicesView,OrderItemFeedbackView,OrderItemFeedbackOperationView,SaveFeedbackIdData,FeedbackResolutionChoicesView

#third party imports
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    # url(r'^customer-list/(?P<pk>\d+)/$', ProductSkillUpdateView.as_view()),
    url(r'^customer-list/$', FeedbackQueueView.as_view()),
    url(r'^assign-feedback-call/$', FeedbackCallsAssignUserView.as_view()),
    url(r'^feedback-detail/(?P<pk>\d+)/$', CustomerFeedbackDetailView.as_view()),
    url(r'^category-choices/$', FeedbackCategoryChoicesView.as_view()),
    url(r'^resolution-choices/$', FeedbackResolutionChoicesView.as_view()),
    url(r'^feedback/(?P<pk>\d+)/order-items/$', OrderItemFeedbackView.as_view()),
    url(r'^feedback/(?P<pk>\d+)/save-data/$', SaveFeedbackIdData.as_view()),
    url(r'^feedback/(?P<pk>\d+)/operations/$', OrderItemFeedbackOperationView.as_view()),
]