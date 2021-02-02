from rest_framework import routers
from . import views
from django.urls import re_path
app_name = "cms"
router = routers.SimpleRouter()

router.register(r'indexerwidget', views.IndexerWidgetViewSet)
router.register(r'columnheading', views.ColumnHeadingViewSet)
router.register(r'indexcolumn', views.IndexColumnViewSet)
router.register(r'widget', views.WidgetViewSet,base_name='Widget')
router.register(r'page', views.PageViewSet)
router.register(r'pagewidget', views.PageWidgetViewSet,base_name='PageWidget')
router.register(r'document', views.DocumentViewSet)
router.register(r'comment', views.CommentViewSet)
router.register(r'pagecounter', views.PageCounterViewSet)
# router.register(r'page-list', views.PageListViewSet)

urlpatterns = router.urls

urlpatterns += [
    re_path(r'^page-list/$',
        views.PageListViewSet.as_view(),
        name='api-page-list'),
]
