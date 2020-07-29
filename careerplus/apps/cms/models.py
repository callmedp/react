from collections import OrderedDict

from django.db import models
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from ckeditor_uploader.fields import RichTextUploadingField
from meta.models import ModelMeta

from core.models import AbstractCommonModel
from seo.models import AbstractSEO
from blog.models import Blog

from .config import WIDGET_CHOICES, SECTION, COLUMN_TYPE

my_store = FileSystemStorage(location='careerplus/download/')


class IndexerWidget(AbstractCommonModel):
    heading = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.id) + self.heading


class ColumnHeading(models.Model):
    column = models.PositiveIntegerField(choices=COLUMN_TYPE)
    name = models.CharField(max_length=255)
    indexer = models.ForeignKey(IndexerWidget,on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.name


class IndexColumn(models.Model):
    indexer = models.ForeignKey(IndexerWidget,on_delete=models.CASCADE)
    column = models.PositiveIntegerField(choices=COLUMN_TYPE)
    url = models.CharField(
        max_length=2048, null=True,
        blank=True,
        help_text='provide full url with valid protocol https:// or http://')
    name = models.CharField(max_length=255)

    ranking = models.IntegerField(
        default=0,
        help_text='determine ranking indexer url')

    class Meta:
        ordering = ['ranking']

    def __str__(self):
        return '%s' % self.name


class Widget(AbstractCommonModel):
    widget_type = models.PositiveIntegerField(
        choices=WIDGET_CHOICES, null=False, blank=False)
    heading = models.CharField(max_length=1024, null=True, blank=True)
    redirect_url = models.URLField(
        null=True, blank=True,
        verbose_name='Re-directing Url',
        help_text='Append http://.')

    image = models.FileField(
        "Image", max_length=200,
        upload_to="images/cms/widget/",
        blank=True, null=True, help_text='use this for Resume help')
    image_alt = models.CharField(max_length=100, null=True, blank=True)

    description = RichTextUploadingField(null=True, blank=True)

    document_upload = models.FileField(
        "Document", max_length=200,
        upload_to="documents/cms/widget/", blank=True, null=True)

    display_name = models.CharField(
        max_length=100, null=True, blank=True)
    writer_designation = models.CharField(
        max_length=255, null=True, blank=True)

    iw = models.ForeignKey(
        IndexerWidget, null=True, blank=True,
        verbose_name='Indexer Widget',on_delete=models.CASCADE)

    related_article = models.ManyToManyField(Blog, blank=True)

    is_external = models.BooleanField(default=False)
    is_pop_up = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        # return str(self.id) + str(self.heading)
        return 'Widget #' + str(self.id) + ' with type ' + str(dict(WIDGET_CHOICES).get(self.widget_type)) if not self.heading else \
            str(self.heading) + ' - widget #' + str(self.id)

    def get_widget_type(self):
        widgetDict = dict(WIDGET_CHOICES)
        return widgetDict.get(self.widget_type)


    def get_widget_data(self):
        data_dict = {}
        for field in self._meta.fields:
            data_dict[field.name] = getattr(self, field.name)

        if self.widget_type == 3:
            related_arts = self.related_article.filter(status=1)
            related_arts = related_arts[: 5]
            data_dict.update({
                "related_arts": related_arts,
            })

        if self.iw:
            data_dict.update({
                'indexer_heading': self.iw.heading,
            })
            data_dict['column_headings'] = OrderedDict(self.iw.columnheading_set.values_list('column', 'name'))
            data_dict['column_data'] = {}
            max_row = 4
            data_dict['max_row'] = max_row
            flag = False

            for key, value in data_dict['column_headings'].items():
                queryset = self.iw.indexcolumn_set.filter(column=key)
                if queryset.count() > max_row:
                    flag = True
                data_dict['column_data'].update({key: OrderedDict(queryset.values_list('name', 'url'))})
            data_dict['view_more_index'] = flag

        return data_dict

    def get_template(self):
        if self.widget_type == 1:
            return 'text_format.html'
        elif self.widget_type == 2:
            return 'download_pdf.html'
        elif self.widget_type == 3:
            return 'related_blog.html'
        elif self.widget_type == 4:
            return 'practice_test.html'
        elif self.widget_type == 5:
            return 'expert_section.html'
        elif self.widget_type == 6:
            return 'request_call.html'
        elif self.widget_type == 7:
            return 'banner_ad.html'
        elif self.widget_type == 8:
            return 'index_widget.html'
        elif self.widget_type == 10:
            return 'button_widget.html'


class Page(AbstractCommonModel, AbstractSEO, ModelMeta):
    name = models.CharField(
        max_length=255, null=False, blank=False,
        verbose_name="Name", help_text='name for slug change')

    parent = models.ForeignKey(
        "self", verbose_name="Parent",
        null=True, blank=True,on_delete=models.CASCADE)

    slug = models.SlugField(
        max_length=255, unique=True, null=True, blank=True)

    widgets = models.ManyToManyField(
        Widget, through='PageWidget',
        verbose_name="Widgets", blank=True)

    total_view = models.PositiveIntegerField(default=0)
    total_download = models.PositiveIntegerField(default=0)
    total_share = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=False)
    show_menu = models.BooleanField(default=False)

    allow_comment = models.BooleanField(default=False)
    comment_count = models.PositiveIntegerField(default=0)

    publish_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    _metadata_default = ModelMeta._metadata_default.copy()
    
    _metadata = {
        'title': 'get_title',
        'description': 'get_description',
        'og_description': 'get_description',
        'published_time': 'publish_date',
        'keywords': 'get_keywords',
        'modified_time': 'last_modified_on',
        'url': 'get_full_url'
    }

    def __str__(self):
        return self.get_display_name

    def get_title(self):
        if not self.title.strip():
            name = self.get_display_name
            if self.parent:
                parent = self.parent.get_display_name
                return '{0} for {1} - Download Online - Shine Learning'.format(parent, name)
            return 'Free {0} - Download Online - Shine Learning'.format(name)
        return self.title
        
    @property
    def get_display_name(self):
        if self.heading:
            return self.heading
        elif self.parent:
            name = self.name
            parent = self.parent.name
            return '{0} for {1}'.format(parent, name)
        return self.name
    
    def get_keywords(self):
        if not self.meta_keywords:
            return settings.META_DEFAULT_KEYWORDS
        return self.meta_keywords.strip().split(",")

    def get_description(self):
        if not self.meta_desc.strip():
            name = self.name
            if self.parent:
                parent = self.parent.name
                return 'Free {0} for {1} - Get Online {0} recommended by experts for {1}. Download {0} samples in pdf or word doc'.format(parent,name)
            return 'Free {0} Online - Get {0} recommended by experts for experienced professionals or freshers. Download {0} samples in pdf or word doc'.format(name)
        return self.meta_desc
        
    def get_full_url(self):
        return self.build_absolute_uri(self.get_absolute_url())

    def get_absolute_url(self):
        if self.parent:
            return reverse('cms:page', kwargs={'parent_slug': self.parent.slug, 'child_slug':self.slug, 'pk': self.pk})
        return reverse('cms:page', kwargs={'slug': self.slug, 'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.get_title()
        if not self.meta_desc:
            self.meta_desc = self.get_description()
        if not self.meta_keywords:
            kw = ','.join(self.get_keywords())
            self.meta_keywords = kw
        if not self.heading:
            self.heading = self.get_display_name
        super(Page, self).save(*args, **kwargs)


class PageWidget(AbstractCommonModel):

    page = models.ForeignKey(Page,on_delete=models.CASCADE)
    widget = models.ForeignKey(Widget,on_delete=models.CASCADE)
    section = models.CharField(
        choices=SECTION, max_length=255,
        help_text='determine section of widget')
    ranking = models.IntegerField(
        default=0,
        help_text='determine ranking of widget')

    class Meta:
        # Comment this while initial migration
        # auto_created = True
        ordering = ['section', 'ranking']
        unique_together = ('page', 'widget')

    def __str__(self):
        # return str(self.id) + ' ' + self.title
        return 'Widget #' + str(self.widget.id) + ' with type ' + dict(WIDGET_CHOICES).get(self.widget.widget_type)


def get_upload_path_cms_doc(instance, filename):
    return "documents/{filename}".format(
        filename=filename)


class Document(models.Model):
    doc = models.FileField(
        "Document", max_length=200,
        upload_to=get_upload_path_cms_doc, null=False, blank=False)
    is_active = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    page = models.ForeignKey(Page,on_delete=models.CASCADE)

    class Meta:
        ordering = ['-priority', ]

    def __str__(self):
        return str(self.id)


class Comment(AbstractCommonModel):
    page = models.ForeignKey(Page,on_delete=models.CASCADE)
    candidate_id = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=False, blank=False)
    is_published = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)
    replied_to = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True,
        blank=True, related_name="comments")

    class Meta:
        ordering = ['-created_on', ]

    def __str__(self):
        # return str(self.id) + '_' + str(self.created_on.date())
        return 'Comment #' + str(self.id) + ' - ' + str(self.message[:12] if isinstance(self.message, str) else '')


class PageCounter(models.Model):
    page = models.ForeignKey(Page,on_delete=models.CASCADE)
    count_period = models.DateField()
    no_views = models.PositiveIntegerField(default=0)
    no_downloads = models.PositiveIntegerField(default=0)
    no_shares = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    added_on = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    modified_on = models.DateTimeField(
        auto_now=True, null=True, blank=True)

    class Meta:
        unique_together = ('page', 'count_period')
        ordering = ['-count_period']

    def __str__(self):
        return str(self.count_period)
