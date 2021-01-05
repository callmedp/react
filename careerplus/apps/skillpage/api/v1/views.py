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
from shop.templatetags.shop_tags import get_faq_list, format_features, format_extra_features
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
        skill_id = int(kwargs.get('pk',None))
        fetch_from_cache = cache.get('skill_page_{}'.format(skill_id), None)
        if not settings.DEBUG and fetch_from_cache:
            data = fetch_from_cache
            return Response(data, status=status.HTTP_200_OK)
        data = {}
        category = Category.objects.only('id','slug','career_outcomes').filter(id=skill_id).first()
        if category:
            subheadercategory = SubHeaderCategory.objects.filter(category=category, active=True, heading_choices__in=[2,3,4])
            for heading in subheadercategory:
                heading_description = SubHeaderCategorySerializer(heading).data
                description = heading_description.get('description',None)
                heading_value = heading.heading_choice_text

                if heading.heading_choice_text == "who-should-learn":
                    heading_value = "whoShouldLearn"
                elif heading.heading_choice_text == "faq":
                    heading_value = "faqList"
                    description = get_faq_list(description)
                elif heading.heading_choice_text == 'features':
                    heading_value = "featuresList"
                    description = format_features(description)
                data.update({
                    heading_value : description
                })
            testimonialcategory = list(TestimonialCategoryRelationship.objects.filter(category=category,
                        testimonial__is_active=True).select_related('testimonial'))
            testimonial = [t.testimonial for t in testimonialcategory]
            testimonialcategory_data = TestimonialSerializer(testimonial,many=True).data
            explore_courses = []
            exp_cour_ids = json.loads(category.ex_cour)
            explore_courses = Category.objects.filter(id__in=exp_cour_ids).values('name','url')
            meta = category.as_meta()
            setattr(meta,'_keywords',None)
            setattr(meta,'_url',category.get_canonical_url())
            data.update({
                'name':category.name,
                'slug':category.slug,
                'about': category.description,
                'skillGainList' : category.split_career_outcomes(),
                'breadcrumbs':self.get_breadcrumb_data(category),
                'testimonialCategory':testimonialcategory_data,
                'otherSkills':explore_courses,
                'absolute_url': category.get_absolute_url(),
                'heading': category.heading,
                'id': category.pk,
                'meta': meta.__dict__
            })

        cache.set('skill_page_{}'.format(skill_id), data, timeout=60*60*24)
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
        category = Category.objects.only('id').filter(id=id).first()
        if category:
            courses = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).filter(pCtg=category.pk).exclude(pTF=16)
            for course in courses:
                d = json.loads(course.pVrs).get('var_list')
                data = {
                    'imgUrl':course.pImg,
                    'url':course.pURL,
                    'name':course.pNm,
                    'imgAlt':course.pImA,
                    'rating': float(course.pARx),
                    'mode':course.pStM[0] if course.pStM else None,
                    'providerName':course.pPvn,
                    'price':float(course.pPin),
                    'skillList': course.pSkilln,
                    'about':course.pAb,
                    'title':course.pTt,
                    'slug':course.pSg,
                    'jobsAvailable':course.pNJ,
                    'tags':PRODUCT_TAG_CHOICES[course.pTg][0],
                    'brochure':json.loads(course.pUncdl[0]).get('brochure') if course.pUncdl else None,
                    'u_courses_benefits':json.loads(course.pUncdl[0]).get('highlighted_benefits').split(';') if course.pUncdl else None,
                    'u_desc': course.pDsc,
                    'stars': course.pStar,
                    'highlights':format_extra_features(course.pBS) if course.pBS else None,
                    'id':course.id,
                    }
                if len(d)!=0:
                    data.update({
                        'duration':d[0].get('dur_days'), 
                        'type':d[0].get('type'),  
                        'label':d[0].get('label'), 
                        'level':d[0].get('level'), 
                    })
                course_data.append(data)
            assesments = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).filter(pCtg=category.pk, pTF=16)
            for assessment in assesments:
                assessment_data = {
                    'name':assessment.pNm,
                    'imgUrl':assessment.pImg,
                    'url':assessment.pURL,
                    'rating':assessment.pARx,
                    'mode': assessment.pStM,# :product_mode_choice
                    'providerName':assessment.pPvn if assessment.pPvn else None,
                    'price':float(assessment.pPin),
                    'about':assessment.text,
                    'tags':PRODUCT_TAG_CHOICES[assessment.pTg][1],
                    'brochure':json.loads(assessment.pUncdl[0]).get('brochure') if course.pUncdl else None,
                    'test_duration':json.loads(assessment.pAsft[0]).get('test_duration') if assessment.pAsft else None,
                    'number_of_questions':json.loads(assessment.pAsft[0]).get('number_of_questions') if assessment.pAsft else None,
                }
                assessments_data.append(assessment_data)
        return_data = {
            'courses':course_data,
            'assessments':assessments_data,
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
        data = []
        category = Category.objects.only('id').filter(id=id).first()
        if category:
            widget_obj = DetailPageWidget.objects.filter(content_type__model='Category', listid__contains=category.pk).first()
            widget_obj_data = widget_obj.widget.iw.indexcolumn_set.filter(column=1) if widget_obj and widget_obj.widget else []
            data = IndexColumnSerializer(widget_obj_data,many=True).data
        return Response(data,status=status.HTTP_200_OK)