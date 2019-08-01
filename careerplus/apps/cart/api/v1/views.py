# python imports
import base64, json, logging
import random
from datetime import datetime, date

# django imports

# local imports

# inter app imports
from users.mixins import RegistrationLoginApi

# third party imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class EmailStatusView(APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = None

    def get(self, request, *args, **kwargs):
        email = kwargs.get('email')
        email_status = RegistrationLoginApi.check_email_exist(email)
        return Response(
            email_status, status=status.HTTP_200_OK)
