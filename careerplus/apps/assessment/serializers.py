from .models import Test
from rest_framework.serializers import ModelSerializer,SerializerMethodField, Serializer
from shared.rest_addons.mixins import SerializerFieldsMixin
from django.shortcuts import reverse

class TestSerializer(SerializerFieldsMixin,ModelSerializer):

    class Meta:
        model = Test
        fields = '__all__'
