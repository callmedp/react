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

        try:
            Skill.objects.get(id=value)
            return value
        except Exception as e:
            raise serializers.ValidationError("Skill with given id does not exits.")

    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value)
            return value
        except Exception as e:
            raise serializers.ValidationError("Product with given id does not exits.")

    def validate(self, data):
        try:
            product_skill = ProductSkill.objects.get(skill_id=data['skill_id'], product_id=data['product_id'])
            if product_skill:
                raise serializers.ValidationError("Duplicate entry. Product Id {} and Skill Id {} already exists together.".format(data['product_id'], data['skill_id']))
        except Exception as e:
            raise serializers.ValidationError(e)


