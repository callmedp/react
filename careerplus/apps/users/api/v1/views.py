from rest_framework.generics import (ListAPIView)
from django.conf import settings
from django.contrib.auth import get_user_model
from .serializers import GetUsersSerializer

User = get_user_model()

class GetUsersView(ListAPIView):
    serializer_class = GetUsersSerializer
    authentication_classes = ()
    permission_classes = ()

    def get_queryset(self):
        group = self.kwargs['group']
        active = self.kwargs['active']
        queryset =User.objects.all()
        if group =='welcome_call':
            group = settings.WELCOMECALL_GROUP_LIST
            queryset = queryset.filter(groups__name__in=group,is_active=active)
        return queryset
        