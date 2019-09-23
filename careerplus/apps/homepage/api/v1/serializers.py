from rest_framework import serializers
from homepage.models import StaticSiteContent

class StaticSiteContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaticSiteContent
        fields = ['page_type','content','page_name']