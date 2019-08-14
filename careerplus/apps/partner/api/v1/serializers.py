#python import

# inbuilt import

# third party
from rest_framework import serializers

# inter-app import
from partner.models import Vendor
from shared.rest_addons.mixins import (SerializerFieldsMixin,
ListSerializerContextMixin, ListSerializerDataMixin)


class VendorListSerializer(SerializerFieldsMixin,serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
