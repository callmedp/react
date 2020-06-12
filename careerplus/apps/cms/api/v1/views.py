from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from cms.api.core.mixins import IndexerWidgetViewMixin, ColumnHeadingViewMixin, IndexColumnViewMixin, WidgetViewMixin,\
	PageViewMixin, PageWidgetViewMixin, DocumentViewMixin, CommentViewMixin, PageCounterViewMixin


from cms.models import PageWidget,Widget


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

    def get_queryset(self):
        filter_dict = {}
        if self.request.GET.get('id'):
            filter_dict.update({'id__in': map(int,self.request.GET.get('id').split(','))})

        return Widget.objects.prefetch_related('related_article','iw').filter(**filter_dict)

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

    def get_queryset(self):
        page_id = self.request.GET.get('page_id')
        filter_dict = {}
        if page_id:
            filter_dict.update({'page__in': map(int,self.request.GET.get('page_id','').split(','))})

        return PageWidget.objects.prefetch_related('widget','page','widget__related_article',
                                                   'widget__iw').filter(
            **filter_dict).order_by('ranking')



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