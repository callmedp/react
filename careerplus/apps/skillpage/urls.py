from django.conf.urls import url

from .views import SkillPageView

urlpatterns = [
    url(r'^skill-page/$', SkillPageView.as_view(), name='skill-page'),
    
]