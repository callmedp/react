from rest_framework import serializers
from userintent.models import RecommendationFeedback

class RecommendationFeedbackSerializer(serializers.ModelSerializer):
    """
    RecommendationFeedback serializer
    """
    class Meta:
        model = RecommendationFeedback
        fields = '__all__'