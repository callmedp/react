# django imports
from django.conf import settings
from shared.rest_addons.authentication import ShineUserAuthentication
from rest_framework.permissions import IsAuthenticated

# third parth imports

from rest_framework.generics import (APIView)


class CartOrderView(APIView):
    authentication_classes = (ShineUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = None


    def post(self, request, *args, **kwargs):
        print('hello')


