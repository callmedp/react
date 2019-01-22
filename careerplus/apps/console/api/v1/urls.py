from django.conf.urls import url, include

#internal imports
from .views import ProductSkillAddView

#third party imports
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^product-skill/add/$', ProductSkillAddView.as_view())
]