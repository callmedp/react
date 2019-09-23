# python imports

# django imports
from django.http import HttpResponse, HttpResponseForbidden


# local imports
from payment.utils import ZestMoneyUtil

# inter app imports


# third party imports

import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class ZestMoneyFetchEMIPlansApi(APIView):
	authentication_classes = ()
	permission_classes = ()
	serializer_class = None

	def get(self, request, *args, **kwargs):
		amount = self.request.GET.get('amount',0)
		if not amount:
			return HttpResponseForbidden()
		zest_util_obj = ZestMoneyUtil()
		response_data = zest_util_obj.get_emi_plans(amount)
		return Response(response_data.get('recommended_options',[]),
						status=status.HTTP_200_OK)



