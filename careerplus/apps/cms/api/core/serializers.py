from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from cms import models
from cms.config import COLUMN_TYPE, WIDGET_CHOICES
from rest_framework import serializers 
import datetime
from users.models import User

class ColumnHeadingSerializer(serializers.ModelSerializer):
    """
        Serializer for `ColumnHeading` model
    """
    column =  serializers.ChoiceField(label='Column*', choices=COLUMN_TYPE, style={'template': 'console/fields/select.html', 'empty_text': 'Select Column',
        'attrs': {'data-parsley-required': True}})
    name = serializers.CharField(label='Name*', max_length=255,
        style={'template': 'console/fields/input.html',
        'attrs': {'data-parsley-trigger': 'keyup', 'data-parsley-length': [4, 255], 'data-parsley-required': True}})
    class Meta:
        model = models.ColumnHeading
        fields = ('id', 'column', 'name', 'indexer_id')
        read_only_fields = ('id',)


class IndexColumnSerializer(serializers.ModelSerializer):
    """
        Serializer for `IndexColumn` model
    """
    column =  serializers.ChoiceField(label='Column*', choices=COLUMN_TYPE, style={'template': 'console/fields/select.html', 'empty_text': 'Select Column',
        'attrs': {'data-parsley-required': True}})
    url = serializers.URLField(allow_blank=True, max_length=2048, required=False,
        style={'template': 'console/fields/input.html', 'attrs': {'data-parsley-trigger': 'keyup', 'data-parsley-length': [3, 2048], 'data-parsley-type': 'url'}})
    name = serializers.CharField(label='Name*', max_length=255,
        style={'template': 'console/fields/input.html',
        'attrs': {'data-parsley-trigger': 'keyup', 'data-parsley-length': [4, 255], 'data-parsley-required': True}})
    class Meta:
        model = models.IndexColumn
        fields = ('id', 'column', 'url', 'name', 'indexer_id')
        read_only_fields = ('id',)


class IndexerWidgetSerializer(serializers.ModelSerializer):
    """
        Serializer for `IndexerWidget` model
    """
    heading = serializers.CharField(max_length=255, allow_blank=True, allow_null=True, required=False,
        style={'template': 'console/fields/input.html',
        'attrs': {'data-parsley-trigger': 'keyup', 'data-parsley-length': [4, 255], 'data-parsley-required': True}})
    column_heading = ColumnHeadingSerializer(label='ColumnHeading')
    index_column = IndexColumnSerializer(label='Index Column')
    class Meta:
        model = models.IndexerWidget
        fields = ('id', 'heading', 'column_heading', 'index_column', 'last_modified_by', 'last_modified_on')
        read_only_fields = ('id', 'last_modified_by', 'last_modified_on')

    def compose_column_heading(self, validated_column_heading_data):
        if validated_column_heading_data.get('indexer_id'):
            retrieved_column_headings = models.ColumnHeading.objects.filter(indexer=validated_column_heading_data.get('indexer_id'))
            if retrieved_column_headings and len(retrieved_column_headings):
                serialized_column_heading = ColumnHeadingSerializer(retrieved_column_headings[0], data=validated_column_heading_data)
                if serialized_column_heading.is_valid():
                    return serialized_column_heading.save()
        return ColumnHeadingSerializer().create(validated_column_heading_data)

    def compose_index_column(self, validated_index_column_data):
        if validated_index_column_data.get('indexer_id'):
            retrieved_index_columns = models.IndexColumn.objects.filter(indexer=validated_index_column_data.get('indexer_id'))
            if retrieved_index_columns and len(retrieved_index_columns):
                serialized_index_column = IndexColumnSerializer(retrieved_index_columns[0], data=validated_index_column_data)
                if serialized_index_column.is_valid():
                    return serialized_index_column.save()
        return IndexColumnSerializer().create(validated_index_column_data)

    def represent_column_heading(self, obj):
        if hasattr(obj, 'id') and obj.id:
            retrieved_column_headings = models.ColumnHeading.objects.filter(indexer=obj.id)
            if retrieved_column_headings and len(retrieved_column_headings):
                serialized_column_heading = ColumnHeadingSerializer(retrieved_column_headings[0])
                return serialized_column_heading.to_representation(serialized_column_heading.data)
        return None

    def represent_index_column(self, obj):
        if hasattr(obj, 'id') and obj.id:
            retrieved_index_columns = models.IndexColumn.objects.filter(indexer=obj.id)
            if retrieved_index_columns and len(retrieved_index_columns):
                serialized_index_column = IndexColumnSerializer(retrieved_index_columns[0])
                return serialized_index_column.to_representation(serialized_index_column.data)
        return None

    def to_representation(self, obj):
        obj.column_heading = self.represent_column_heading(obj)
        obj.index_column = self.represent_index_column(obj)
        data = super(IndexerWidgetSerializer, self).to_representation(obj)
        return data

    def create(self, validated_data):
        column_heading_data = validated_data.get('column_heading', {})
        index_column_data = validated_data.get('index_column', {})
        validated_data.pop('column_heading')
        validated_data.pop('index_column')
        indexer_obj = super(IndexerWidgetSerializer, self).create(validated_data)
        column_heading_data['indexer_id'] = indexer_obj.id
        index_column_data['indexer_id'] = indexer_obj.id
        column_heading_obj = self.compose_column_heading(column_heading_data)
        index_column_obj = self.compose_index_column(index_column_data)
        return indexer_obj

    def update(self, instance, validated_data):
        column_heading_data = validated_data.get('column_heading', {})
        index_column_data = validated_data.get('index_column', {})
        validated_data.pop('column_heading')
        validated_data.pop('index_column')
        indexer_obj = super(IndexerWidgetSerializer, self).update(instance, validated_data)
        column_heading_data['indexer_id'] = indexer_obj.id
        index_column_data['indexer_id'] = indexer_obj.id
        column_heading_obj = self.compose_column_heading(column_heading_data)
        index_column_obj = self.compose_index_column(index_column_data)
        return indexer_obj


class WidgetSerializer(serializers.ModelSerializer):
    """
        Serializer for `Widget` model
    """
    widget_type = serializers.ChoiceField(choices=WIDGET_CHOICES)
    heading = serializers.CharField(allow_blank=True, allow_null=True, max_length=1024, required=False)
    redirect_url = serializers.URLField(allow_blank=True, allow_null=True, help_text='Append http://.', label='Re-directing Url', max_length=200, required=False)
    image = serializers.FileField(allow_null=True, help_text='use this for Resume help', required=False)
    image_alt = serializers.CharField(allow_blank=True, allow_null=True, max_length=100, required=False)
    description = serializers.CharField(allow_blank=True, allow_null=True, required=False, style={'base_template': 'textarea.html'})
    document_upload = serializers.FileField(allow_null=True, label='Document', required=False)
    display_name = serializers.CharField(allow_blank=True, allow_null=True, max_length=100, required=False)
    writer_designation = serializers.CharField(allow_blank=True, allow_null=True, max_length=255, required=False)
    is_external = serializers.BooleanField(required=False)
    is_pop_up = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)
    user = serializers.PrimaryKeyRelatedField(allow_null=True, help_text='for user or writer', queryset=User.objects.all(), required=False)
    iw = serializers.PrimaryKeyRelatedField(allow_null=True, label='Indexer Widget', queryset=models.IndexerWidget.objects.all(), required=False)
    class Meta:
        model = models.Widget
        fields = '__all__'
        read_only_fields = ('id', 'created_by', 'created_on', 'last_modified_by', 'last_modified_on')


class PageSerializer(serializers.ModelSerializer):
    """
        Serializer for `Page` model 
    """
    # TODO: Through table for Widgets and inline form for Documents
    name = serializers.CharField(label='Name*', max_length=255,
        style={'template': 'console/fields/input.html',
        'attrs': {'data-parsley-trigger': 'keyup', 'data-parsley-length': [4, 255], 'data-parsley-required': True}})
    parent = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=models.Page.objects.all(), required=False,
        style={'template': 'console/fields/select.html', 'empty_text': 'Select Parent Page', 'attrs': {}})
    widgets = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Widget.objects.all(), required=False,
        style={'template': 'console/fields/select_multiple.html', 'attrs': {'id': 'id_page_widgets'}})
    is_active = serializers.BooleanField(required=False,
        style={'template': 'console/fields/checkbox.html', 'attrs': {}})
    show_menu = serializers.BooleanField(required=False,
        style={'template': 'console/fields/checkbox.html', 'attrs': {}})
    allow_comment = serializers.BooleanField(required=False,
        style={'template': 'console/fields/checkbox.html', 'attrs': {}})
    publish_date = serializers.DateTimeField(allow_null=True, required=False,
        style={'template': 'console/fields/datetime.html', 'attrs': {}})
    expiry_date = serializers.DateTimeField(allow_null=True, required=False,
        style={'template': 'console/fields/datetime.html', 'attrs': {}})
    title = serializers.CharField(allow_blank=True, max_length=255, required=False,
        style={'template': 'console/fields/input.html', 'attrs': {'data-parsley-length': [4, 255]}})
    url = serializers.URLField(allow_blank=True, max_length=255, required=False,
        style={'template': 'console/fields/input.html', 'attrs': {'data-parsley-trigger': 'keyup', 'data-parsley-length': [3, 255], 'data-parsley-type': 'url'}})
    meta_desc = serializers.CharField(allow_blank=True, label='Meta Description', required=False,
        style={'template': 'console/fields/textarea.html', 'rows': 10})
    meta_keywords = serializers.CharField(allow_blank=True, label='Keywords', required=False,
        style={'template': 'console/fields/textarea.html', 'rows': 4})
    heading = serializers.CharField(allow_blank=True, max_length=255, required=False,
        style={'template': 'console/fields/input.html', 'attrs': {'data-parsley-length': [4, 255]}})
    
    class Meta:
        model = models.Page
        fields = ('id', 'name', 'parent', 'slug', 'widgets', 'total_view', 'total_download', 'total_share', 'is_active', 'show_menu', 'allow_comment',
            'comment_count', 'publish_date', 'expiry_date', 'created_by', 'created_on', 'last_modified_by', 'last_modified_on', 'title', 'url', 'meta_desc', 'meta_keywords', 'heading')
        read_only_fields = ('id', 'slug', 'total_view', 'total_download', 'total_share', 'comment_count', 'created_by', 'created_on', 'last_modified_by', 'last_modified_on')


class PageWidgetSerializer(serializers.ModelSerializer):
    """
        Serializer for `PageWidget` model
    """
    class Meta:
        model = models.PageWidget
        fields = '__all__'
        read_only_fields = ('id', 'last_modified_by', 'last_modified_on')


class DocumentSerializer(serializers.ModelSerializer):
    """
        Serializer for `Document` model
    """
    class Meta:
        model = models.Document
        fields = '__all__'
        read_only_fields = ('id', )


class CommentSerializer(serializers.ModelSerializer):
    """
        Serializer for `Comment` model 
    """ 
    class Meta:
        model = models.Comment
        fields = '__all__'
        read_only_fields = ('id', 'last_modified_by', 'last_modified_on')


class PageCounterSerializer(serializers.ModelSerializer):
    """
        Serializer for `PageCounter` model
    """
    class Meta:
        model = models.PageCounter
        fields = '__all__'
        read_only_fields = ('id', 'last_modified_by', 'last_modified_on')
