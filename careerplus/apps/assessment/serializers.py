from .models import Test
from rest_framework.serializers import ModelSerializer,SerializerMethodField, Serializer
from rest_framework import serializers
from shared.rest_addons.mixins import SerializerFieldsMixin
from django.shortcuts import reverse

class TestSerializer(SerializerFieldsMixin,ModelSerializer):

    question_count = serializers.CharField(read_only=True)

    class Meta:
        model = Test
        fields = '__all__'
