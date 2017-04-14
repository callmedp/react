from django.db import models
from django.contrib.sites.models import Site
from django.conf import settings

from meta.models import ModelMeta
from ckeditor_uploader.fields import RichTextUploadingField
from decimal import Decimal

from cms.models import AbstractCommonModel
from seo.models import AbstractSEO

from .config import STATUS


class Category(AbstractCommonModel, AbstractSEO, ModelMeta):
	name = models.CharField(max_length=255, null=False, blank=False, unique=True)
	slug = models.SlugField(('Slug'), unique=True, max_length=255,
		blank=True, null=True, help_text=("Used to build the category's URL."))
	is_active = models.BooleanField(default=False)
	priority = models.IntegerField(default=0)

	class Meta:
		ordering = ['-priority']

	def __str__(self):
		return self.name


class Tag(AbstractCommonModel, AbstractSEO, ModelMeta):
	name = models.CharField(max_length=255, null=False, blank=False, unique=True)
	slug = models.SlugField(('Slug'), unique=True, max_length=255,
		blank=True, null=True, help_text=("Used to build the tag's URL."))
	is_active = models.BooleanField(default=False)
	priority = models.IntegerField(default=0)

	def __str__(self):
		return self.name


class Blog(AbstractCommonModel, AbstractSEO, ModelMeta):
	name = models.CharField(('Name'), max_length=200, blank=False,
		help_text=("Set title for blog."))
	p_cat = models.ForeignKey(Category, related_name='primary_category', blank=False, null=False)
	sec_cat = models.ManyToManyField(Category, related_name='secondary_category', blank=True)
	slug = models.SlugField(('Slug'), unique=True, max_length=255,
		blank=True, null=True, help_text=("Used to build the tag's URL."))
	image = models.FileField("Image", max_length=200, upload_to="images/blog/",
    	blank=True, null=True, help_text='use this banner image')
	image_alt = models.CharField(max_length=100, null=True, blank=True)
	content = RichTextUploadingField(default="", blank=True, null=True,
		help_text=("content for blog."))
	tags = models.ManyToManyField(Tag, blank=True)
	sites = models.ManyToManyField(Site, related_name='related_sites',
		help_text=("sites where blog published."))

	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
		help_text='for user or writer')
	writer_name = models.CharField(max_length=100, blank=True, null=True)
	status = models.PositiveIntegerField(choices=STATUS, default=0)
	allow_comment = models.BooleanField(default=False)

	no_comment = models.PositiveIntegerField(default=0)
	no_views = models.PositiveIntegerField(default=0)
	no_shares = models.PositiveIntegerField(default=0)
	score = models.DecimalField(max_digits=10, default=0,
        decimal_places=2, help_text=("popularity score"))

	publish_date = models.DateTimeField(null=True, blank=True)
	expiry_date = models.DateTimeField(null=True, blank=True)

	class Meta:
		ordering = ['-score', '-publish_date']

	def __str__(self):
		return str(self.id) + '_' + self.name

	def update_score(self):
		score = Decimal(self.no_views) * Decimal(0.9)
		score += Decimal(self.no_shares) * Decimal(0.7)
		score = Decimal(round(score, 2))
		self.score = score
		self.save()