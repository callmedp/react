from rest_framework.generics import ListAPIView
from shared.rest_addons.pagination import LearningCustomPagination
from .serializers import LoadMoreSerializerSolr
from django.conf import settings
from core.library.haystack.query import SQS
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser, )
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from shared.rest_addons.mixins import FieldFilterMixin
from django_filters.rest_framework import DjangoFilterBackend

from shop.models import Category, SubHeaderCategory
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import SubHeaderCategorySerializer

class LoadMoreApiView(FieldFilterMixin, ListAPIView):
    serializer_class = LoadMoreSerializerSolr
    pagination_class = LearningCustomPagination
    permission_classes = []
    authentication_classes = []

    def get_queryset(self, *args, **kwargs):
        pCtg = self.request.query_params.get('pCtg', None)
        pTF = self.request.query_params.get('pTF', 16)
        pTF_include = self.request.query_params.get('pTF_include')

        if pCtg is None:
            return []

        if pTF_include == 'true':
            return SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).filter(pCtg=pCtg, pTF=pTF)    

        return SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).filter(pCtg=pCtg).exclude(pTF=pTF)

class SkillPageAbout(APIView):
    ''' 
    api to return about section of skillpage(course detailpage)
    id : id of the skill category
    '''
    permission_classes = []
    authentication_classes = []

    def get_breadcrumb_data(self,category):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        parent = category.get_parent()
        if parent:
            breadcrumbs.append({
                "url": parent.first().get_absolute_url(), "name": parent.first().name,
            })
        breadcrumbs.append({"url": '', "name": category.name})
        return breadcrumbs

    def get(self,request,*args,**kwargs):
        id = request.GET.get('id',None)
        try:
            category = Category.objects.get(id=id)
            subheading = SubHeaderCategory.objects.filter(category=category,active=True,heading='Who should learn')
            career_outcomes = category.split_career_outcomes()
        except Category.DoesNotExist:
            return Response({'detail':'Category not found'},status=status.HTTP_404_NOT_FOUND)
        except SubHeaderCategory.DoesNotExist:
            return Response({'detail':'SubHeaderCategory not found'},status=status.HTTP_404_NOT_FOUND)
        subheading_data = SubHeaderCategorySerializer(subheading,many=True).data
        data = {
            'name':category.name +' Courses & <br/>Certifications</h1>',
            'description' : category.description,
            'subheading':subheading_data,
            'career_outcomes':career_outcomes,
            'breadcrumbs':self.get_breadcrumb_data(category),
        }
        return Response({'data':data},status=status.HTTP_200_OK) 