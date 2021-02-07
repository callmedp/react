import requests
from datetime import datetime
from django.conf import settings
import logging

from core.api_mixin import ShineCandidateDetail
from shop.models import Product

class VendorUrlMixins():
    def get_candidate_details(self, candidate_id):
        if not candidate_id:
            return {"error_message":"Please Complete your Registration on Shine to Access the Course"}

        personal_detail = None
        try:
            candidate_details = ShineCandidateDetail().get_candidate_detail(shine_id=candidate_id)
        except Exception as e:
            logging.getLogger('error_log').error("Unable to fetch candidate data for id {},\
                 for vendor registeration :{}".format(candidate_id, e))
        personal_details = candidate_details.get('personal_detail')
        if isinstance(personal_details, list) and len(personal_details)>0:
            personal_detail = personal_details[0]

        if not personal_detail:
            return {"error_message":"Please Complete your Registration on Shine to Access the Course"}
        if not personal_detail.get('first_name', '') or not personal_detail.get('email', '') or \
            not personal_detail.get('cell_phone', ''):
                return {"error_message":"Please Complete your Registration on Shine to Access the Course"}
    
        return personal_detail


    def get_isel_global_url(self, data_dict):
        """
        login token for isel global
        """
        # email = data_dict.get('Email', '')\
        candidate_id = data_dict.get('candidate_id', '')
        default_url = settings.ISEL_GLOBAL_URLS.get('default_url')

        if not candidate_id:
            return default_url
        headers = { 'Authorization' :  settings.ISEL_GLOBAL_URLS.get('authentication')}
        
        candidate_details = self.get_candidate_details(candidate_id = candidate_id)

        if candidate_details.get('error_message', ''):
            return candidate_details


        data = {"Email" : candidate_details.get('email', '')}
        try: 
            response = requests.post(settings.ISEL_GLOBAL_URLS.get("check_candidate_exists"), 
                data=data, headers=headers)
            if response.status_code != 200:
                return default_url
        except Exception as e:
            logging.getLogger('error_log').error("vendor api response error {}".format(e))

        response_data = response.json()
        user_name = '{} {}'.format(candidate_details.get('first_name', ''), 
                candidate_details.get('last_name', ''))
        course_id = data_dict.get("course_id", 0)
        try:
            course = Product.objects.filter(id = course_id).first()
            if course:
                course_name = course.name
                if not course_name:
                    logging.getLogger('error_log').error("No universal product code provided for course: {}".format(course.id))
                    return default_url

        except Exception as e:
            logging.getLogger('error_log').error("vendor api response error {}".format(e))

        # course_name = data_dict.get('Course', '')
        # user_name = data_dict.get('StudentName', '')
        now = datetime.now()
        course_registered = False
        if response_data.get('status', '') == 'success':

            response = requests.post(settings.ISEL_GLOBAL_URLS.get("get_assigned_courses"),
                data, headers=headers)
            if response.status_code != 200:
                return default_url
            response_data = response.json()
            course_list = response_data.get('data', [])
            for course in course_list:
                if course.get('Course','') == course_name:
                    course_registered = True

        if not course_registered:
            data.update({
                "StudentName" : user_name,
                "password" : "password",
                "Course" : course_name,
                "StartDate" : now.strftime("%Y-%m-%d")
            })
            response = requests.post(settings.ISEL_GLOBAL_URLS.get("register_candidate"), 
                data, headers=headers)
            if response.status_code != 200:
                return default_url
        try: 
            response = requests.post(settings.ISEL_GLOBAL_URLS.get("get_login_token"),
                {"Email" : candidate_details.get('email', '')}, headers=headers)
            if response.status_code != 200:
                return default_url
        except Exception as e:
            logging.getLogger('error_log').error("vendor api response error {}".format(e))

        response_data = response.json()
        if response_data.get('status') != 'success':
            return default_url

        response_value = response_data.get('data', {})
        login_url = response_value.get('LoginUrl', None)
        if login_url:
            return login_url
        return default_url

    def get_erb_academy_url(self, data_dict):
        '''
        login token for erb academy url
        '''

        vendor_data = settings.ERB_ACADEMY_URLS
        default_url = vendor_data.get("default_url")
        header_data = {
            "username" : vendor_data.get("username"),
            "password" : vendor_data.get("password")
            }

        try:
            response = requests.post(vendor_data.get("header_api"), header_data)

            if response.status_code != 200:
                return default_url
        except Exception as e:
            logging.getLogger('error_log').error("vendor api response error {}".format(e))


        response_data = response.json()
        response_value = response_data.get('data', {})
        header = {"Authorization" : response_value.get('token', '')}
        course_id = data_dict.get("course_id", 0)

        try:
            course = Product.objects.filter(id = course_id).first()

            if course:
                product_id = course.upc
                if not product_id:
                    logging.getLogger('error_log').error("No universal product code provided for course: {}".format(course.id))
                    return default_url
        except Exception as e:
            logging.getLogger('error_log').error("vendor api response error {}".format(e))

        candidate_id = data_dict.get('candidate_id')
        candidate_details = self.get_candidate_details(candidate_id = candidate_id)

        if candidate_details.get('error_message', ''):
            return candidate_details

        data = {
            "candidate_email" : candidate_details.get('email', ''),
            "product_id" : product_id,
            "candidate_phone" : candidate_details.get('cell_phone', ''),
            "candidate_name" : '{} {}'.format(candidate_details.get('first_name', ''), 
                candidate_details.get('last_name', '')),
            "shine_learning_order_id" : data_dict.get('order_id', '')
        }

        try:
            response = requests.post(vendor_data.get('register_new_product'), 
                data=data, headers=header)
            if response.status_code != 200:
                logging.getLogger('error_log').error("vendor api response error {}".format(e))
                return default_url
        except Exception as e:
            logging.getLogger('error_log').error("vendor api response error {}".format(e))

        response_data = response.json()
        if response_data.get('message', '') != 'Order successfully added':
            return default_url
        url_data = response_data.get('data', {})
        url = url_data.get('sso_url', '')

        if not url:
            return default_url

        return url

    def get_vendor_mapping(self, vendor_slug, data_dict):
        """
        list of vendor for iframe
        """
        # vendor_choice = dict(IFRAME_VENDOR_CHOICES)
        # vendor_name = None
        # for  key in vendor_choice:
        #     if vendor_choice[key] == vendor_slug:
        #         vendor_name = vendor_choice[key]
        if not vendor_slug:
            return None
        if vendor_slug == "isel_global":
            return self.get_isel_global_url(data_dict = data_dict)
        elif vendor_slug == "erb_academy":
            return self.get_erb_academy_url(data_dict = data_dict)
