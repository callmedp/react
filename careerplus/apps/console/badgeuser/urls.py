from django.conf.urls import url
from . import views

app_name = 'console'
urlpatterns = [

    # partner inbox Queue
    url(r'^upload-certificate/(?P<upload_type>[a-z\-]+)$',
        views.UploadCertificate.as_view(),
        name='upload-certificate'),

    url(r'^upload-tasklist/$',
        views.UploadTaskListView.as_view(),
        name='upload-tasklist'),

    url(r'^badge-user-task/$',
        views.DownloadBadgeUserView.as_view(),
        name='badge-user-task'),
]