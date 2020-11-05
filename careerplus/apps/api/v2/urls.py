from django.urls import re_path ,include
from django.conf import settings

from api.views import   ShineCandidateLoginAPIView

app_name='api'
urlpatterns = [

    re_path(r'^candidate-login/', ShineCandidateLoginAPIView.as_view(),
            name='v2.api-login'),

]