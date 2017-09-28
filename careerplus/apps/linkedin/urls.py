from django.conf.urls import url

from .views import (
	CounsellingSubmit,
	LinkedinDraftView,
	DraftAdminView,
	DraftDownloadView,
	CounsellingForm)

urlpatterns = [
	url(r'^counsellingform/(?P<order_item>[-\w]+)/$',
        CounsellingSubmit.as_view(), name='counselling-form'),

    url(r'^linkedin-draft/(?P<order_item>[-\w]+)/(?P<op_id>[-\w]+)/$',
        LinkedinDraftView.as_view(), name='linkedin-draft'),

    url(r'^linkedin-admin/linkedin/(?P<order_item>[-\w]+)/(?P<op_id>[-\w]+)/$',
        DraftAdminView.as_view(), name='oio_linkedin'),

    url(r'^draft-download/linkedin/(?P<order_item>[-\w]+)/(?P<op_id>[-\w]+)/$',
        DraftDownloadView.as_view(), name='linkedin-draf-download'),

    url(r'^counselling-form/(?P<order_item>.+)/$',
        CounsellingForm.as_view(), name='counselling_form'),
]
