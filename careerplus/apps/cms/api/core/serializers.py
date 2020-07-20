from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from cms import models
from cms.config import COLUMN_TYPE, WIDGET_CHOICES
from rest_framework import serializers
import datetime
from django.core.cache import cache
from users.models import User
from blog.models import Blog


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ('id', 'image', 'image_alt', 'url', 'title', 'heading')


class CommentSerializer(serializers.ModelSerializer):
    """
        Serializer for `Comment` model
    """
    message = serializers.CharField(
        style={'template': 'console/fields/textarea.html', 'rows': 4})
    is_published = serializers.BooleanField(required=False,
                                            style={'template': 'console/fields/checkbox.html', 'attrs': {}})
    is_removed = serializers.BooleanField(required=False,
                                          style={'template': 'console/fields/checkbox.html', 'attrs': {}})
    page = serializers.PrimaryKeyRelatedField(queryset=models.Page.objects.all(),
                                              style={'template': 'console/fields/select.html', 'empty_text': 'Select Page', 'attrs': {}})
    replied_to = serializers.PrimaryKeyRelatedField(allow_null=True, queryset=models.Comment.objects.all(), required=False,
                                                    style={'template': 'console/fields/select.html', 'empty_text': 'Select Comment replied to', 'attrs': {}})

    class Meta:
        model = models.Comment
        fields = ('id', 'message', 'is_published', 'is_removed', 'page',
                  'replied_to', 'last_modified_by', 'last_modified_on')
        read_only_fields = ('id', 'last_modified_by', 'last_modified_on')


class ColumnHeadingSerializer(serializers.ModelSerializer):
    """
        Serializer for `ColumnHeading` model
    """
    column = serializers.ChoiceField(label='Column*', choices=COLUMN_TYPE, style={'template': 'console/fields/select.html', 'empty_text': 'Select Column',
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
    column = serializers.ChoiceField(label='Column*', choices=COLUMN_TYPE, style={'template': 'console/fields/select.html', 'empty_text': 'Select Column',
                                                                                  'attrs': {'data-parsley-required': True}})
    url = serializers.URLField(allow_blank=True, max_length=2048, required=False,
                               style={'template': 'console/fields/input.html', 'attrs': {'data-parsley-trigger': 'keyup', 'data-parsley-length': [3, 2048], 'data-parsley-type': 'url'}})
    name = serializers.CharField(label='Name*', max_length=255,
                                 style={'template': 'console/fields/input.html',
                                        'attrs': {'data-parsley-trigger': 'keyup', 'data-parsley-length': [4, 255], 'data-parsley-required': True}})

    # heading = serializers.SerializerMethodField()

    class Meta:
        model = models.IndexColumn
        fields = ('id', 'column', 'url', 'name', 'indexer_id')
        read_only_fields = ('id',)

    # def get_heading(self,obj):
    #     if not obj.indexer_id:
    #         return ''
    #     column_name = obj.indexer.columnheading_set.only('name').first()
    #     if not column_name:
    #         return ''
    #     return column_name.name


class IndexerWidgetSerializer(serializers.ModelSerializer):
    """
        Serializer for `IndexerWidget` model
    """
    heading = serializers.CharField(max_length=255, allow_blank=True, allow_null=True, required=False,
                                    style={'template': 'console/fields/input.html',
                                           'attrs': {'data-parsley-trigger': 'keyup', 'data-parsley-length': [4, 255]}})
    column_heading = ColumnHeadingSerializer(label='ColumnHeading', many=True)
    index_column = IndexColumnSerializer(label='IndexColumn', many=True)

    class Meta:
        model = models.IndexerWidget
        fields = ('id', 'heading', 'column_heading', 'index_column',
                  'last_modified_by', 'last_modified_on')
        read_only_fields = ('id', 'last_modified_by', 'last_modified_on')
    #
    # def compose_column_heading(self, validated_column_heading_data):
    #     if validated_column_heading_data.get('indexer_id'):
    #         retrieved_column_headings = models.ColumnHeading.objects.filter(indexer=validated_column_heading_data.get('indexer_id'))
    #         if retrieved_column_headings and len(retrieved_column_headings):
    #             serialized_column_heading = ColumnHeadingSerializer(retrieved_column_headings[0], data=validated_column_heading_data)
    #             if serialized_column_heading.is_valid():
    #                 return serialized_column_heading.save()
    #     return ColumnHeadingSerializer().create(validated_column_heading_data)
    #
    # def compose_index_column(self, validated_index_column_data):
    #     if validated_index_column_data.get('indexer_id'):
    #         retrieved_index_columns = models.IndexColumn.objects.filter(indexer=validated_index_column_data.get('indexer_id'))
    #         if retrieved_index_columns and len(retrieved_index_columns):
    #             serialized_index_column = IndexColumnSerializer(retrieved_index_columns[0], data=validated_index_column_data)
    #             if serialized_index_column.is_valid():
    #                 return serialized_index_column.save()
    #     return IndexColumnSerializer().create(validated_index_column_data)
    #

    def represent_column_heading(self, obj):
        if hasattr(obj, 'id') and obj.id:
            retrieved_column_headings = models.ColumnHeading.objects.filter(
                indexer=obj.id)
            if retrieved_column_headings and len(retrieved_column_headings):
                serialized_column_heading = ColumnHeadingSerializer(
                    retrieved_column_headings, many=True)
                return serialized_column_heading.to_representation(serialized_column_heading.data)
        return None

    def represent_index_column(self, obj):
        if hasattr(obj, 'id') and obj.id:
            retrieved_index_columns = models.IndexColumn.objects.filter(
                indexer=obj.id)
            if retrieved_index_columns and len(retrieved_index_columns):
                serialized_index_column = IndexColumnSerializer(
                    retrieved_index_columns, many=True)
                return serialized_index_column.to_representation(serialized_index_column.data)
        return None

    def to_representation(self, obj):
        obj.column_heading = self.represent_column_heading(obj)
        obj.index_column = self.represent_index_column(obj)
        data = super(IndexerWidgetSerializer, self).to_representation(obj)
        return data

    # def create(self, validated_data):
    #     column_heading_data = validated_data.get('column_heading', {})
    #     index_column_data = validated_data.get('index_column', {})
    #     validated_data.pop('column_heading')
    #     validated_data.pop('index_column')
    #     indexer_obj = super(IndexerWidgetSerializer, self).create(validated_data)
    #     column_heading_data['indexer_id'] = indexer_obj.id
    #     index_column_data['indexer_id'] = indexer_obj.id
    #     column_heading_obj = self.compose_column_heading(column_heading_data)
    #     index_column_obj = self.compose_index_column(index_column_data)
    #     return indexer_obj
    #
    # def update(self, instance, validated_data):
    #     column_heading_data = validated_data.get('column_heading', {})
    #     index_column_data = validated_data.get('index_column', {})
    #     validated_data.pop('column_heading')
    #     validated_data.pop('index_column')
    #     indexer_obj = super(IndexerWidgetSerializer, self).update(instance, validated_data)
    #     column_heading_data['indexer_id'] = indexer_obj.id
    #     index_column_data['indexer_id'] = indexer_obj.id
    #     column_heading_obj = self.compose_column_heading(column_heading_data)
    #     index_column_obj = self.compose_index_column(index_column_data)
    #     return indexer_obj


class WidgetSerializer(serializers.ModelSerializer):
    """
        Serializer for `Widget` model
    """
    widget_type = serializers.ChoiceField(label='Widget Type*', choices=WIDGET_CHOICES,
                                          style={'template': 'console/fields/select.html', 'empty_text': 'Select Column',
                                                 'attrs': {'data-parsley-required': True}})
    heading = serializers.CharField(allow_blank=True, allow_null=True, max_length=1024, required=False,
                                    style={'template': 'console/fields/input.html',
                                           'attrs': {'data-parsley-max-length': 1024}})
    redirect_url = serializers.URLField(allow_blank=True, allow_null=True, help_text='Append http://.', label='Re-directing Url', max_length=200, required=False,
                                        style={'template': 'console/fields/input.html', 'attrs': {'data-parsley-trigger': 'keyup', 'data-parsley-length': [3, 200], 'data-parsley-type': 'url'}})
    image = serializers.FileField(allow_null=True, help_text='use this for Resume help', required=False,
                                  style={'template': 'console/fields/input.html', 'attrs': {}})
    image_alt = serializers.CharField(allow_blank=True, allow_null=True, max_length=100, required=False,
                                      style={'template': 'console/fields/input.html',
                                             'attrs': {'data-parsley-max-length': 100}})
    description = serializers.CharField(allow_blank=True, allow_null=True, required=False,
                                        style={'template': 'console/fields/textarea.html', 'rows': 10})
    document_upload = serializers.FileField(allow_null=True, label='Document', required=False,
                                            style={'template': 'console/fields/input.html', 'attrs': {}})
    display_name = serializers.CharField(allow_blank=True, allow_null=True, max_length=100, required=False,
                                         style={'template': 'console/fields/input.html',
                                                'attrs': {'data-parsley-max-length': 100}})
    writer_designation = serializers.CharField(allow_blank=True, allow_null=True, max_length=255, required=False,
                                               style={'template': 'console/fields/input.html',
                                                      'attrs': {'data-parsley-max-length': 255}})
    is_external = serializers.BooleanField(required=False,
                                           style={'template': 'console/fields/checkbox.html', 'attrs': {}})
    is_pop_up = serializers.BooleanField(required=False,
                                         style={'template': 'console/fields/checkbox.html', 'attrs': {}})
    is_active = serializers.BooleanField(required=False,
                                         style={'template': 'console/fields/checkbox.html', 'attrs': {}})
    related_article = BlogSerializer(many=True)
    # iw = serializers.PrimaryKeyRelatedField(allow_null=True, label='Indexer Widget', queryset=models.IndexerWidget.objects.all(), required=False,
    #     style={'template': 'console/fields/select.html', 'empty_text': 'Select associated Indexer Widget', 'attrs': {}})

    iw = IndexerWidgetSerializer()

    class Meta:
        model = models.Widget
        fields = '__all__'
        read_only_fields = ('id', 'created_by', 'created_on',
                            'last_modified_by', 'last_modified_on')


class DocumentSerializer(serializers.ModelSerializer):
    """
        Serializer for `Document` model
    """
    doc = serializers.FileField(label='Document', required=False,
                                style={'template': 'console/fields/input.html', 'attrs': {}})
    is_active = serializers.BooleanField(required=False,
                                         style={'template': 'console/fields/checkbox.html', 'attrs': {}})
    priority = serializers.IntegerField(max_value=2147483647, min_value=-2147483648, required=False,
                                        style={'template': 'console/fields/input.html', 'attrs': {}})

    class Meta:
        model = models.Document
        fields = ('id', 'doc', 'is_active', 'priority', 'page')
        read_only_fields = ('id', 'page')


class PageWidgetSerializer(serializers.ModelSerializer):
    """
        Serializer for `PageWidget` model
    """
    # page = PageSerializer()
    widget = WidgetSerializer()

    class Meta:
        model = models.PageWidget
        # fields = '__all__'
        exclude = ['page']
        read_only_fields = ('id', 'last_modified_by', 'last_modified_on')


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
    # widgets = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Widget.objects.all(), required=False,
    #     style={'template': 'console/fields/select_multiple.html', 'attrs': {'id': 'id_page_widgets'}})
    is_active = serializers.BooleanField(required=False,
                                         style={'template': 'console/fields/checkbox.html', 'attrs': {}})
    show_menu = serializers.BooleanField(required=False,
                                         style={'template': 'console/fields/checkbox.html', 'attrs': {}})
    allow_comment = serializers.BooleanField(required=False,
                                             style={'template': 'console/fields/checkbox.html', 'attrs': {}})
    publish_date = serializers.DateTimeField(allow_null=True, required=False,
                                             style={'template': 'console/fields/datetime.html', 'attrs': {'id': 'id_page_publishing'}})
    expiry_date = serializers.DateTimeField(allow_null=True, required=False,
                                            style={'template': 'console/fields/datetime.html', 'attrs': {'id': 'id_page_expiry'}})
    title = serializers.CharField(allow_blank=True, max_length=255, required=False,
                                  style={'template': 'console/fields/input.html', 'attrs': {'data-parsley-length': [4, 255]}})
    url = serializers.URLField(allow_blank=True, max_length=255, required=False,
                               style={'template': 'console/fields/input.html',
                                      'attrs': {'data-parsley-trigger': 'keyup', 'data-parsley-length': [3, 255], 'data-parsley-type': 'url'}})
    meta_desc = serializers.CharField(allow_blank=True, label='Meta Description', required=False,
                                      style={'template': 'console/fields/textarea.html', 'rows': 10})
    meta_keywords = serializers.CharField(allow_blank=True, label='Keywords', required=False,
                                          style={'template': 'console/fields/textarea.html', 'rows': 4})
    heading = serializers.CharField(allow_blank=True, max_length=255, required=False,
                                    style={'template': 'console/fields/input.html',
                                           'attrs': {'data-parsley-length': [4, 255]}})
    document = DocumentSerializer(label='Document', required=False)
    # widgets = serializers.SerializerMethodField()

    class Meta:
        model = models.Page
        fields = ('id', 'name', 'parent', 'slug', 'total_view', 'total_download', 'total_share', 'is_active',
                  'show_menu', 'allow_comment',
                  'comment_count', 'publish_date', 'expiry_date', 'created_by', 'created_on', 'last_modified_by', 'last_modified_on', 'title', 'url', 'meta_desc', 'meta_keywords', 'heading', 'document')
        read_only_fields = ('id', 'slug', 'total_view', 'total_download', 'total_share', 'comment_count',
                            'created_by', 'created_on', 'last_modified_by', 'last_modified_on',)

    # def get_widgets(self,obj):
    #     return obj.widgets.filter(is_active=True).values_list('id',flat=True)

    def compose_document(self, validated_document_data):
        if validated_document_data.get('page'):
            retrieved_documents = models.Document.objects.filter(
                page=validated_document_data.get('page'))
            if retrieved_documents and len(retrieved_documents):
                serialized_document = DocumentSerializer(
                    retrieved_documents[0], data=validated_document_data)
                if serialized_document.is_valid():
                    return serialized_document.save()
        return DocumentSerializer().create(validated_document_data)

    def to_representation(self, obj):
        document = obj.document_set.filter().first()
        data = super(PageSerializer, self).to_representation(obj)
        comment = obj.comment_set.filter(is_published=True, is_removed=False).values(
            'name', 'message', 'created_on')
        if obj.parent_id:
            data.update({'parent_name': obj.parent.get_display_name})
        if comment:
            data.update({'comments': comment})
        if document:
            data.update({'document': document.doc.url})
        return data
    #

    # def create(self, validated_data):
    #     document_data = validated_data.get('document', {})
    #     validated_data.pop('document')
    #     page_obj = super(PageSerializer, self).create(validated_data)
    #     document_data['page'] = page_obj
    #     if 'doc' in document_data and document_data['doc']:
    #         document_obj = self.compose_document(document_data)
    #     return page_obj

    # def update(self, instance, validated_data):
    #     document_data = validated_data.get('document', {})
    #     validated_data.pop('document')
    #     page_obj = super(PageSerializer, self).update(instance, validated_data)
    #     document_data['page'] = page_obj
    #     if 'doc' in document_data and document_data['doc']:
    #         document_obj = self.compose_document(document_data)
    #     return page_obj


class PageCounterSerializer(serializers.ModelSerializer):
    """
        Serializer for `PageCounter` model
    """
    page = serializers.PrimaryKeyRelatedField(queryset=models.Page.objects.all(), required=True,
                                              style={'template': 'console/fields/select.html', 'empty_text': 'Select Page', 'attrs': {}})
    count_period = serializers.DateField(required=True,
                                         style={'template': 'console/fields/datetime.html', 'attrs': {'id': 'id_pagecounter_period'}})
    no_views = serializers.IntegerField(max_value=4294967296, min_value=0, required=False,
                                        style={'template': 'console/fields/input.html', 'attrs': {}})
    no_downloads = serializers.IntegerField(max_value=4294967295, min_value=0, required=False,
                                            style={'template': 'console/fields/input.html', 'attrs': {}})
    no_shares = serializers.IntegerField(max_value=4294967295, min_value=0, required=False,
                                         style={'template': 'console/fields/input.html', 'attrs': {}})
    comment_count = serializers.IntegerField(max_value=4294967295, min_value=0, required=False,
                                             style={'template': 'console/fields/input.html', 'attrs': {}})

    class Meta:
        model = models.PageCounter
        fields = '__all__'
        read_only_fields = ('id', 'added_on', 'modified_on')
        validators = [UniqueTogetherValidator(
            queryset=models.PageCounter.objects.all(), fields=('page', 'count_period'))]
