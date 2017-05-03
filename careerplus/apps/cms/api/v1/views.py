from rest_framework.viewsets import ModelViewSet

from cms.api.core.mixins import PageViewMixin, CommentViewMixin  

# TODO: Will MODIFY these viewsets AFTERWARDS to limit the end point required.
class PageViewSet(PageViewMixin, ModelViewSet):
    """
        CRUD Viewset for `Page` model.
    """


class CommentViewSet(CommentViewMixin, ModelViewSet):
    """
        CRUD ViewSet for `Comment` model.
    """
