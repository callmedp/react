from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from cms.api.core.serializers import PageSerializer, CommentSerializer  
from cms.models import Page, Comment
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import list_route


class PageViewSet(ModelViewSet):
    """
        CRUD Viewset for `Page` model.
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer


class CommentViewSet(ModelViewSet):
    """
        CRUD ViewSet for `Comment` model.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
