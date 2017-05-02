from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated
from cms.api.core.serializers import PageSerializer, CommentSerializer  
from cms.models import Page, Comment

from django.shortcuts import get_object_or_404 #render

class PageListPartial(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cms/partials/page-list-partial.html'
    serializer_class = PageSerializer

    def get_queryset(self):
        return Page.objects.all()

    def get(self, request):
        context = {'page': self.get_queryset(), 'partial_template': 'cms/partials/page-list-partial.html'}
        return Response(context)


class PageDetailPartial(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cms/partials/page-detail-partial.html'
    serializer_class = PageSerializer

    def get_queryset(self):
        return Page.objects.all()

    def get(self, request, pk):
        page = get_object_or_404(Page, pk=pk)
        serializer = PageSerializer(page)
        return Response({'serializer': serializer, 'page': page, 'partial_template': 'cms/partials/page-detail-partial.html'})

    def post(self, request, pk):
        page = get_object_or_404(Page, pk=pk)
        serializer = PageSerializer(page, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'page': page})
        serializer.save()
        return redirect('page-list')


class PageAddPartial(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cms/partials/page-add-partial.html'
    serializer_class = PageSerializer

    def get_queryset(self):
        return Page.objects.all()

    def get(self, request):
        serializer = PageSerializer()
        return Response({'serializer': serializer, 'partial_template': 'cms/partials/page-add-partial.html'})

    def post(self, request):
        serializer = PageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        serializer.save()
        return redirect('page-list')
