from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from console.common.mixins import ListPartialMixin, UpdatableDetailPartialMixin, AddPartialMixin
from cms.api.core.mixins import IndexerWidgetViewMixin, ColumnHeadingViewMixin, IndexColumnViewMixin, WidgetViewMixin,\
    PageViewMixin, PageWidgetViewMixin, CommentViewMixin, DocumentViewMixin, PageCounterViewMixin
from cms.api.core.serializers import PageSerializer, CommentSerializer  
from cms.models import Page, Comment


class IndexerWidgetListPartial(ListPartialMixin, IndexerWidgetViewMixin, ListAPIView):

    template_name = partial_template_name = 'console/cms/partials/indexerwidget-list-partial.html'


class ColumnHeadingListPartial(ListPartialMixin, ColumnHeadingViewMixin, ListAPIView):
    template_name = partial_template_name = 'console/cms/partials/columnheading-list-partial.html'


class IndexColumnListPartial(ListPartialMixin, IndexColumnViewMixin, ListAPIView):
    template_name = partial_template_name = 'console/cms/partials/indexcolumn-list-partial.html'


class WidgetListPartial(ListPartialMixin, WidgetViewMixin, ListAPIView):
    template_name = partial_template_name = 'console/cms/partials/widget-list-partial.html'


class PageListPartial(ListPartialMixin, PageViewMixin, ListAPIView):
    template_name = partial_template_name = 'console/cms/partials/page-list-partial.html'


class PageWidgetListPartial(ListPartialMixin, PageWidgetViewMixin, ListAPIView):
    template_name = partial_template_name = 'console/cms/partials/pagewidget-list-partial.html'


class DocumentListPartial(ListPartialMixin, DocumentViewMixin, ListAPIView):
    template_name = partial_template_name = 'console/cms/partials/document-list-partial.html'


class CommentListPartial(ListPartialMixin, CommentViewMixin, ListAPIView):
    template_name = partial_template_name = 'console/cms/partials/comment-list-partial.html'


class PageCounterListPartial(ListPartialMixin, PageCounterViewMixin, ListAPIView):
    template_name = partial_template_name = 'console/cms/partials/pagecounter-list-partial.html'


class IndexerWidgetDetailPartial(UpdatableDetailPartialMixin, IndexerWidgetViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'console/cms/partials/indexerwidget-detail-partial.html'
    success_list_redirect = 'console:cms:pages:indexerwidget-list'
    success_detail_redirect = 'console:cms:pages:indexerwidget-detail'


class ColumnHeadingDetailPartial(UpdatableDetailPartialMixin, ColumnHeadingViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'console/cms/partials/columnheading-detail-partial.html'
    success_list_redirect = 'console:cms:pages:columnheading-list'
    success_detail_redirect = 'console:cms:pages:columnheading-detail'


class IndexColumnDetailPartial(UpdatableDetailPartialMixin, IndexColumnViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'console/cms/partials/indexcolumn-detail-partial.html'
    success_list_redirect = 'console:cms:pages:indexcolumn-list'
    success_detail_redirect = 'console:cms:pages:indexcolumn-detail'


class WidgetDetailPartial(UpdatableDetailPartialMixin, WidgetViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'console/cms/partials/widget-detail-partial.html'
    success_list_redirect = 'console:cms:pages:widget-list'
    success_detail_redirect = 'console:cms:pages:widget-detail'


class PageDetailPartial(UpdatableDetailPartialMixin, PageViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'console/cms/partials/page-detail-partial.html'
    success_list_redirect = 'console:cms:pages:page-list'
    success_detail_redirect = 'console:cms:pages:page-detail'


class PageWidgetDetailPartial(UpdatableDetailPartialMixin, PageWidgetViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'console/cms/partials/pagewidget-detail-partial.html'
    success_list_redirect = 'console:cms:pages:pagewidget-list'
    success_detail_redirect = 'console:cms:pages:pagewidget-detail'


class DocumentDetailPartial(UpdatableDetailPartialMixin, DocumentViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'console/cms/partials/document-detail-partial.html'
    success_list_redirect = 'console:cms:pages:document-list'
    success_detail_redirect = 'console:cms:pages:document-detail'


class CommentDetailPartial(UpdatableDetailPartialMixin, CommentViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'console/cms/partials/comment-detail-partial.html'
    success_list_redirect = 'console:cms:pages:comment-list'
    success_detail_redirect = 'console:cms:pages:comment-detail'


class PageCounterDetailPartial(UpdatableDetailPartialMixin, PageCounterViewMixin, RetrieveUpdateAPIView):
    template_name = partial_template_name = 'console/cms/partials/pagecounter-detail-partial.html'
    success_list_redirect = 'console:cms:pages:pagecounter-list'
    success_detail_redirect = 'console:cms:pages:pagecounter-detail'


class IndexerWidgetAddPartial(AddPartialMixin, IndexerWidgetViewMixin, CreateAPIView):
    template_name = partial_template_name = 'console/cms/partials/indexerwidget-add-partial.html'
    success_list_redirect = 'console:cms:pages:indexerwidget-list'
    success_detail_redirect = 'console:cms:pages:indexerwidget-detail'


class ColumnHeadingAddPartial(AddPartialMixin, ColumnHeadingViewMixin, CreateAPIView):
    template_name = partial_template_name = 'console/cms/partials/columnheading-add-partial.html'
    success_list_redirect = 'console:cms:pages:columnheading-list'
    success_detail_redirect = 'console:cms:pages:columnheading-detail'


class IndexColumnAddPartial(AddPartialMixin, IndexColumnViewMixin, CreateAPIView):
    template_name = partial_template_name = 'console/cms/partials/indexcolumn-add-partial.html'
    success_list_redirect = 'console:cms:pages:indexcolumn-list'
    success_detail_redirect = 'console:cms:pages:indexcolumn-detail'


class WidgetAddPartial(AddPartialMixin, WidgetViewMixin, CreateAPIView):
    template_name = partial_template_name = 'console/cms/partials/widget-add-partial.html'
    success_list_redirect = 'console:cms:pages:widget-list'
    success_detail_redirect = 'console:cms:pages:widget-detail'


class PageAddPartial(AddPartialMixin, PageViewMixin, CreateAPIView):
    template_name = partial_template_name = 'console/cms/partials/page-add-partial.html'
    success_list_redirect = 'console:cms:pages:page-list'
    success_detail_redirect = 'console:cms:pages:page-detail'


class PageWidgetAddPartial(AddPartialMixin, PageWidgetViewMixin, CreateAPIView):
    template_name = partial_template_name = 'console/cms/partials/pagewidget-add-partial.html'
    success_list_redirect = 'console:cms:pages:pagewidget-list'
    success_detail_redirect = 'console:cms:pages:pagewidget-detail'


class DocumentAddPartial(AddPartialMixin, DocumentViewMixin, CreateAPIView):
    template_name = partial_template_name = 'console/cms/partials/document-add-partial.html'
    success_list_redirect = 'console:cms:pages:document-list'
    success_detail_redirect = 'console:cms:pages:document-detail'


class CommentAddPartial(AddPartialMixin, CommentViewMixin, CreateAPIView):
    template_name = partial_template_name = 'console/cms/partials/comment-add-partial.html'
    success_list_redirect = 'console:cms:pages:comment-list'
    success_detail_redirect = 'console:cms:pages:comment-detail'


class PageCounterAddPartial(AddPartialMixin, PageCounterViewMixin, CreateAPIView):
    template_name = partial_template_name = 'console/cms/partials/pagecounter-add-partial.html'
    success_list_redirect = 'console:cms:pages:pagecounter-list'
    success_detail_redirect = 'console:cms:pages:pagecounter-detail'
