from dashboard.dashboard_mixin import DashboardInfo
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView


class DashboardMyorderApi(DashboardInfo, APIView):

    def get(self, request, *args, **kwargs):
        candidate_id = self.request.session.get('candidate_id', None)
        if candidate_id:
            order_list = DashboardInfo().get_myorder_list(candidate_id=candidate_id, request=self.request)
        else:
            order_list = ''
        return Response(order_list,status=status.HTTP_200_OK)