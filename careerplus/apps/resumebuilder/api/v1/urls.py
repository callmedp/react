from django.conf.urls import url

# internal imports
from .views import (CandidateListCreateView, CandidateRetrieveUpdateView, SkillRetrieveUpdateView, SkillListCreateView,
                    CandidateShineProfileRetrieveUpdateView,
                    CandidateExperienceListCreateView, CandidateExperienceRetrieveUpdateView,
                    CandidateEducationListCreateView,
                    CandidateEducationRetrieveUpdateView, CandidateCertificationListCreateView,
                    CandidateCertificationRetrieveUpdateView, CandidateProjectListCreateView,
                    CandidateProjectRetrieveUpdateView,
                    CandidateReferenceListCreateView, CandidateReferenceRetrieveUpdateView,
                    CandidateSocialLinkListCreateView,
                    CandidateSocialLinkRetrieveUpdateView, CandidateAchievementListCreateView,
                    CandidateAchievementRetrieveUpdateView, CandidateLanguageListCreateView,
                    CandidateLanguageRetrieveUpdateView,
                    CandidateResumePreview)
# third party imports
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^candidates/(?P<pk>.+)/$', CandidateRetrieveUpdateView.as_view()),
    url(r'^candidates/$', CandidateListCreateView.as_view()),
    url(r'^candidate/(?P<candidate_id>.+)/skills/(?P<pk>\d+)/$', SkillRetrieveUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>.+)/skills/$', SkillListCreateView.as_view()),
    url(r'^user-profile/$', CandidateShineProfileRetrieveUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>.+)/experiences/(?P<pk>\d+)/$', CandidateExperienceRetrieveUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>.+)/experiences/$', CandidateExperienceListCreateView.as_view()),
    url(r'^candidate/(?P<candidate_id>.+)/educations/(?P<pk>\d+)/$', CandidateEducationRetrieveUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>.+)/educations/$', CandidateEducationListCreateView.as_view()),
    url(r'^candidate/(?P<candidate_id>.+)/certifications/(?P<pk>\d+)/$',
        CandidateCertificationRetrieveUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>.+)/certifications/$', CandidateCertificationListCreateView.as_view()),
    url(r'^candidate/(?P<candidate_id>.+)/projects/(?P<pk>\d+)/$', CandidateProjectRetrieveUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>.+)/projects/$', CandidateProjectListCreateView.as_view()),
    url(r'^candidate/(?P<candidate_id>.+)/references/(?P<pk>\d+)/$', CandidateReferenceRetrieveUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>.+)/references/$', CandidateReferenceListCreateView.as_view()),
    url(r'^candidate/(?P<candidate_id>.+)/external-links/(?P<pk>\d+)/$',
        CandidateSocialLinkRetrieveUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>.+)/external-links/$', CandidateSocialLinkListCreateView.as_view()),
    url(r'^candidate/(?P<candidate_id>.+)/achievements/(?P<pk>\d+)/$',
        CandidateAchievementRetrieveUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>.+)/achievements/$', CandidateAchievementListCreateView.as_view()),
    url(r'^candidate/(?P<candidate_id>.+)/languages/(?P<pk>\d+)/$',
        CandidateLanguageRetrieveUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>.+)/languages/$', CandidateLanguageListCreateView.as_view()),
    url(r'^preview/(?P<candidate_id>.+)$', CandidateResumePreview.as_view()),  # (?P<pk>\d+)/

]
