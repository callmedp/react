from rest_framework import routers
from . import views

router = routers.SimpleRouter()

router.register(r'indexerwidget', views.IndexerWidgetViewSet)
router.register(r'columnheading', views.ColumnHeadingViewSet)
router.register(r'indexcolumn', views.IndexColumnViewSet)
router.register(r'widget', views.WidgetViewSet)
router.register(r'page', views.PageViewSet)
router.register(r'pagewidget', views.PageWidgetViewSet)
router.register(r'document', views.DocumentViewSet)
router.register(r'comment', views.CommentViewSet)
router.register(r'pagecounter', views.PageCounterViewSet)

urlpatterns = router.urls
