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


class ProductDetailSerializer(SerializerFieldsMixin,ModelSerializer):
    #
    # def to_representation(self,instance):
    #     ret = super(ProductDetailSerializer,self).to_representation(instance)
    #     asked_fields = self.context.get('asked_fields',[])
    #     [ret.pop(field,"") for field in asked_fields]
    #     return ret

    class Meta:
        model = Product
        fields = '__all__'

