from django.conf.urls import url, include

#internal imports
from .views import ProductSkillAddView, SkillListView, ProductListView, ProductSkillUpdateView

#third party imports
from rest_framework import routers

router = routers.DefaultRouter()
app_name= 'console'
urlpatterns = [
    url(r'^product-skills/(?P<pk>\d+)/$', ProductSkillUpdateView.as_view()),
    url(r'^product-skills/$', ProductSkillAddView.as_view()),
    url(r'^skills/$', SkillListView.as_view()),
    url(r'^products/$', ProductListView.as_view()),
    url(r'^feedback-call/', include('console.api.v1.feedbackCall.urls', namespace='v1')),
]