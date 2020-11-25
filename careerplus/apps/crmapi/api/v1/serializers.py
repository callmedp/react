from rest_framework import serializers
from crmapi.models import UserQuries


class LeadManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuries
        fields = '__all__'
