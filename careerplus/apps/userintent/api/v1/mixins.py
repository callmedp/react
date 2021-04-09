# Django imports 
from django.conf import settings    
from django.core.cache import cache
from rest_framework.status import HTTP_400_BAD_REQUEST
# Inter app imports
from shop.models import Product
from order.models import OrderItem
from payment.models import PaymentTxn
from core.common import APIResponse

import requests
import json
from pymongo import MongoClient
import urllib
import logging  
logger = logging.getLogger('error_log')

class RecommendationMixin(object):
    LEARNING_MONGO_PORT = settings.ANALYTICS_MONGO_PORT
    LEARNING_MONGO_USERNAME = settings.ANALYTICS_MONGO_USERNAME
    LEARNING_MONGO_PASSWORD = settings.ANALYTICS_MONGO_PASSWORD
    LEARNING_MONGO_INSTANCE_STR = settings.ANALYTICS_MONGO_INSTANCE_STR
    LEARNING_MONGO_DB = settings.ANALYTICS_MONGO_DB

    def __init__(self):
        # Recommended services data is to be fetched from LearningAnalytics mongo database.
        connection_string = 'mongodb://{}:{}@{}/{}'.format(
            urllib.parse.quote(self.LEARNING_MONGO_USERNAME),urllib.parse.quote(self.LEARNING_MONGO_PASSWORD),
            self.LEARNING_MONGO_INSTANCE_STR, self.LEARNING_MONGO_DB
        )
        conn = MongoClient(connection_string)
        database = conn[self.LEARNING_MONGO_DB]
        self.coll = database['recos_service_prod']
        self.courses = database['recos_course_prod']

    def get_services_from_analytics_recommendation_engine(self, candidate_id=None):
        recommended_services_ids = []
        add_assessment = False
        if candidate_id is None:
            recommendation = self.coll.find_one({"fcu": settings.DEFAULT_LEARNING_SERVICE_RECOMMENDATION_CANDIDATE_ID})
        else:
            recommendation = self.coll.find_one({"fcu": candidate_id})
        if not recommendation:
            recommendation = self.coll.find_one({"fcu": settings.DEFAULT_LEARNING_SERVICE_RECOMMENDATION_CANDIDATE_ID})
        try:
            services = eval(recommendation['s_lst'])
            assessments = eval(recommendation['a_lst'])
            services = services if isinstance(services, list) else []
            assessments= (
                assessments if isinstance(assessments, list) else []
            )
            #Get product against fetched assessment and services category id as per mapping ANALYTIC_TO_LEARNING_PRODUCTFLOWS
            type_flows =[]
            sub_type_flows=[]
            for service_id in services:
                type_flows.extend(settings.ANALYTIC_TO_LEARNING_PRODUCTFLOWS[service_id]['type_flow'])
                sub_type_flows.extend(settings.ANALYTIC_TO_LEARNING_PRODUCTFLOWS[service_id]['sub_type_flow'])

            if 2 in services and assessments:
                add_assessment = True

            # Get services already purchased by user
            excl_txns = PaymentTxn.objects.filter(
            status__in=[0, 2, 3, 4, 5,6],
            payment_mode__in=[6, 7],
            order__candidate_id=candidate_id)
            excl_order_list = excl_txns.all().values_list('order_id', flat=True)
            user_purchased_items = OrderItem.objects.filter(order__candidate_id=candidate_id, no_process=False,order__status__in=[1, 3]).exclude(order__in=excl_order_list).values_list('product__id',flat=True)
            recommended_services_ids = list(Product.objects.filter(type_flow__in=type_flows,sub_type_flow__in=sub_type_flows).exclude(id__in=user_purchased_items).values_list('id',flat=True))
            if add_assessment:
                recommended_services_ids.append(assessments[0])
            return recommended_services_ids
        except:
            recommended_services_ids = []
        return recommended_services_ids
    
    def get_courses_from_analytics_recommendation_engine(self,data={}):
        data = json.dumps(data)
        headers = {"Content-type": "application/json"}
        course_ids = []

        try:
            response = requests.post(
                settings.ANALYTICS_COURSES_RECOMMENDATION_API,
                data=data,
                headers=headers,
                auth=settings.ANALYTICS_COURSES_RECOMMENDATION_API_AUTH,
            )
            course_ids = response.json().get("course_ids", [])
        except ValueError as e:
            logger.info(
                f"Unable to parse JSON Response from analytics courses recommended api:{repr(e)}"
            )

        except requests.ConnectionError as e:
            logger.info(
                f"Connection Error Occured Unable to connect to analytics courses recommended api {repr(e)}"
            )

        except requests.Timeout as e:
            logger.info(
                f"Timeout Error Occured Unable to connect to analytics courses recommended api {repr(e)}"
            )

        return course_ids
    
    def get_courses_and_certification_from_analytics_recommendation_db(self, candidate_id=None):
        recommended_course_ids = []
        recommended_assessment_ids = []
        if candidate_id is None:
            service_recommendation = self.coll.find_one({"fcu": settings.DEFAULT_LEARNING_SERVICE_RECOMMENDATION_CANDIDATE_ID})
            course_recommendation = self.coll.find_one({"fcu": settings.DEFAULT_LEARNING_SERVICE_RECOMMENDATION_CANDIDATE_ID})

        else:
            course_recommendation = self.courses.find_one({"fcu": candidate_id})          
            service_recommendation = self.coll.find_one({"fcu": candidate_id})
        if service_recommendation and course_recommendation:
            try:
                courses = eval(course_recommendation['cand_courses'])
                assessments = eval(service_recommendation['a_lst'])
                # Get services already purchased by user
                excl_txns = PaymentTxn.objects.filter(
                status__in=[0, 2, 3, 4, 5,6],
                payment_mode__in=[6, 7],
                order__candidate_id=candidate_id)
                excl_order_list = excl_txns.all().values_list('order_id', flat=True)
                user_purchased_items = OrderItem.objects.filter(order__candidate_id=candidate_id, no_process=False,order__status__in=[1, 3]).exclude(order__in=excl_order_list).values_list('product__id',flat=True)
                recommended_course_ids = [x for x in courses if x not in user_purchased_items]
                recommended_assessment_ids = [x for x in assessments if x not in user_purchased_items]
                return {'courses':recommended_course_ids,'assessment':recommended_assessment_ids}
            except:
                recommended_course_ids = []
        return {'courses':recommended_course_ids,'assessment':recommended_assessment_ids}