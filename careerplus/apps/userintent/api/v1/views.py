from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from core.common import APIResponse
from .mixins import RecommendationMixin
from haystack.query import SearchQuerySet
from homepage.api.v1.mixins import ProductMixin
from order.models import OrderItem
from userintent.models import UserIntent
import logging
logger = logging.getLogger('error_log')
class CourseRecommendationAPI(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_classes = None

    def get(self,request):
        candidate_id = self.request.session.get('candidate_id', None)
        intent = request.GET.get('intent',None)
        data = {
        'preferred_role': request.GET.get("preferred_role",None),
        'department':request.GET.get("department",None),
        'experience' : request.GET.get('experience',None),
        'skills': request.GET.get('skills',None),
        }
        try:
            UserIntent.objects.create(
                preferred_role=data['preferred_role'],
                department=data['department'],
                experience=data['experience'],
                skills=data['skills'],
                intent=intent,
                candidate_id='601b8120ca3f418906a889a8'
            )
            logging.getLogger('error_log').info('userintent obj created')
        except Exception as e:
            logging.getLogger('error_log').error('response for {} - {}'.format(candidate_id, str(e)))
            return APIResponse(error=True,message='Error in user intent object creation',status=status.HTTP_400_BAD_REQUEST)

        data = {  
                "user_imp_skills": ["hindi", "english", "auto cad", "internet browsing", "industrial training", "microsoft office"],
                "user_app_skills": ["auto cad"],
                "user_skills": ["transport manager and camp boss", "secretarial", "stores", "transport management", "office administration"],
                "user_jobtitle": "purchase officer",
                "user_functionalarea": "purchase",
                "user_desiredjt": ["purchase officer", "storekeeper", "document controller"],
                "user_exp": "0 yr 4 months"
            }
        data = RecommendationMixin().get_courses_from_analytics_recommendation_engine(data=data)
        # res ={
        #     'data':data
        # }
        # if data.get('status')=="success":
        #     course_ids = data.get('course_ids',None)
        #     user_purchased_courses = OrderItem.objects.filter(product__type_flow=2,no_process=False,order__candidate_id=candidate_id,order__status__in=[1, 3]).values_list('product__id')
        #     courses = SearchQuerySet().filter(id__in=course_ids).exclude(id__in=user_purchased_courses)
        #     course_data = ProductMixin().get_course_json(courses)
        #     res['course_data']=course_data
        return APIResponse(data=data,message='recommended courses fetched', status=status.HTTP_200_OK)