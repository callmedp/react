from django.conf.urls import url

# internal imports
from .views import (UserListCreateView, UserRetrieveUpdateView, SkillRetrieveUpdateView, SkillListCreateView,
                    UserExperienceListCreateView, UserExperienceRetrieveUpdateView, UserEducationListCreateView,
                    UserEducationRetrieveUpdateView, UserCertificationListCreateView,
                    UserCertificationRetrieveUpdateView, UserProjectListCreateView, UserProjectRetrieveUpdateView,
                    UserReferenceListCreateView, UserReferenceRetrieveUpdateView, ExternalLinkListCreateView,
                    ExternalLinkRetrieveUpdateView)
# third party imports
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^users/(?P<pk>\d+)/$', UserRetrieveUpdateView.as_view()),
    url(r'^users/$', UserListCreateView.as_view()),
    url(r'^skills/(?P<pk>\d+)/$', SkillRetrieveUpdateView.as_view()),
    url(r'^skills/$', SkillListCreateView.as_view()),
    url(r'^user-experiences/(?P<pk>\d+)/$', UserExperienceRetrieveUpdateView.as_view()),
    url(r'^user-experiences/$', UserExperienceListCreateView.as_view()),
    url(r'^user-educations/(?P<pk>\d+)/$', UserEducationRetrieveUpdateView.as_view()),
    url(r'^user-educations/$', UserEducationListCreateView.as_view()),
    url(r'^user-certifications/(?P<pk>\d+)/$', UserCertificationRetrieveUpdateView.as_view()),
    url(r'^user-certifications/$', UserCertificationListCreateView.as_view()),
    url(r'^user-projects/(?P<pk>\d+)/$', UserProjectRetrieveUpdateView.as_view()),
    url(r'^user-projects/$', UserProjectListCreateView.as_view()),
    url(r'^user-references/(?P<pk>\d+)/$', UserReferenceRetrieveUpdateView.as_view()),
    url(r'^user-references/$', UserReferenceListCreateView.as_view()),
    url(r'^external-links/(?P<pk>\d+)/$', ExternalLinkRetrieveUpdateView.as_view()),
    url(r'^external-links/$', ExternalLinkListCreateView.as_view()),
]
