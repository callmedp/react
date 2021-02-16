    
import requests
import logging  
from django.conf import settings    
logger = logging.getLogger('error_log')
import json
    
def get_courses_from_analytics_recommendation_engine(self):
    data = {
        "user_imp_skills": self.imp_skills,
        "user_app_skills": self.job_skills,
        "user_skills": self.profile_skills,
        "user_jobtitle": self.user_jobtitle,
        "user_functionalarea": self.user_fa,
        "user_desiredjt": self.desiredjt,
        "user_exp": self.user_exp,
    }
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
