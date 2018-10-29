from rest_framework.serializers import ModelSerializer
from shop.models import Product
from shared.rest_addons.mixins import SerializerFieldsMixin


class ProductListSerializerForAuditHistory(SerializerFieldsMixin, ModelSerializer):

    class Meta:
        model = Product
        fields = ('__all__')
