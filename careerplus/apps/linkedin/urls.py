# from django.conf.urls import url
from django.urls import re_path

from .views import (
	CounsellingSubmit,
	LinkedinDraftView,
	DraftAdminView,
	DraftDownloadView,
	CounsellingForm,
    DashboardDraftDownloadView,
    ConsoleLinkedinDraftView,)

urlpatterns = [
	re_path(r'^counsellingform/(?P<order_item>[-\w]+)/$',
        CounsellingSubmit.as_view(), name='counselling-form'),

    re_path(r'^linkedin-draft/(?P<order_item>[-\w]+)/(?P<op_id>[-\w]+)/$',
        LinkedinDraftView.as_view(), name='linkedin-draft'),

    re_path(r'^linkedin-admin/linkedin/(?P<order_item>[-\w]+)/(?P<op_id>[-\w]+)/$',
        DraftAdminView.as_view(), name='oio_linkedin'),

    re_path(r'^draft-download/linkedin/(?P<order_item>[-\w]+)/(?P<op_id>[-\w]+)/$',
        DraftDownloadView.as_view(), name='linkedin-draf-download'),

    re_path(r'^counselling-form/(?P<order_item>.+)/$',
        CounsellingForm.as_view(), name='counselling_form'),
    
    re_path(r'^dashboard-draft-download/(?P<order_item>[-\w]+)/$',
        DashboardDraftDownloadView.as_view(), name='dashboard-draf-download'),

    re_path(r'^console-linkedin-draft/(?P<order_item>[-\w]+)/$',
        ConsoleLinkedinDraftView.as_view(), name='console-linkedin-draft'),
]
