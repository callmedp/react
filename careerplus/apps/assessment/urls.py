from django.conf.urls import url, include
from assessment.views import *



urlpatterns = [

url(r'^online-exam$',VskillTestView.as_view(), name='vskill-exam'),

url(r'^practice-tests/$',AssessmentLandingPage.as_view(), name='vskill-landing'),

url(r'^practice-tests/(?P<slug>[-\w]+)/$',AssessmentCategoryPage.as_view(), name='vskill-category'),

url(r'^api/', include('assessment.api.urls', namespace='assessment-api')),

]