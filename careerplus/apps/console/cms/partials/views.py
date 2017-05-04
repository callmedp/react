from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from cms.api.core.mixins import IndexerWidgetViewMixin, ColumnHeadingViewMixin, IndexColumnViewMixin, WidgetViewMixin,\
    PageViewMixin, PageWidgetViewMixin, CommentViewMixin, DocumentViewMixin, PageCounterViewMixin
from cms.api.core.serializers import PageSerializer, CommentSerializer  
from cms.models import Page, Comment

from django.shortcuts import get_object_or_404 , redirect #render


# TODO: Check page_size param acceptance in url param - not accepting, accepting for api view
class ListPartialMixin(object):
    renderer_classes = [TemplateHTMLRenderer]
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        return Response(data={'page': serializer.data, 'partial_template': self.partial_template_name, 'doing_partial': request.META.get('HTTP_X_PJAX')}, template_name=self.partial_template_name if request.META.get('HTTP_X_PJAX') else self.template_name)


class IndexerWidgetListPartial(ListPartialMixin, IndexerWidgetViewMixin, ListAPIView):

    template_name = partial_template_name = 'cms/partials/indexerwidget-list-partial.html'


class ColumnHeadingListPartial(ListPartialMixin, ColumnHeadingViewMixin, ListAPIView):
    template_name = partial_template_name = 'cms/partials/columnheading-list-partial.html'


class IndexColumnListPartial(ListPartialMixin, IndexColumnViewMixin, ListAPIView):
    template_name = partial_template_name = 'cms/partials/indexcolumn-list-partial.html'


class WidgetListPartial(ListPartialMixin, WidgetViewMixin, ListAPIView):
    template_name = partial_template_name = 'cms/partials/widget-list-partial.html'


class PageListPartial(ListPartialMixin, PageViewMixin, ListAPIView):
    template_name = partial_template_name = 'cms/partials/page-list-partial.html'


class PageWidgetListPartial(ListPartialMixin, PageWidgetViewMixin, ListAPIView):
    template_name = partial_template_name = 'cms/partials/pagewidget-list-partial.html'


class DocumentListPartial(ListPartialMixin, DocumentViewMixin, ListAPIView):
    template_name = partial_template_name = 'cms/partials/document-list-partial.html'


class CommentListPartial(ListPartialMixin, CommentViewMixin, ListAPIView):
    template_name = partial_template_name = 'cms/partials/comment-list-partial.html'


class PageCounterListPartial(ListPartialMixin, PageCounterViewMixin, ListAPIView):
    template_name = partial_template_name = 'cms/partials/pagecounter-list-partial.html'


class DetailPartialMixin(object):
    renderer_classes = [TemplateHTMLRenderer]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(data={'serializer': serializer, 'instance': instance, 'partial_template': self.partial_template_name}, template_name=self.partial_template_name if request.META.get('HTTP_X_PJAX') else self.template_name)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'doing_partial': request.META.get('HTTP_X_PJAX'), 'partial_template': self.partial_template_name})
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        if hasattr(self, 'success_list_redirect') and self.success_list_redirect:
            return redirect(self.success_list_redirect)
        elif hasattr(self, 'success_detail_redirect') and self.success_detail_redirect:
            return redirect(self.success_detail_redirect, pk=serializer.data.id)
        else:
            return Response(data={'serializer': 'serializer', 'doing_partial': request.META.get('HTTP_X_PJAX'), 'partial_template': self.partial_template_name}, template_name=self.partial_template_name if request.META.get('HTTP_X_PJAX') else self.template_name , status=status.HTTP_200_OK, headers=headers)

    def post(self, request, *args, **kwargs):
        return self.update(self, request, *args, **kwargs)


class IndexerWidgetDetailPartial(DetailPartialMixin, IndexerWidgetViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'cms/partials/indexerwidget-detail-partial.html'
    success_list_redirect = 'console:cms:pages:indexerwidget-list'
    success_detail_redirect = 'console:cms:pages:indexerwidget-detail'


class ColumnHeadingDetailPartial(DetailPartialMixin, ColumnHeadingViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'cms/partials/columnheading-detail-partial.html'
    success_list_redirect = 'console:cms:pages:columnheading-list'
    success_detail_redirect = 'console:cms:pages:columnheading-detail'


class IndexColumnDetailPartial(DetailPartialMixin, IndexColumnViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'cms/partials/indexcolumn-detail-partial.html'
    success_list_redirect = 'console:cms:pages:indexcolumn-list'
    success_detail_redirect = 'console:cms:pages:indexcolumn-detail'


class WidgetDetailPartial(DetailPartialMixin, WidgetViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'cms/partials/widget-detail-partial.html'
    success_list_redirect = 'console:cms:pages:widget-list'
    success_detail_redirect = 'console:cms:pages:widget-detail'


class PageDetailPartial(DetailPartialMixin, PageViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'cms/partials/page-detail-partial.html'
    success_list_redirect = 'console:cms:pages:page-list'
    success_detail_redirect = 'console:cms:pages:page-detail'


class PageWidgetDetailPartial(DetailPartialMixin, PageWidgetViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'cms/partials/pagewidget-detail-partial.html'
    success_list_redirect = 'console:cms:pages:pagewidget-list'
    success_detail_redirect = 'console:cms:pages:pagewidget-detail'


class DocumentDetailPartial(DetailPartialMixin, DocumentViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'cms/partials/document-detail-partial.html'
    success_list_redirect = 'console:cms:pages:document-list'
    success_detail_redirect = 'console:cms:pages:document-detail'


class CommentDetailPartial(DetailPartialMixin, CommentViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'cms/partials/comment-detail-partial.html'
    success_list_redirect = 'console:cms:pages:comment-list'
    success_detail_redirect = 'console:cms:pages:comment-detail'


class PageCounterDetailPartial(DetailPartialMixin, PageCounterViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'cms/partials/pagecounter-detail-partial.html'
    success_list_redirect = 'console:cms:pages:pagecounter-list'
    success_detail_redirect = 'console:cms:pages:pagecounter-detail'


class AddPartialMixin(object):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        return Response(data={'serializer': serializer, 'doing_partial': request.META.get('HTTP_X_PJAX'), 'partial_template': self.partial_template_name}, template_name=self.partial_template_name if request.META.get('HTTP_X_PJAX') else self.template_name)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'serializer': serializer, 'doing_partial': request.META.get('HTTP_X_PJAX'), 'partial_template': self.partial_template_name}, template_name=self.partial_template_name if request.META.get('HTTP_X_PJAX') else self.template_name)
        self.perform_create(serializer)
        import pdb; pdb.set_trace()
        headers = self.get_success_headers(serializer.data)
        if hasattr(self, 'success_list_redirect') and self.success_list_redirect:
            return redirect(self.success_list_redirect)
        elif hasattr(self, 'success_detail_redirect') and self.success_detail_redirect:
            return redirect(self.success_detail_redirect, pk=serializer.data.id)
        else:
            return Response(data={'serializer': 'serializer', 'doing_partial': request.META.get('HTTP_X_PJAX'), 'partial_template': self.partial_template_name}, template_name=self.partial_template_name if request.META.get('HTTP_X_PJAX') else self.template_name , status=status.HTTP_201_CREATED, headers=headers)


class IndexerWidgetAddPartial(AddPartialMixin, IndexerWidgetViewMixin, CreateAPIView):
    template_name = partial_template_name = 'cms/partials/indexerwidget-add-partial.html'
    success_list_redirect = 'console:cms:pages:indexerwidget-list'
    success_detail_redirect = 'console:cms:pages:indexerwidget-detail'


class ColumnHeadingAddPartial(AddPartialMixin, ColumnHeadingViewMixin, CreateAPIView):
    template_name = partial_template_name = 'cms/partials/columnheading-add-partial.html'
    success_list_redirect = 'console:cms:pages:columnheading-list'
    success_detail_redirect = 'console:cms:pages:columnheading-detail'


class IndexColumnAddPartial(AddPartialMixin, IndexColumnViewMixin, CreateAPIView):
    template_name = partial_template_name = 'cms/partials/indexcolumn-add-partial.html'
    success_list_redirect = 'console:cms:pages:indexcolumn-list'
    success_detail_redirect = 'console:cms:pages:indexcolumn-detail'


class WidgetAddPartial(AddPartialMixin, WidgetViewMixin, CreateAPIView):
    template_name = partial_template_name = 'cms/partials/widget-add-partial.html'
    success_list_redirect = 'console:cms:pages:widget-list'
    success_detail_redirect = 'console:cms:pages:widget-detail'


class PageAddPartial(AddPartialMixin, PageViewMixin, CreateAPIView):
    template_name = partial_template_name = 'cms/partials/page-add-partial.html'
    success_list_redirect = 'console:cms:pages:page-list'
    success_detail_redirect = 'console:cms:pages:page-detail'


class PageWidgetAddPartial(AddPartialMixin, PageWidgetViewMixin, CreateAPIView):
    template_name = partial_template_name = 'cms/partials/pagewidget-add-partial.html'
    success_list_redirect = 'console:cms:pages:pagewidget-list'
    success_detail_redirect = 'console:cms:pages:pagewidget-detail'


class DocumentAddPartial(AddPartialMixin, DocumentViewMixin, CreateAPIView):
    template_name = partial_template_name = 'cms/partials/document-add-partial.html'
    success_list_redirect = 'console:cms:pages:document-list'
    success_detail_redirect = 'console:cms:pages:document-detail'


class CommentAddPartial(AddPartialMixin, CommentViewMixin, CreateAPIView):
    template_name = partial_template_name = 'cms/partials/comment-add-partial.html'
    success_list_redirect = 'console:cms:pages:comment-list'
    success_detail_redirect = 'console:cms:pages:comment-detail'


class PageCounterAddPartial(AddPartialMixin, PageCounterViewMixin, CreateAPIView):
    template_name = partial_template_name = 'cms/partials/pagecounter-add-partial.html'
    success_list_redirect = 'console:cms:pages:pagecounter-list'
    success_detail_redirect = 'console:cms:pages:pagecounter-detail'
