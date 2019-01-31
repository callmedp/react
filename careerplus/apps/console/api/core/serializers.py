# inter app imports
from shop.models import (ProductSkill, Skill, Product)

#third party imports
from rest_framework import serializers


class ProductSkillSerializer(serializers.ModelSerializer):

    skill_id = serializers.IntegerField()
    product_id = serializers.IntegerField()

    class Meta:
        model = ProductSkill
        fields = ('id', 'skill_id', 'active', 'priority', 'product_id',)

    def validate_skill_id(self, value):
        skill = Skill.objects.filter(id=value).first()
        if skill is None:
            raise serializers.ValidationError("Skill with given id does not exits.")
        return value

    def validate_product_id(self, value):
        product = Product.objects.filter(id=value).first()
        if product is None:
            raise serializers.ValidationError("Product with given id does not exits.")
        return value

    def validate(self, data):
        if self.context['request'].method == 'POST':
            product_skill = ProductSkill.objects.filter(skill_id=data['skill_id'], product_id=data['product_id']).first()
            if product_skill is not None:
                raise serializers.ValidationError("Duplicate entry. Product Id {} and Skill Id {} already exists together.".format(data['product_id'], data['skill_id']))
        return data

    def to_representation(self, instance):
        data = super(ProductSkillSerializer, self).to_representation(instance)
        skill_name = instance.skill.name
        data.update({'skill_name': skill_name})
        return data




class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ('id', 'name',)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name',)
