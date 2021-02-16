    
import requests
import logging  
from django.conf import settings    
logger = logging.getLogger('error_log')
import json


class RecommendationMixin(object):
    
    def get_courses_from_analytics_recommendation_engine(self,data={}):
        # data = {
        #     "user_app_skills": data.get('skills'),
        #     # "user_skills": self.profile_skills,
        #     # "user_jobtitle": data.get('preferred_role'),
        #     "user_app_skills": ["auto cad"],
        #     "user_jobtitle": "purchase officer",
        #     "user_skills": ["transport manager and camp boss", "secretarial", "stores", "transport management", "office administration"],
        #     "user_functionalarea": data.get('department'),
        #     "user_desiredjt":  data.get('preferred_role'),
        #     "user_exp":  data.get('experience'),
        # }
        data = json.dumps(data)
        headers = {"Content-type": "application/json"}
        course_ids = []
        # status="failure"

        try:
            response = requests.post(
                settings.ANALYTICS_COURSES_RECOMMENDATION_API,
                data=data,
                headers=headers,
                auth=settings.ANALYTICS_COURSES_RECOMMENDATION_API_AUTH,
            )
            course_ids = response.json().get("course_ids", [])
            # course_ids = response.json().get("course_ids", [])
            # status = response.json().get("status", None)
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
