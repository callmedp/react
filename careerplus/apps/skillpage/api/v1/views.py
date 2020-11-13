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
from .serializers import SubHeaderCategorySerializer,ProductSerializer,IndexColumnSerializer
from review.models import DetailPageWidget

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
        return Response(data,status=status.HTTP_200_OK) 
    
class CourseComponentView(APIView):
    '''
    skillpage: course components api
    id: category id
    '''
    permission_classes = []
    authentication_classes = []
    no_of_products = 5

    def get(self, request,*args, **kwargs):
        id = request.GET.get('id',None)
        course_data = []
        assessments_data = []
        try:
            category = Category.objects.get(id=id)
            courses = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).filter(pCtg=category.pk).exclude(pTF=16)
            for course in courses[:self.no_of_products]:
                data = {
                    'label':course.pNm,
                    'src':course.pImg,
                    'url':course.pURL,
                    'name':course.pNm,
                    'rating': float(course.pARx),
                    'mode':course.pStM,
                    'provider__name':course.pPvn,
                    'courses__price':float(course.pPin),
                    'bestseller':True if course.pTg==1 else False,
                    'newly_added':True if course.pTg==2 else False,
                }
                course_data.append(data)
            assesments = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).filter(pCtg=category.pk, pTF=16)
            for assessment in assesments[:self.no_of_products]:
                assessment_data = {
                    'label':assessment.pNm,
                    'src':assessment.pImg,
                    'url':assessment.pURL,
                    'rating__output':assessment.pARx,
                    'mode': assessment.pStM,# :product_mode_choice
                    'provider_name':assessment.pPvn if assessment.pPvn else None,
                    'price':float(assessment.pPin),
                }
                assessments_data.append(assessment_data)
        except Category.DoesNotExist:
            return Response({'detail':'Category not found'},status=status.HTTP_404_NOT_FOUND)
        return_data = {
            'courses':course_data,
            'course_count':courses.count(),
            'assesments':assessments_data,
            'assesment_count':assesments.count(),
        }
        return Response(return_data,status=status.HTTP_200_OK)        

class DomainJobsView(APIView):
    '''
    returns domain jobs on skillpage as per category
    '''
    permission_classes = []
    authentication_classes = []
    no_of_products = 5

    def get(self, request,*args, **kwargs):
        id = request.GET.get('id',None)
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response({'detail':'Category not found'},status=status.HTTP_404_NOT_FOUND)
        widget_obj = DetailPageWidget.objects.filter(content_type__model='Category', listid__contains=category.pk).first()
        widget_obj_data = widget_obj.widget.iw.indexcolumn_set.filter(column=1) if widget_obj and widget_obj.widget else []
        data = IndexColumnSerializer(widget_obj_data,many=True).data
        return Response(data,status=status.HTTP_200_OK)