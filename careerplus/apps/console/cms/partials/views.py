from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from cms.api.core.mixins import PageViewMixin, CommentViewMixin
from cms.api.core.serializers import PageSerializer, CommentSerializer  
from cms.models import Page, Comment

from django.shortcuts import get_object_or_404 , redirect #render


# TODO: Check page_size param acceptance in url param - not accepting, accepting for api view
class ListPartialMixin(object):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        return Response(data={'page': serializer.data, 'partial_template': self.partial_template_name}, template_name=self.partial_template_name if request.META.get('HTTP_X_PJAX') else self.template_name)


class PageListPartial(ListPartialMixin, PageViewMixin, ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = partial_template_name = 'cms/partials/page-list-partial.html'


class CommentListPartial(ListPartialMixin, CommentViewMixin, ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = partial_template_name = 'cms/partials/comment-list-partial.html'


class PageDetailPartial(PageViewMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = partial_template_name = 'cms/partials/page-detail-partial.html'

    def get(self, request, pk):
        import pdb; pdb.set_trace()
        page = get_object_or_404(Page, pk=pk)
        serializer = PageSerializer(page)
        return Response(data={'serializer': serializer, 'page': page, 'partial_template': self.partial_template_name}, template_name=self.partial_template_name if request.META.get('HTTP_X_PJAX') else self.template_name)

    def post(self, request, pk):
        page = get_object_or_404(Page, pk=pk)
        serializer = PageSerializer(page, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'page': page, 'partial_template': self.partial_template_name})
        serializer.save()
        return redirect('console:cms:pages:page-list')


class PageAddPartial(PageViewMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = partial_template_name = 'cms/partials/page-add-partial.html'

    def get(self, request):
        serializer = PageSerializer()
        return Response(data={'serializer': serializer, 'partial_template': self.partial_template_name}, template_name=self.partial_template_name if request.META.get('HTTP_X_PJAX') else self.template_name)

    def post(self, request):
        serializer = PageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'serializer': serializer, 'partial_template': self.partial_template_name})
        serializer.save()
        return redirect('console:cms:pages:page-list')
