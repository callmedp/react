from django.conf.urls import url, include
from assessment.views import *



urlpatterns = [

url(r'^online-exam/(?P<pk>\d+)/$',VskillTestView.as_view(), name='vskill-exam'),

url(r'^practice-tests/$',AssessmentLandingPage.as_view(), name='vskill-landing'),

url(r'^practice-tests/(?P<slug>[-\w]+)/$',AssessmentCategoryPage.as_view(), name='vskill-category'),
url(r'^practice-tests/(?P<slug>[-\w]+)/sub$',AssessmentSubCategoryPage.as_view(), name='vskill-subcategory'),


url(r'^api/', include('assessment.api.urls', namespace='assessment-api')),

]