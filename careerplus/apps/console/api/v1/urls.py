# from django.conf.urls import url, include
from django.urls import re_path, include

#internal imports
from .views import ProductSkillAddView, SkillListView, ProductListView, ProductSkillUpdateView

#third party imports
from rest_framework import routers

router = routers.DefaultRouter()
app_name = 'console'
urlpatterns = [
    re_path(r'^product-skills/(?P<pk>\d+)/$', ProductSkillUpdateView.as_view()),
    re_path(r'^product-skills/$', ProductSkillAddView.as_view()),
    re_path(r'^skills/$', SkillListView.as_view()),
    re_path(r'^products/$', ProductListView.as_view()),
    re_path(r'^feedback-call/', include('console.api.v1.feedbackCall.urls', namespace='v1')),
]