from django.conf.urls import url
from users.views import DownloadBoosterResume


urlpatterns = [
    url(r'^resume/download/$',
        DownloadBoosterResume.as_view(), name='download_booster_resume'),
]