from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from cms.api.core.mixins import IndexerWidgetViewMixin, ColumnHeadingViewMixin, IndexColumnViewMixin, WidgetViewMixin,\
	PageViewMixin, PageWidgetViewMixin, DocumentViewMixin, CommentViewMixin, PageCounterViewMixin


# TODO: Will MODIFY these viewsets AFTERWARDS to limit the end point required.
class IndexerWidgetViewSet(IndexerWidgetViewMixin, ModelViewSet):
    """
        CRUD Viewset for `IndexerWidget` model.
    """

    authentication_classes = ()
    permission_classes = ()

class ColumnHeadingViewSet(ColumnHeadingViewMixin, ReadOnlyModelViewSet):
    """
        CRUD Viewset for `ColumnHeading` model.
    """

    authentication_classes = ()
    permission_classes = ()

class IndexColumnViewSet(IndexColumnViewMixin, ReadOnlyModelViewSet):
    """
        CRUD Viewset for `IndexColumn` model.
    """
    authentication_classes = ()
    permission_classes = ()


class WidgetViewSet(WidgetViewMixin, ReadOnlyModelViewSet):
    """
        CRUD Viewset for `Widget` model.
    """

    authentication_classes = ()
    permission_classes = ()

class PageViewSet(PageViewMixin, ModelViewSet):
    """
        CRUD Viewset for `Page` model.
    """
    authentication_classes = ()
    permission_classes = ()


class PageWidgetViewSet(PageWidgetViewMixin, ReadOnlyModelViewSet):
    """
        CRUD Viewset for `PageWidget` model.
    """
    authentication_classes = ()
    permission_classes = ()


class DocumentViewSet(DocumentViewMixin, ReadOnlyModelViewSet):
    """
        CRUD ViewSet for `Document` model.
    """
    authentication_classes = ()
    permission_classes = ()


class CommentViewSet(CommentViewMixin, ReadOnlyModelViewSet):
    """
        CRUD ViewSet for `Comment` model.
    """

    authentication_classes = ()
    permission_classes = ()

class PageCounterViewSet(PageCounterViewMixin, ReadOnlyModelViewSet):
    """
        CRUD ViewSet for `PageCounter` model.
    """

    authentication_classes = ()
    permission_classes = ()