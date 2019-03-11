from django.conf.urls import url

# internal imports
from .views import (UserListCreateView, UserRetrieveUpdateView, SkillRetrieveUpdateView, SkillListCreateView,
                    UserShineProfileRetrieveUpdateView,
                    UserExperienceListCreateView, UserExperienceRetrieveUpdateView, UserEducationListCreateView,
                    UserEducationRetrieveUpdateView, UserCertificationListCreateView,
                    UserCertificationRetrieveUpdateView, UserProjectListCreateView, UserProjectRetrieveUpdateView,
                    UserReferenceListCreateView, UserReferenceRetrieveUpdateView, UserSocialLinkListCreateView,
                    UserSocialLinkRetrieveUpdateView, UserAchievementListCreateView, UserAchievementRetrieveUpdateView,
                    UserResumePreview)
# third party imports
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^users/(?P<pk>\d+)/$', UserRetrieveUpdateView.as_view()),
    url(r'^users/$', UserListCreateView.as_view()),
    url(r'^skills/(?P<pk>\d+)/$', SkillRetrieveUpdateView.as_view()),
    url(r'^skills/$', SkillListCreateView.as_view()),
    url(r'^user-profile/(?P<email>.+)/$', UserShineProfileRetrieveUpdateView.as_view()),
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
    url(r'^external-links/(?P<pk>\d+)/$', UserSocialLinkRetrieveUpdateView.as_view()),
    url(r'^external-links/$', UserSocialLinkListCreateView.as_view()),
    url(r'^user-achievements/(?P<pk>\d+)/$', UserAchievementRetrieveUpdateView.as_view()),
    url(r'^user-achievements/$', UserAchievementListCreateView.as_view()),
    url(r'^preview/$', UserResumePreview.as_view()),  # (?P<pk>\d+)/

]
