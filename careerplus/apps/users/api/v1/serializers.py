from rest_framework import serializers
from django.contrib.auth import get_user_model

# in app imports
from users.models import UserProfile

User = get_user_model()


class GetUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    user = GetUsersSerializer(required=True)

    class Meta:
        model = UserProfile
        fields = (
            'user', 'profile_photo', 'description', 'facebook_url', 'twitter_url', 'linkedIn_url'
            )
