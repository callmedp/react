from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from shop.models import Product,Category
from shop.choices import  C_ATTR_DICT,S_ATTR_DICT
from shared.rest_addons.mixins import SerializerFieldsMixin


class ProductListSerializerForAuditHistory(SerializerFieldsMixin, ModelSerializer):

    class Meta:
        model = Product
        fields = ('__all__')


class CategorySerializer(SerializerFieldsMixin,ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ProductDetailSerializer(SerializerFieldsMixin,ModelSerializer):
    #
    # def to_representation(self,instance):
    #     ret = super(ProductDetailSerializer,self).to_representation(instance)
    #     asked_fields = self.context.get('asked_fields',[])
    #     [ret.pop(field,"") for field in asked_fields]
    #     return ret
    day_duration = serializers.CharField(read_only=True)
    absolute_url = serializers.CharField(read_only=True)



    class Meta:
        model = Product
        fields = '__all__'
