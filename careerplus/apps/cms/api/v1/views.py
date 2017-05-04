from rest_framework.viewsets import ReadOnlyModelViewSet

from cms.api.core.mixins import IndexerWidgetViewMixin, ColumnHeadingViewMixin, IndexColumnViewMixin, WidgetViewMixin,\
	PageViewMixin, PageWidgetViewMixin, DocumentViewMixin, CommentViewMixin, PageCounterViewMixin


# TODO: Will MODIFY these viewsets AFTERWARDS to limit the end point required.
class IndexerWidgetViewSet(IndexerWidgetViewMixin, ReadOnlyModelViewSet):
    """
        CRUD Viewset for `IndexerWidget` model.
    """


class ColumnHeadingViewSet(ColumnHeadingViewMixin, ReadOnlyModelViewSet):
    """
        CRUD Viewset for `ColumnHeading` model.
    """


class IndexColumnViewSet(IndexColumnViewMixin, ReadOnlyModelViewSet):
    """
        CRUD Viewset for `IndexColumn` model.
    """


class WidgetViewSet(WidgetViewMixin, ReadOnlyModelViewSet):
    """
        CRUD Viewset for `Widget` model.
    """


class PageViewSet(PageViewMixin, ReadOnlyModelViewSet):
    """
        CRUD Viewset for `Page` model.
    """


class PageWidgetViewSet(PageWidgetViewMixin, ReadOnlyModelViewSet):
    """
        CRUD Viewset for `PageWidget` model.
    """


class DocumentViewSet(DocumentViewMixin, ReadOnlyModelViewSet):
    """
        CRUD ViewSet for `Document` model.
    """


class CommentViewSet(CommentViewMixin, ReadOnlyModelViewSet):
    """
        CRUD ViewSet for `Comment` model.
    """


class PageCounterViewSet(PageCounterViewMixin, ReadOnlyModelViewSet):
    """
        CRUD ViewSet for `PageCounter` model.
    """
