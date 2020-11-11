# Python Imports
import datetime
import os
import json

# Core Django Imports
from django.conf import settings

# Local Imports
from .helper import APIResponse

# Inter App Imports

# Core RestFramework Imports
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

# Third Party Imports


class LeadManagementAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        """
        Need help Section:
        Getting the request from user like email, mobile, name, msg etc to create a lead
        in the back-end.
        Variables can be dynamic but the email or mobile should be neccessary.
        """

        # Specify the lead is not created yet
        created = False

        try:
            email               = request.POST.get('email' ,'')
            university_course   = request.POST.get('uc', 0)
            mobile_number       = request.POST.get('number', '')
            name                = request.POST.get('name', '')
            msg                 = request.POST.get('msg', '')
            prd                 = request.POST.get('prd', '')
            product_id          = request.POST.get('product', '')
            country             = request.POST.get('country', '91')
            source              = request.POST.get('source', '')
            queried_for         = 

        pass