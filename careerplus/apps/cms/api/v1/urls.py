from rest_framework import routers
from .views import PageViewSet, CommentViewSet

router = routers.SimpleRouter()

router.register(r'pages', PageViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = router.urls
