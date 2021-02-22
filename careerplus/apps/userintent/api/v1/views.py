# Django imports
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from core.common import APIResponse
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from django.core.cache import cache
from django.conf import settings

from haystack.query import SearchQuerySet

# Inter app imports
from .mixins import RecommendationMixin
from homepage.api.v1.mixins import ProductMixin
from order.models import OrderItem
from userintent.models import UserIntent
from shine.core import ShineCandidateDetail
from api.helpers import offset_paginator

#Logger import
import logging
logger = logging.getLogger('error_log')

class CourseRecommendationAPI(APIView):
    """
    Fetches recommended courses based on parameters like preferred role, skills etc from recommendaton engine.
    Method: GET
    ==================================================================================
    Input:
    get parameters: preferred_role, department, experience, skills
    
    other parameters based on user profile(not mandatory): user_imp_skills, user_skills, user_jobtitle

    Response :list of recommended courses based on input parameters
    """
    permission_classes = ()
    authentication_classes = ()

    def get(self,request):
        candidate_id = request.GET.get('candidate_id', None)
        page = int(request.GET.get('page',1))
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

        course_id = RecommendationMixin().get_courses_from_analytics_recommendation_engine(data=data)
        user_purchased_courses = OrderItem.objects.filter(product__type_flow=2,no_process=False,order__candidate_id=candidate_id,order__status__in=[1, 3]).values_list('product__id',flat=True)
        course_ids = [4,1,1568,570,2]
        courses = SearchQuerySet().filter(id__in=course_ids).exclude(id__in=user_purchased_courses)
        paginated_data = offset_paginator(page, courses,size=3)
        course_data = ProductMixin().get_course_json(paginated_data["data"])
        #pagination
        page_info ={
                'current_page':paginated_data['current_page']if paginated_data else 0,
                'total':paginated_data['total_pages'] if paginated_data else 0,
                'has_prev': True if paginated_data['current_page'] >1 else False,
                'has_next':True if (paginated_data['total_pages']-paginated_data['current_page'])>0 else False
                }
        data ={
            'course_data':course_data,
            'recommended_course_ids':course_id,
            'page':page_info
        }
        return APIResponse(data=data,message='recommended courses fetched', status=HTTP_200_OK)

class ServiceRecommendationAPI(APIView):
    """
    Fetches recommended services from recommedation enginge database.
    """
    permission_classes = ()
    authentication_classes = ()

    def get(self,request):
        candidate_id = request.GET.get('candidate_id', None)
        page = int(request.GET.get('page',1))
        # data = cache.get(f"analytics_recommendations_services{candidate_id}",None)
        # if data is None:
        data = []
        recommended_services_ids = RecommendationMixin().get_services_from_analytics_recommendation_engine(candidate_id=candidate_id)
        services = SearchQuerySet().filter(id__in=recommended_services_ids)
        paginated_data = offset_paginator(page, services,size=3)
        data = ProductMixin().get_course_json(paginated_data["data"])
        #pagination
        page_info ={
                'current_page':paginated_data['current_page']if paginated_data else 0,
                'total':paginated_data['total_pages'] if paginated_data else 0,
                'has_prev': True if paginated_data['current_page'] >1 else False,
                'has_next':True if (paginated_data['total_pages']-paginated_data['current_page'])>0 else False
                }
        return APIResponse(data={'services':data,'page':page_info},message='recommended services fetched', status=HTTP_200_OK)
        # cache.set(f"analytics_recommendations_services{candidate_id}", data, timeout=86400)

class JobsSearchAPI(APIView):
    """
    Returns list of available jobs based on parameters like location, experience etc.

    Input fields :
    ==================================================================================
    q -> The main query parameter i.e. the keyword for search for non logged in user.

    loc -> Location for which the job is to be searched.

    area -> Functional Area of the job(Integer value from lookup)

    minexp -> Minimum experience of the jobs to be searched.

    page -> Page no of the search results to be requested.

    ==================================================================================
    """
    permission_classes = ()
    authentication_classes = ()

    def get(self,request):
        candidate_id = request.GET.get('candidate_id', None)
        intent = request.GET.get('intent',None)
        data = {
        'job_title': request.GET.get("job_title",''),
        'loc':request.GET.get("loc",''),
        'minexp' : request.GET.get('minexp',''),
        'skill': request.GET.get('skill',''),
        'farea': request.GET.get("area", ''),
        # 'q': request.GET.get("q", ''),
        'page':int(request.GET.get('page',1))
        } 
        if not candidate_id:
            if data['job_title'] and data['skill']:
                data['q'] = data['job_title']+'-'+data['skill']
            elif data['skill']:
                data['q']=data['skill']
            elif data['job_title']:
                data['q'] = data['job_title']
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
            return APIResponse(error=True,message='Error in user intent object creation..Passing intent value as 0,1 etc?',status=HTTP_400_BAD_REQUEST)

class KeywordSuggestionAPI(APIView):
    """
    Returns skills and jobs suggestions as per the query entered.

    Input fields :
    ==================================================================================
    q -> The main query parameter i.e. the keyword for search.
    skill_only -> returns only suggested skills

    ==================================================================================
    """
    permission_classes = ()
    authentication_classes = ()

    def get(self,request):
        skill_only = request.GET.get('skill_only', False)
        job_title_only = request.GET.get('job_title_only',False)
        skill_quantity = request.GET.get('skill_quantity',7)
        job_title_quantity = request.GET.get('job_title_quantity',7)
        suggestion_quantity = request.GET.get('suggestion_quantity',7)

        q = request.GET.get('q', '')
        skills = []
        job_titles = []
        data = {}
        try:
            response = ShineCandidateDetail().get_keyword_sugesstion(query=q,skill_only=skill_only)
            if response:
                keyword_suggestions = response.get('keyword_suggestion',None)[:suggestion_quantity]
                data['keyword_suggestion'] = keyword_suggestions
                if not(skill_only and job_title_only):
                    for word in keyword_suggestions:
                        word_type = word.get('type',None)
                        if word_type == 'skill':
                            if len(skills)<skill_quantity:
                                skills.append(word)
                        elif len(job_titles)<job_title_quantity:
                            job_titles.append(word)
                    if skill_only:                   
                        data['keyword_suggestion'] = skills
                    elif job_title_only:
                        data['keyword_suggestion'] = job_titles

            return APIResponse(data=data,message='suggested words fetched', status=HTTP_200_OK)
        except Exception as e:
            logging.getLogger('error_log').error(
                "Data fetch from shine.com jobs search api failed  - {}".format(e))
            return APIResponse(error=True,message='Data fetch from shine.com api failed : {}'.format(e),status=HTTP_400_BAD_REQUEST)
