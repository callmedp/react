from rest_framework.serializers import ModelSerializer
from shop.models import Product,Category
from shared.rest_addons.mixins import SerializerFieldsMixin


class ProductListSerializerForAuditHistory(SerializerFieldsMixin, ModelSerializer):

    class Meta:
        model = Product
        fields = ('__all__')


class CategorySerializer(SerializerFieldsMixin,ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
