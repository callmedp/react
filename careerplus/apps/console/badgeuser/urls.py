from django.conf.urls import url
from . import views

urlpatterns = [

    # partner inbox Queue
    url(r'^upload-certificate/$',
        views.UploadCertificate.as_view(),
        name='upload-certificate'),

    url(r'^upload-tasklist/$',
        views.UploadTaskListView.as_view(),
        name='upload-tasklist'),

    # url(r'^download-task/$',
    #     views.DownloadTaskView.as_view(),
    #     name='download-task'),
]