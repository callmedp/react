# from django.conf.urls import url
from django.urls import re_path
from . import views

app_name = 'console'
urlpatterns = [

    # partner inbox Queue
    re_path(r'^upload-certificate/(?P<upload_type>[a-z\-]+)$',
        views.UploadCertificate.as_view(),
        name='upload-certificate'),

    re_path(r'^upload-tasklist/$',
        views.UploadTaskListView.as_view(),
        name='upload-tasklist'),

    re_path(r'^badge-user-task/$',
        views.DownloadBadgeUserView.as_view(),
        name='badge-user-task'),
]