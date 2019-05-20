from django.conf.urls import url, include
from .views import AssessmentTestView



urlpatterns = [

url(r'^get-category-level-products',AssessmentTestView.as_view(), name='category-level-product'),
]