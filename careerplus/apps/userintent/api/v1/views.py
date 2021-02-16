from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from core.common import APIResponse
from .mixins import RecommendationMixin
from haystack.query import SearchQuerySet
from homepage.api.v1.mixins import ProductMixin
from order.models import OrderItem
from userintent.models import UserIntent
from shine.core import ShineCandidateDetail

import logging
logger = logging.getLogger('error_log')
class CourseRecommendationAPI(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_classes = None

    def get(self,request):
        candidate_id = request.GET.get('candidate_id', None)
        if not candidate_id:
            candidate_id = '601b8120ca3f418906a889a8'
        intent = request.GET.get('intent',None)
        course_data = []
        data = {
        'user_desiredjt': request.GET.get("preferred_role",None),
        'user_functionalarea':request.GET.get("department",None),
        'user_exp' : request.GET.get('experience',None),
        'user_app_skills': request.GET.get('skills',None),
        #below fields are not used in intent capture form
        'user_imp_skills':request.GET.get('user_imp_skills',None),
        'user_skills':request.GET.get('user_skills',None),
        'user_jobtitle':request.GET.get('user_jobtitle',None)
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
            return APIResponse(error=True,message='Error in user intent object creation',status=status.HTTP_400_BAD_REQUEST)

        # data = {  
        #         "user_imp_skills": ["hindi", "english", "auto cad", "internet browsing", "industrial training", "microsoft office"],
        #         "user_app_skills": ["auto cad"],
        #         "user_skills": ["transport manager and camp boss", "secretarial", "stores", "transport management", "office administration"],
        #         "user_jobtitle": "purchase officer",
        #         "user_functionalarea": "purchase",
        #         "user_desiredjt": ["purchase officer", "storekeeper", "document controller"],
        #         "user_exp": "0 yr 4 months"
        #     }
        course_ids = RecommendationMixin().get_courses_from_analytics_recommendation_engine(data=data)
        if course_ids:
            user_purchased_courses = OrderItem.objects.filter(product__type_flow=2,no_process=False,order__candidate_id=candidate_id,order__status__in=[1, 3]).values_list('product__id')
            courses = SearchQuerySet().filter(id__in=course_ids).exclude(id__in=user_purchased_courses)
            course_data = ProductMixin().get_course_json(courses)
        return APIResponse(data={'course_data':course_data,'course_ids':course_ids},message='recommended courses fetched', status=status.HTTP_200_OK)

class JobsSearchAPI(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_classes = None

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
                return APIResponse(data=jobs_response,message='Jobs fetched', status=status.HTTP_200_OK)
            except Exception as e:
                logging.getLogger('error_log').error('response for {} - {}'.format(candidate_id, str(e)))
                return APIResponse(error=True,message='Error in user intent object creation',status=status.HTTP_400_BAD_REQUEST)