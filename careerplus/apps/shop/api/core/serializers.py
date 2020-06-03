from rest_framework import serializers
from shop import models


class ProductSerializer(serializers.ModelSerializer):
    """
        Serializer for `Product` model
    """
    class Meta:
        model = models.Product
        fields = '__all__'
        read_only_fields = ('id',)


class ProductSerializerForThankYouAPI(serializers.ModelSerializer):
    get_name = serializers.CharField(allow_null=True, allow_blank=True)

    class Meta:
        model = models.Product
        fields = ('id', 'name', 'is_course', 'is_assesment',
                  'sub_type_flow', 'get_name')


class DeliveryServiceSerializerForThankYouAPI(serializers.ModelSerializer):

    class Meta:
        model = models.DeliveryService
        fields = 'id', 'name'
