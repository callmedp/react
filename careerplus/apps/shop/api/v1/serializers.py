from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from shop.models import Product, PracticeTestInfo
from shared.rest_addons.mixins import SerializerFieldsMixin

class ProductListSerializerForAuditHistory(SerializerFieldsMixin, ModelSerializer):

    class Meta:
        model = Product
        fields = ('__all__')


class PracticeTestInfoCreateSerializer(ModelSerializer):
    has_completed = serializers.SerializerMethodField()

    class Meta:
        model = PracticeTestInfo
        fields = ('email', 'mobile_no', 'name', 'has_completed')

    def create(self, validated_data):
        try:
            test_info = PracticeTestInfo.objects.get(email=validated_data.get('email', None))
            test_info.save()
            return test_info
        except:
            return super(PracticeTestInfoCreateSerializer, self).create(validated_data)

    def get_has_completed(self, obj):
        return obj.has_completed
