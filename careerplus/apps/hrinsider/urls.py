from django.conf.urls import url
from django.views.generic import TemplateView

from .views import HRLandingView

urlpatterns = [
     url(r'^$', HRLandingView.as_view(), name='hr-landing'),

]


# mobile page url

urlpatterns += [
    
]