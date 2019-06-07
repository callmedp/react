from django.conf.urls import url
from . import views

urlpatterns = [

    # partner inbox Queue
    url(r'^generate-autologintoken/$',
        views.GenerateAutoLoginTask.as_view(),
        name='generate-autologintoken'),

    url(r'^generate-encrypted-urls-for-mailer/$',
        views.GenerateEncryptedURLSForMailer.as_view(),
        name='generate-encrypted-urls'),

    url(r'^tasklist/$',
        views.TaskListView.as_view(),
        name='tasklist'),

    url(r'^download-task/$',
        views.DownloadTaskView.as_view(),
        name='download-task'),

    url(r'^download-product-list/$',
        views.DownloadProductListView.as_view(),
        name='download-product-list'),

    url(r'^generate-pixel-tracker/$',
        views.GeneratePixelTracker.as_view(),
        name='generate-pixel-tracker'),

]
