from rest_framework.serializers import ModelSerializer
from cms.models import Page, Comment
from rest_framework import serializers 
import datetime


class PageSerializer(ModelSerializer):
    """
        Serializer for `Page` model 
    """
    name = serializers.CharField(
        max_length=255,
        style={'placeholder': 'The H1 heading for the page'}
    )
    class Meta:
        model = Page
        fields = ('id', 'name', 'parent', 'slug', 'widgets', 'total_view', 'total_download', 'total_share', 'is_active', 'show_menu', 'allow_comment',
            'comment_count', 'publish_date', 'expiry_date', 'created_by', 'created_on', 'last_modified_by', 'last_modified_on', 'title', 'url', 'meta_desc', 'meta_keywords', 'heading')
        read_only_fields = ('id', 'total_view', 'total_download', 'total_share', 'comment_count', 'last_modified_by', 'last_modified_on')


class CommentSerializer(ModelSerializer):
    """
        Serializer for `Comment` model 
    """ 
    class Meta:
        model = Comment
        fields = '__all__'
