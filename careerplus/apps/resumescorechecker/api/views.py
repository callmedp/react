# python imports
import logging
import requests
# django imports
from django.conf import settings
# local imports
from resumescorechecker.models import ResumeScoreCheckerUserDetails
from resumescorechecker.choices import section_mapping

# inter app imports
from core.api_mixin import ShineCandidateDetail
# third party imports
from rest_framework.response import Response
from rest_framework.views import APIView

class SaveResumeDetailsApiView(APIView):
    authentication_classes = ()
    permission_classes = []

    def post(self, request, *args, **kwargs):
        data_dict = self.request.data 
        if not data_dict:
            logging.getLogger("error_log").error("no data content recieved")
            return  Response({"status": "No data recieved"})
        candidate_id = data_dict.get('loggedIn', '')
        try:
            if not candidate_id:
                raise Exception('Non LoggedIn User')
            response = ShineCandidateDetail().get_candidate_detail(shine_id=candidate_id)
            personal_details = response.get('personal_detail', [])
            personal_detail = personal_details[0]
            mobile = personal_detail.get('cell_phone', '')
            email = personal_detail.get('email', '')
        except Exception as e:
            logging.getLogger("info_log").info("Not a logged in user, reason : {}".format(e))
            email = data_dict.get('email', '')
            mobile = data_dict.get('mobile', '')
        if not email:
            logging.getLogger("info_log").info("Email is not found from resume nor from candidate")
            return Response({"status": "No email is found"})
        total_score = data_dict.get('total_score', 0)
        section_score = data_dict.get('section_score', [])
        section_dict = {}
        if isinstance(section_score, list):
            for section in section_score:
                section_name = section.get('section_name', '')
                section_id = section_mapping.get(section_name, '')
                section_score = section.get('section_score', 0)
                if not section_name and not section_id:
                    continue
                section_dict.update({
                        str(section_id) : str(section_score)
                    })

        if not email and not mobile and not candidate_id:
            logging.getLogger("info_log").info("No Details is present")
            return Response({"status": "No Details is present"})
        # user_detail = ResumeScoreCheckerUserDetails.objects.filter(email=email)

        # if user_detail:
        #     logging.getLogger("info_log").error("User is already present")
        #     user = user_detail[0]
        #     user.total_score = int(total_score)
        #     user.mobile = mobile
        #     user.section_score = section_dict
        #     user.save()
        #     return Response({"status": "User was already present, score updated"})
        try: 
            user = ResumeScoreCheckerUserDetails.objects.create(
                    total_score = int(total_score),
                    email = email,
                    mobile_number = mobile,
                    candidate_id = candidate_id,
                    section_scores = section_dict,
                )
            if user:
                logging.getLogger("info_log").info("Resume score checker user is added")
        except Exception as e:
            logging.getLogger("error_log").error("Error in adding user to resume score checker, reason - {}".format(e))
            return Response({"status": "Failure to add user"})
        return Response({"status": "SUCCESS"})

class GetResumeScoreApiView(APIView):
    authentication_classes = ()
    permission_classes = []

    def post(self, request, *args, **kwargs):
        file = self.request.FILES
        url = settings.RESUME_SHINE_URL + '/api/resume-score-checker/get-score/'
        try:
            response = requests.post(url, files=file)
            if response.status_code == 200:
                result = response.json()
                data = result.get('data',{})
                total_score = data.get('total_score', None)
                if not total_score:
                    return Response({"status": "ERROR", "error": "unable to Parse Resume"})
                return Response({"status": "SUCCESS", "total_score":total_score})
        except Exception as e:
            logging.getLogger('error_log').error('unable to Parse Resume %s'%str(e))
            return Response({"status": "ERROR", "error": "Unable to Parse Resume"})

