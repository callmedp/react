from django.db import models
from django.conf import settings

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


from .config import STATUS, WIDGET_CHOICES, SECTION, COLUMN_TYPE
# Create your models here.


class AbstractCommonModel(models.Model):
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
		blank=True, related_name="%(app_label)s_%(class)s_created_by",
        related_query_name="%(app_label)s_%(class)ss",)
	created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	last_modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
		blank=True, related_name="%(app_label)s_%(class)s_last_modified_by",
        related_query_name="%(app_label)s_%(class)ss",)
	last_modified_on = models.DateTimeField(auto_now=True, null=True, blank=True)

	class Meta:
		abstract = True


class PageCategory(AbstractCommonModel):
	name = models.CharField(max_length=255, unique=True)
	parent = models.ForeignKey('self', null=True, blank=True)
	slug = models.SlugField(verbose_name='Slug', unique=True, max_length=255,
		help_text=("Used to build the category's URL."))
	is_active = models.BooleanField(default=False)
	show_menu = models.BooleanField(default=False)

	def __str__(self):
		return self.name


class Tag(AbstractCommonModel):
	name = models.CharField(max_length=255, unique=True)
	parent = models.ForeignKey('self', null=True, blank=True)
	slug = models.SlugField(verbose_name='Slug', unique=True, max_length=255,
		help_text=("Used to build the category's URL."))
	is_active = models.BooleanField(default=False)
	show_menu = models.BooleanField(default=False)

	def __str__(self):
		return self.name


class IndexerWidget(AbstractCommonModel):
	name = models.CharField(max_length=100, null=False, blank=False)
	heading = models.CharField(max_length=255, null=True, blank=True)

	def __str__(self):
		return '%s' % self.name


class ColumnHeading(models.Model):
	column = models.PositiveIntegerField(choices=COLUMN_TYPE)
	name = models.CharField(max_length=255)
	indexer = models.ForeignKey(IndexerWidget)

	def __str__(self):
		return '%s' % self.name


class IndexColumn(models.Model):
	indexer = models.ForeignKey(IndexerWidget)
	column = models.PositiveIntegerField(choices=COLUMN_TYPE)
	url = models.CharField(max_length=2048, null=True, blank=True)
	name = models.CharField(max_length=255)

	def __str__(self):
		return '%s' % self.name


# class ExpertComment(AbstractCommonModel):
# 	writer = models.ForeignKey(settings.AUTH_USER_MODEL)
# 	display_name = models.CharField(max_length=100, null=False, blank=False)
# 	writer_designation = models.CharField(max_length=255)
# 	image = models.FileField("Image", max_length=200,
# 		upload_to="images/cms/page/", blank=True, null=True)
# 	description = models.TextField()
# 	# page = models.ForeignKey(Page)
# 	active = models.BooleanField()

# 	def __str__(self):
# 		return '%s' % self.writer


class Widget(AbstractCommonModel):
	widget_type = models.PositiveIntegerField(choices=WIDGET_CHOICES, null=False, blank=False)
	name = models.CharField(max_length=200, null=False, blank=False)
	template_name = models.CharField(max_length=1024, null=True, blank=True)
	heading = models.CharField(max_length=1024, null=True, blank=True)
	redirect_url = models.URLField(null=True, blank=True,
		verbose_name='Re-directing Url',
    	help_text='Append http://.')

	image = models.FileField("Image", max_length=200, upload_to="images/cms/widget/",
    	blank=True, null=True, help_text='use this for Resume help')
	image_alt = models.CharField(max_length=100, null=True, blank=True)

	description = RichTextUploadingField(null=True, blank=True)
	document_upload = models.FileField("Document", max_length=200,
    	upload_to="documents/cms/widget/", blank=True, null=True)

	upload_template = models.FileField(upload_to='templates/includes/cms/',
    	max_length=1024, blank=True, null=True)

	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
		help_text='for user or writer')
	display_name = models.CharField(max_length=100, null=True, blank=True)
	writer_designation = models.CharField(max_length=255, null=True, blank=True)

	iw = models.ForeignKey(IndexerWidget, null=True, blank=True,
		verbose_name='Indexer Widget')

	is_external = models.BooleanField(default=False)
	is_pop_up = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)

	def __str__(self):
		return str(self.id) + str(self.name)

	def get_widget_data(self):
		data_dict = {}
		for field in self._meta.fields:
			data_dict[field.name] = getattr(self, field.name)

		if self.iw:
			data_dict.update({
				'indexer_heading': self.iw.heading,
			})
			data_dict['column_headings'] = dict(self.iw.columnheading_set.values_list('column', 'name'))
			data_dict['column_data'] = {}
			for key, value in data_dict['column_headings'].items():
				data_dict['column_data'].update({key: dict(self.iw.indexcolumn_set.filter(column=key).values_list('name', 'url'))})

		return data_dict


class Page(AbstractCommonModel):
	title = models.CharField(max_length=255, null=False, blank=False,
		verbose_name="Title", help_text='The H1 heading for the page.')
	category = models.ForeignKey(PageCategory, null=True, blank=False)
	description = RichTextUploadingField(null=False, verbose_name="Description",
		blank=True, default="", help_text='The content of the page containing \
		the h2 and other content about the product.')
	short_desc = RichTextUploadingField(null=False, verbose_name="Short Description",
		blank=True, help_text='Very short description of the page in about 50 \
		 words', default="")
	parent = models.ForeignKey("self", verbose_name="Parent",
		null=True, blank=True)
	slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

	tag = models.ManyToManyField(Tag, verbose_name="Tags",
		blank=True, help_text='Add the tags to make some relation \
		between the pages.', related_name="related_tag")
	related_pages = models.ManyToManyField("self", blank=True,
		verbose_name='Realted Page')

	widgets = models.ManyToManyField(Widget, through='PageWidget',
        verbose_name="Widgets", blank=True)

	url = models.URLField(blank=True, null=True)

	total_view = models.PositiveIntegerField(default=0)
	total_download = models.PositiveIntegerField(default=0)
	total_share = models.PositiveIntegerField(default=0)
	status = models.PositiveIntegerField(choices=STATUS, default=0)
	active = models.BooleanField(default=False)
	show_menu = models.BooleanField(default=False)

	allow_comment = models.BooleanField(default=False)
	comment_count = models.PositiveIntegerField(default=0)

	publish_date = models.DateTimeField(null=True, blank=True)
	expiry_date = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return str(self.id) + ' ' + self.title	


class PageWidget(AbstractCommonModel):
	page = models.ForeignKey(Page)
	widget = models.ForeignKey(Widget)
	section = models.CharField(choices=SECTION, max_length=255,
		help_text='determine section of widget')
	ranking = models.IntegerField(default=0,
		help_text='determine ranking of widget')

	class Meta:
		ordering = ['section', '-ranking']
		unique_together = ('page', 'widget')


class Document(models.Model):
	doc = models.FileField("Document", max_length=200,
		upload_to="documents/cms/page/", null=False, blank=False)
	is_active = models.BooleanField(default=False)
	priority = models.IntegerField(default=0)
	page = models.ForeignKey(Page)

	class Meta:
		ordering = ['-priority', ]

	def __str__(self):
		return str(self.id)


class Comment(AbstractCommonModel):
	page = models.ForeignKey(Page)
	message = models.TextField(null=False, blank=False)
	is_published = models.BooleanField(default=False)
	is_removed = models.BooleanField(default=False)
	replied_to = models.ForeignKey("self", on_delete=models.CASCADE, null=True,
		blank=True, related_name="comments")

	class Meta:
		ordering = ['-created_on', ]

	def __str__(self):
		return str(self.id) + '_' + str(self.submit_date.date())


class PageCounter(models.Model):
	page = models.ForeignKey(Page)
	count_period = models.DateField()
	no_views = models.PositiveIntegerField(default=0)
	no_downloads = models.PositiveIntegerField(default=0)
	no_shares = models.PositiveIntegerField(default=0)
	added_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	modified_on = models.DateTimeField(auto_now=True, null=True, blank=True)

	class Meta:
		unique_together = ('page', 'count_period')
		ordering = ['-count_period']

	def __str__(self):
		return str(self.count_period)
