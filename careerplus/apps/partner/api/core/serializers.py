from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from partner import models
from rest_framework import serializers 
import datetime
from users.models import User
from geolocation.models import (
    Country,
    State,
    City,)

class VendorSerializer(serializers.ModelSerializer):
    """
        Serializer for `Vendor` model
    """
    name = serializers.CharField(label='Name*', max_length=100,
        style={'template': 'console/fields/input.html',
        'attrs': {'data-parsley-trigger': 'keyup', 'data-parsley-length': [4, 100], 'data-parsley-required': True}})
    slug = serializers.CharField(label='Slug*', max_length=100, validators=[UniqueValidator(queryset=models.Vendor.objects.all())],
        style={'template': 'console/fields/input.html',
        'attrs': {'data-parsley-trigger': 'keyup', 'data-parsley-length': [4, 100], 'data-parsley-required': True}})
    email = serializers.EmailField(label='Email*', max_length=100, validators=[UniqueValidator(queryset=models.Vendor.objects.all())],
        style={'template': 'console/fields/input.html',
        'attrs': {'data-parsley-trigger': 'keyup', 'data-parsley-length': [4, 100], 'data-parsley-required': True, 'data-parsley-type': 'email'}})
    mobile = serializers.CharField(max_length=20, required=False, allow_blank=True,
        style={'template': 'console/fields/input.html',
        'attrs': {'data-parsley-trigger': 'keyup', 'data-parsley-length': [6, 20]}})
    country = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=Country.objects.all(),
        style={'template': 'console/fields/select.html', 'empty_text': 'Select Country',
        'attrs': {'id': 'vendor-country'}})
    state = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=State.objects.all(),
        style={'template': 'console/fields/select.html', 'empty_text': 'Select State',
        'attrs': {}})
    city = serializers.PrimaryKeyRelatedField(required=False, allow_null=True, queryset=City.objects.all(),
        style={'template': 'console/fields/select.html', 'empty_text': 'Select City',
        'attrs': {'id': 'vendor-city'}})
    address = serializers.CharField(required=False, allow_blank=True,
        style={'template': 'console/fields/textarea.html',
        'attrs': {}})
    image = serializers.ImageField(required=False, allow_null=True, allow_empty_file=False,
        style={'template': 'console/fields/input.html',
        'attrs': {}})
    icon = serializers.ImageField(required=False, allow_null=True, allow_empty_file=False,
        style={'template': 'console/fields/input.html',
        'attrs': {}})
    pan = serializers.CharField(label='PAN Number', required=False, allow_blank=True, max_length=20,
        style={'template': 'console/fields/input.html',
        'attrs': {'data-parsley-trigger': 'keyup', 'data-parsley-length': 10}})
    website = serializers.CharField(required=False, allow_blank=True, max_length=20,
        style={'template': 'console/fields/input.html',
        'attrs': {'data-parsley-trigger': 'keyup', 'data-parsley-length': [4,20]}})
    employees = serializers.PrimaryKeyRelatedField(label='Vendor Hierarchy', many=True, queryset=User.objects.all(), required=False,
        style={'template': 'console/fields/select_multiple.html', 'attrs': {'id': 'id_vendor_employees'}})

    title = serializers.CharField(allow_blank=True, max_length=255, required=False,
        style={'template': 'console/fields/input.html', 'attrs': {'data-parsley-length': [4, 255]}})
    url = serializers.URLField(allow_blank=True, max_length=255, required=False,
        style={'template': 'console/fields/input.html',
        'attrs': {'data-parsley-trigger': 'keyup', 'data-parsley-length': [3, 255], 'data-parsley-type': 'url'}})
    meta_desc = serializers.CharField(allow_blank=True, label='Meta Description', required=False,
        style={'template': 'console/fields/textarea.html', 'rows': 10})
    meta_keywords = serializers.CharField(allow_blank=True, label='Keywords', required=False,
        style={'template': 'console/fields/textarea.html', 'rows': 4})
    heading = serializers.CharField(allow_blank=True, max_length=255, required=False,
        style={'template': 'console/fields/input.html',
        'attrs': {'data-parsley-length': [4, 255]}})
    image_alt = serializers.CharField(allow_blank=True, max_length=255, required=False,
        style={'template': 'console/fields/input.html',
        'attrs': {'data-parsley-length': [4, 255]}})

    class Meta:
        model = models.Vendor
        fields = ('id', 'name', 'slug', 'email', 'mobile', 'country', 'state', 'city', 'address', 'image', 'icon', 'pan', 'website', 'employees',
            'title', 'url', 'meta_desc', 'meta_keywords', 'heading', 'image_alt', 'created', 'modified')
        read_only_fields = ('id', 'created', 'modified')


class VendorHierarchySerializer(serializers.ModelSerializer):
    """
        Serializer for `VendorHierarchy` model
    """
    active = serializers.BooleanField(required=False,
        style={'template': 'console/fields/checkbox.html', 'attrs': {}})
    vendee = serializers.PrimaryKeyRelatedField(label='Vendor', queryset=models.Vendor.objects.all(),
        style={'template': 'console/fields/select.html', 'empty_text': 'Select City',
        'attrs': {}})
    employee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
        style={'template': 'console/fields/select.html', 'empty_text': 'Select City',
        'attrs': {}})
    class Meta:
        model = models.VendorHierarchy
        fields = '__all__'
        read_only_fields = ('id', 'designation') #, 'created', 'modified')