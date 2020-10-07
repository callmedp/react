from rest_framework.generics import (ListAPIView)
from django.conf import settings
from django.contrib.auth import get_user_model
from .serializers import GetUsersSerializer, UserProfileSerializer
from users.models import UserProfile
from shared.rest_addons.pagination import LearningCustomPagination


import json

User = get_user_model()


class GetUsersView(ListAPIView):
    serializer_class = GetUsersSerializer
    authentication_classes = ()
    permission_classes = ()

    def get_queryset(self):
        group = self.request.query_params.get('group', '')
        active = json.loads(self.request.query_params.get('active', 'false'))
        queryset = User.objects.all()
        if group == 'welcome_call':
            group = settings.WELCOMECALL_GROUP_LIST
            queryset = queryset.filter(groups__name__in=group, is_active=active)
        return queryset


class WriterUsersListView(ListAPIView):
    serializer_class = UserProfileSerializer
    authentication_classes = ()
    permission_classes = ()
    pagination_class = LearningCustomPagination
    queryset = UserProfile.objects.filter(writer_type__gte=1)
