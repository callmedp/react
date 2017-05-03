from rest_framework.serializers import ModelSerializer
from cms import models
from rest_framework import serializers 
import datetime


class IndexerWidgetSerializer(ModelSerializer):
    """
        Serializer for `IndexerWidget` model
    """
    class Meta:
        model = models.IndexerWidget
        fields = '__all__'
        read_only_fields = ('id', 'last_modified_by', 'last_modified_on')


class ColumnHeadingSerializer(ModelSerializer):
    """
        Serializer for `ColumnHeading` model
    """
    class Meta:
        model = models.ColumnHeading
        fields = '__all__'
        read_only_fields = ('id', 'last_modified_by', 'last_modified_on')


class IndexColumnSerializer(ModelSerializer):
    """
        Serializer for `IndexColumn` model
    """
    class Meta:
        model = models.IndexColumn
        fields = '__all__'
        read_only_fields = ('id', 'last_modified_by', 'last_modified_on')


class WidgetSerializer(ModelSerializer):
    """
        Serializer for `IndexColumn` model
    """
    class Meta:
        model = models.Widget
        fields = '__all__'
        read_only_fields = ('id', 'last_modified_by', 'last_modified_on')


class PageSerializer(ModelSerializer):
    """
        Serializer for `Page` model 
    """
    # TODO: Through table for Widgets and inline form for Documents
    class Meta:
        model = models.Page
        fields = ('id', 'name', 'parent', 'slug', 'widgets', 'total_view', 'total_download', 'total_share', 'is_active', 'show_menu', 'allow_comment',
            'comment_count', 'publish_date', 'expiry_date', 'created_by', 'created_on', 'last_modified_by', 'last_modified_on', 'title', 'url', 'meta_desc', 'meta_keywords', 'heading')
        read_only_fields = ('id', 'total_view', 'total_download', 'total_share', 'comment_count', 'last_modified_by', 'last_modified_on')


class PageWidgetSerializer(ModelSerializer):
    """
        Serializer for `IndexColumn` model
    """
    class Meta:
        model = models.PageWidget
        fields = '__all__'
        read_only_fields = ('id', 'last_modified_by', 'last_modified_on')


class DocumentSerializer(ModelSerializer):
    """
        Serializer for `IndexColumn` model
    """
    class Meta:
        model = models.Document
        fields = '__all__'
        read_only_fields = ('id', )


class CommentSerializer(ModelSerializer):
    """
        Serializer for `Comment` model 
    """ 
    class Meta:
        model = models.Comment
        fields = '__all__'
        read_only_fields = ('id', 'last_modified_by', 'last_modified_on')


class PageCounterSerializer(ModelSerializer):
    """
        Serializer for `Comment` model
    """
    class Meta:
        model = models.PageCounter
        fields = '__all__'
        read_only_fields = ('id', 'last_modified_by', 'last_modified_on')
