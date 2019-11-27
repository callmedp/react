#python imports

#django imports
from django.conf.urls import url

# local imports
from .views import (CandidateCreateView, CandidateRetrieveUpdateView, SkillRetrieveUpdateView, SkillListCreateView,
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
                    CandidateResumePreview,ProfileEntityBulkUpdateView, InterestView,
                    OrderCustomisationListView,OrderCustomisationRUDView,ResumeImagePreviewView,
                    SuggestionApiView, EntityReorderView,PDFRefreshAPIView,FreeTrialResumeDownload,FreeTrialResumePolling)

#inter app imports

# third party imports
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^candidates/(?P<pk>.+)/$', CandidateRetrieveUpdateView.as_view()),
    url(r'^candidates/$', CandidateCreateView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/skills/(?P<pk>\d+)/$', SkillRetrieveUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/skills/$', SkillListCreateView.as_view()),
    url(r'^user-profile/$', CandidateShineProfileRetrieveUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/experiences/(?P<pk>\d+)/$', CandidateExperienceRetrieveUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/experiences/$', CandidateExperienceListCreateView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/educations/(?P<pk>\d+)/$', CandidateEducationRetrieveUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/educations/$', CandidateEducationListCreateView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/certifications/(?P<pk>\d+)/$',
        CandidateCertificationRetrieveUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/certifications/$', CandidateCertificationListCreateView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/projects/(?P<pk>\d+)/$', CandidateProjectRetrieveUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/projects/$', CandidateProjectListCreateView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/references/(?P<pk>\d+)/$', CandidateReferenceRetrieveUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/references/$', CandidateReferenceListCreateView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/external-links/(?P<pk>\d+)/$',
        CandidateSocialLinkRetrieveUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/external-links/$', CandidateSocialLinkListCreateView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/achievements/(?P<pk>\d+)/$',
        CandidateAchievementRetrieveUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/achievements/$', CandidateAchievementListCreateView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/languages/(?P<pk>\d+)/$',
        CandidateLanguageRetrieveUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/languages/$', CandidateLanguageListCreateView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/order-customisations/$',OrderCustomisationListView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/order-customisations/(?P<template_no>[0-9]+)/$',OrderCustomisationRUDView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/preview/(?P<pk>\d+)/$', CandidateResumePreview.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/image-preview/(?P<template_no>\d+)/$', ResumeImagePreviewView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/entity-reorder/(?P<template_no>\d+)/$', EntityReorderView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/bulk-update/(?P<entity_slug>[a-z\-]+)/$', ProfileEntityBulkUpdateView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/refresh-order/(?P<order_id>[0-9]+)/$', PDFRefreshAPIView.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/free-resume/template/(?P<template_no>[0-9]+)/$', FreeTrialResumeDownload.as_view()),
    url(r'^candidate/(?P<candidate_id>[0-9a-z]+)/free-resume/polling/$', FreeTrialResumePolling.as_view()),
    url(r'^interest-list/$', InterestView.as_view()),
    url(r'^suggestion/$', SuggestionApiView.as_view()),

]
