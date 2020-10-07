# from django.conf.urls import url, include
from django.urls import re_path,include
from assessment.views import *


app_name = 'assessment'
urlpatterns = [

re_path(r'^practice-tests/(?P<slug>[-\w]+)-test/$',VskillTestView.as_view(), name='vskill-exam'),

re_path(r'^practice-tests/$',AssessmentLandingPage.as_view(), name='vskill-landing'),

re_path(r'^practice-tests/(?P<slug>[-\w]+)/$',AssessmentCategoryPage.as_view(), name='vskill-category'),
re_path(r'^practice-tests/(?P<slug>[-\w]+)/sub$',AssessmentSubCategoryPage.as_view(), name='vskill-subcategory'),

re_path(r'^practice-tests/(?P<slug>[-\w]+)/result/$',AssessmentResultPage.as_view(), name='vskill-result'),

re_path(r'^api/', include('assessment.api.urls', namespace='assessment-api')),

]