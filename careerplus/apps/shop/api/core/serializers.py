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
