from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from core.common import APIResponse
from haystack.query import SearchQuerySet

from .mixins import RecommendationMixin
from homepage.api.v1.mixins import ProductMixin
from order.models import OrderItem
from userintent.models import UserIntent
from shine.core import ShineCandidateDetail

from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from django.core.cache import cache
from django.conf import settings

#Logger import
import logging
logger = logging.getLogger('error_log')

class CourseRecommendationAPI(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self,request):
        candidate_id = request.GET.get('candidate_id', None)
        if not candidate_id:
            course_ids = settings.DEFAULT_LEARNING_COURSE_RECOMMENDATION_PRODUCT_ID
        intent = request.GET.get('intent',None)
        course_data = []
        data = {
        'user_desiredjt': request.GET.get("preferred_role",''),
        'user_functionalarea':request.GET.get("department",''),
        'user_exp' : request.GET.get('experience',''),
        'user_app_skills': request.GET.get('skills',''),
        #below fields are not used in intent capture form
        'user_imp_skills':request.GET.get('user_imp_skills',''),
        'user_skills':request.GET.get('user_skills',''),
        'user_jobtitle':request.GET.get('user_jobtitle','')
        }
        #Capturing user intent request made
        try:
            UserIntent.objects.create(
                preferred_role=data['user_desiredjt'],
                department=data['user_functionalarea'],
                experience=data['user_exp'],
                skills=data['user_app_skills'],
                intent=intent,
                candidate_id=candidate_id
            )
            logging.getLogger('info_log').info('userintent obj created')
        except Exception as e:
            logging.getLogger('error_log').error('response for {} - {}'.format(candidate_id, str(e)))
            return APIResponse(error=True,message='Error in user intent object creation',status=HTTP_400_BAD_REQUEST)

        course_ids = RecommendationMixin().get_courses_from_analytics_recommendation_engine(data=data)
        user_purchased_courses = OrderItem.objects.filter(product__type_flow=2,no_process=False,order__candidate_id=candidate_id,order__status__in=[1, 3]).values_list('product__id',flat=True)
        course_ids = [4,1,1568,570,2,7]
        courses = SearchQuerySet().filter(id__in=course_ids).exclude(id__in=user_purchased_courses)
        course_data = ProductMixin().get_course_json(courses)
        return APIResponse(data={'course_data':course_data,'recommended_course_ids':course_ids},message='recommended courses fetched', status=HTTP_200_OK)

class ServiceRecommendationAPI(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self,request):
        candidate_id = request.GET.get('candidate_id', None)
        # if not candidate_id:
        #     candidate_id = '5e4c0b5f5d0795517fd73c08'
        # data = cache.get(f"analytics_recommendations_services{candidate_id}",None)
        # if data is None:
        recommended_services_ids = RecommendationMixin().get_services_from_analytics_recommendation_engine(candidate_id=candidate_id)
        services = SearchQuerySet().filter(id__in=recommended_services_ids)
        data = ProductMixin().get_course_json(services)
    #     cache.set(
    #     f"analytics_recommendations_services{candidate_id}", data, timeout=86400
    # )
        return APIResponse(data=data,message='recommended services fetched', status=HTTP_200_OK)

class JobsSearchAPI(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get(self,request):
        candidate_id = request.GET.get('candidate_id', None)
        if not candidate_id:
            candidate_id = '601b8120ca3f418906a889a8'
        intent = request.GET.get('intent',None)
        data = {
        'job_title': request.GET.get("job_title",None),
        'loc':request.GET.get("loc",None),
        'minexp' : request.GET.get('minexp',None),
        'skill': request.GET.get('skill',None),
        'farea': request.GET.get("area", ""),
        # 'q': request.GET.get("q", "")
        }  
        if candidate_id:
            try:
                jobs_response = ShineCandidateDetail().get_jobs(shine_id=candidate_id,data=data)
            except Exception as e:
                logging.getLogger('error_log').error(
                    "Data fetch from shine.com jobs search api failed  - {}".format(e))
            try:
                UserIntent.objects.create(
                    preferred_role=data['job_title'],
                    department=data['farea'],
                    experience=data['minexp'],
                    skills=data['skill'],
                    intent=intent,
                    candidate_id=candidate_id
                )
                return APIResponse(data=jobs_response,message='Jobs fetched', status=HTTP_200_OK)
            except Exception as e:
                logging.getLogger('error_log').error('response for {} - {}'.format(candidate_id, str(e)))
                return APIResponse(error=True,message='Error in user intent object creation',status=HTTP_400_BAD_REQUEST)