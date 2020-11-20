from rest_framework.generics import ListAPIView
from shared.rest_addons.pagination import LearningCustomPagination
from .serializers import LoadMoreSerializerSolr
from django.conf import settings
from django.core.cache import cache
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
from .serializers import SubHeaderCategorySerializer,ProductSerializer,IndexColumnSerializer, TestimonialSerializer
from review.models import DetailPageWidget
from homepage.models import TestimonialCategoryRelationship, Testimonial
from shop.templatetags.shop_tags import get_faq_list
import json
from shop.choices import PRODUCT_CHOICES,PRODUCT_TAG_CHOICES

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

class SkillPage(APIView):
    ''' 
    api to return skillpage(course detailpage) data
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
        # id = request.GET.get('id',None)
        id = int(kwargs.get('pk',None))
        if cache.get('skill_page_{}'.format(id), None):
            data = cache.get('skill_page_{}'.format(id)) 
            return Response(data, status=status.HTTP_200_OK)
        try:
            category = Category.objects.get(id=id)
            subheadercategory = SubHeaderCategory.objects.filter(category=category, active=True, heading_choices__in=[2,3])
            career_outcomes = category.split_career_outcomes()
        except Category.DoesNotExist:
            return Response({'detail':'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        except SubHeaderCategory.DoesNotExist:
            return Response({'detail':'SubHeaderCategory not found'},\
                status=status.HTTP_404_NOT_FOUND)
        data = {}
        for heading in subheadercategory:
            heading_description = SubHeaderCategorySerializer(heading).data
            description = heading_description.get('description',None)
            heading_value = heading.heading_choice_text

            if heading.heading_choice_text == "who-should-learn":
                heading_value = "whoShouldLearn"
            elif heading.heading_choice_text == "faq":
                heading_value = "faq"
                description = get_faq_list(description)
            data.update({
                heading_value : description
            })

        testimonialcategory = Testimonial.objects.filter(testimonialcategoryrelationship__category=id,is_active=True)
        testimonialcategory_data = TestimonialSerializer(testimonialcategory,many=True).data
        explore_courses = []
        exp_cour_ids = json.loads(category.ex_cour)
        explore_courses = Category.objects.filter(id__in=exp_cour_ids).values('name','url')
        data.update({
            'name':category.name,
            'slug':category.slug,
            'about': category.description,
            'skillGainList' : career_outcomes,
            'breadcrumbs':self.get_breadcrumb_data(category),
            'testimonialCategory':testimonialcategory_data,
            'otherSkills':explore_courses,
        })

        cache.set('skill_page_{}'.format(id), data, timeout=60*60*24)
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
                d = json.loads(course.pVrs)['var_list']
                data = {
                    'src':course.pImg,
                    'url':course.pURL,
                    'name':course.pNm,
                    'rating': float(course.pARx),
                    'mode':course.pStM,
                    'providerName':course.pPvn,
                    'coursePrice':float(course.pPin),
                    'skill': course.pSkilln,
                    'about':course.pAb,
                    'title':course.pTt,
                    'slug':course.pSg,
                    'jobsAvailable':course.pNJ,
                    'tags':PRODUCT_TAG_CHOICES[course.pTg][1],
                    'brochure':json.loads(course.pUncdl[0])['brochure'] if course.pUncdl else None,
                    'highlights':json.loads(course.pUncdl[0])['highlighted_benefits'] if course.pUncdl else None,
                    }
                if len(d)!=0:
                    data.update({
                        'duration':d[0]['dur_days'], 
                        'type':d[0]['type'],  
                        'label':d[0]['label'], 
                        'level':d[0]['level'], 
                    })
                course_data.append(data)
            assesments = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).filter(pCtg=category.pk, pTF=16)
            for assessment in assesments[:self.no_of_products]:
                assessment_data = {
                    'src':assessment.pImg,
                    'url':assessment.pURL,
                    'rating__output':assessment.pARx,
                    'mode': assessment.pStM,# :product_mode_choice
                    'provider_name':assessment.pPvn if assessment.pPvn else None,
                    'price':float(assessment.pPin),
                    'about':assessment.text,
                    'test_duration':json.loads(assessment.pAsft[0])['test_duration'] if assessment.pAsft else None,
                    'number_of_questions':json.loads(assessment.pAsft[0])['number_of_questions'] if assessment.pAsft else None,
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