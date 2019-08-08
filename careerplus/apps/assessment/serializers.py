from .models import Test
from rest_framework.serializers import ModelSerializer,SerializerMethodField, Serializer
from rest_framework import serializers
from shared.rest_addons.mixins import SerializerFieldsMixin, ListSerializerContextMixin, ListSerializerDataMixin
from django.shortcuts import reverse
from shop.models import Category,Product

class TestSerializer(SerializerFieldsMixin, ListSerializerContextMixin, ListSerializerDataMixin,ModelSerializer):

    question_count = serializers.CharField(read_only=True)


    list_lookup_fields = ['course_id', 'product_id', 'category_id']
    fields_required_mapping = {'course_id': ['name','inr_price'],
                               'product_id': ['name','inr_price','day_duration'],
                               'category_id': ['name','inr_price','day_duration'],
                              }
    field_model_mapping = {'course_id': Product, 'product_id': Product, 'category_id': Category}

    class Meta:
        model = Test
        fields = '__all__'
