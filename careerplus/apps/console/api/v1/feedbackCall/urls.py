from django.conf.urls import url, include

#internal imports
from .views import FeedbackQueueView

#third party imports
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    # url(r'^customer-list/(?P<pk>\d+)/$', ProductSkillUpdateView.as_view()),
    url(r'^customer-list/$', FeedbackQueueView.as_view()),
]