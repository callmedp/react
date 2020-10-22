# from django.conf.urls import url
from django.urls import re_path
from . import views
app_name = 'console'
urlpatterns = [

    # partner inbox Queue
    re_path(r'^generate-autologintoken/$',
        views.GenerateAutoLoginTask.as_view(),
        name='generate-autologintoken'),

    re_path(r'^generate-encrypted-urls-for-mailer/$',
        views.GenerateEncryptedURLSForMailer.as_view(),
        name='generate-encrypted-urls'),

    re_path(r'^tasklist/$',
        views.TaskListView.as_view(),
        name='tasklist'),

    re_path(r'^download-task/$',
        views.DownloadTaskView.as_view(),
        name='download-task'),

    re_path(r'^download-product-list/$',
        views.DownloadProductListView.as_view(),
        name='download-product-list'),

    re_path(r'^generate-pixel-tracker/$',
        views.GeneratePixelTracker.as_view(),
        name='generate-pixel-tracker'),

]
