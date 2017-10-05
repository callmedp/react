from django.db import models
from django.urls import reverse
from django.core.files.storage import FileSystemStorage

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
    indexer = models.ForeignKey(IndexerWidget)

    def __str__(self):
        return '%s' % self.name


class IndexColumn(models.Model):
    indexer = models.ForeignKey(IndexerWidget)
    column = models.PositiveIntegerField(choices=COLUMN_TYPE)
    url = models.CharField(
        max_length=2048, null=True,
        blank=True,
        help_text='provide full url with valid protocol https:// or http://')
    name = models.CharField(max_length=255)

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
        verbose_name='Indexer Widget')

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
            data_dict['column_headings'] = dict(self.iw.columnheading_set.values_list('column', 'name'))
            data_dict['column_data'] = {}
            for key, value in data_dict['column_headings'].items():
                data_dict['column_data'].update({key: dict(self.iw.indexcolumn_set.filter(column=key).values_list('name', 'url'))})

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


class Page(AbstractCommonModel, AbstractSEO, ModelMeta):
    name = models.CharField(
        max_length=255, null=False, blank=False,
        verbose_name="Name", help_text='The H1 heading for the page.')

    parent = models.ForeignKey(
        "self", verbose_name="Parent",
        null=True, blank=True)

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
    _metadata_default['locale'] = 'dummy_locale'

    _metadata = {
        'title': 'get_title',
        'description': 'get_keywords',
        'og_description': 'get_description',
        'keywords': 'get_keywords',
        'published_time': 'publish_date',
        'modified_time': 'last_modified_on',
        'url': 'get_full_url'
    }

    def __str__(self):
        return 'Page #' + str(self.id) + ' - ' + str(self.name if isinstance(self.name, str) else '')

    def get_title(self):
        title = self.title
        if not self.title:
            title = self.name
        return title.strip()

    def get_keywords(self):
        return self.meta_keywords.strip().split(",")

    def get_description(self):
        description = self.meta_desc
        return description.strip()

    def get_full_url(self):
        return self.build_absolute_uri(self.get_absolute_url())

    def get_absolute_url(self):
        return reverse('cms:page', kwargs={'slug': self.slug, 'pk': self.pk})


class PageWidget(AbstractCommonModel):

    page = models.ForeignKey(Page)
    widget = models.ForeignKey(Widget)
    section = models.CharField(
        choices=SECTION, max_length=255,
        help_text='determine section of widget')
    ranking = models.IntegerField(
        default=0,
        help_text='determine ranking of widget')

    class Meta:
        # Comment this while initial migration
        # auto_created = True
        ordering = ['section', '-ranking']
        unique_together = ('page', 'widget')

    def __str__(self):
        # return str(self.id) + ' ' + self.title
        return 'Widget #' + str(self.widget.id) + ' with type ' + dict(WIDGET_CHOICES).get(self.widget.widget_type)


class Document(models.Model):
    doc = models.FileField(
        "Document", max_length=200,
        storage=my_store, null=False, blank=False)
    is_active = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    page = models.ForeignKey(Page)

    class Meta:
        ordering = ['-priority', ]

    def __str__(self):
        return str(self.id)

    def get_url(self):
        if self.doc:
            filename = self.doc.name
            url = '/download/' + filename
            return url


class Comment(AbstractCommonModel):
    page = models.ForeignKey(Page)
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
    page = models.ForeignKey(Page)
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
