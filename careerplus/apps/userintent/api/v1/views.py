from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from core.common import APIResponse


class CourseRecommendation(APIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_classes = None

    def get(self,request):
        candidate_id = self.request.session.get('candidate_id', None)
        if candidate_id is None:
            return APIResponse(data='', error='Candidate Details required', status=status.HTTP_400_BAD_REQUEST)
        return APIResponse(data=['datalist'],message='Details data loaded', status=status.HTTP_200_OK)