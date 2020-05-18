# python imports


# django imports

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
        candidate_id = data_dict.get('loggedIn', '')
        try:
            if not candidate_id:
                raise Exception('Non LoggedIn User')
            response = ShineCandidateDetail().get_candidate_detail(shine_id=candidate_id)
            personal_details = response.get('personal_details', [])
            personal_detail = personal_details[0]
            mobile = personal_detail.get('cell_phone', '')
            email = personal_detail.get('email', '')
        except:
            email = data_dict.get('email', '')
            mobile = data_dict.get('mobile', '')
        if not email:
            return Response({"status": "FAIL"}, status=status.HTTP_400_BAD_REQUEST)
        total_score = data_dict.get('total_score', 0)
        section_score = data_dict.get('section_score', [])
        section_dict = {}
        for section in section_score:
            section_name = section.get('section_name', '')
            section_id = section_mapping.get(section_name, '')
            section_score = section.get('section_score', 0)
            if not section_name and not section_id:
                continue
            section_dict.update({
                    str(section_id) : str(section_score)
                })
        ResumeScoreCheckerUserDetails.objects.create(
                total_score = int(total_score),
                email = email,
                mobile_number = mobile,
                section_scores = section_dict,
            )
        return Response({"status": "SUCCESS"}, status=status.HTTP_200_OK)
