import re

from django.db import models
from django.contrib.sites.models import Site
from django.conf import settings
from django.urls import reverse
# from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


from meta.models import ModelMeta
from ckeditor_uploader.fields import RichTextUploadingField
from decimal import Decimal

from core.models import AbstractCommonModel
from seo.models import AbstractSEO

from .config import STATUS

SITE_TYPE = ((1, 'ShineLearning'),(2, 'TalentEconomy'),(3, 'Both'))

class Category(AbstractCommonModel, AbstractSEO, ModelMeta):
    name = models.CharField(
        max_length=255, null=False, blank=False, unique=True)
    slug = models.SlugField(
        ('Slug'), unique=True, max_length=255,
        blank=True, null=True, help_text=("Used to build the category's URL."))
    visibility = models.PositiveIntegerField(
        _('Site Visibilty'),
        choices=SITE_TYPE,
        default=1,
        help_text=_('sites where blog published.'))
    image = models.FileField(
        "Image", max_length=200, upload_to="images/blog/category/",
        blank=True, null=True, help_text='use this category image')
    image_alt = models.CharField(
        max_length=100, null=True, blank=True)
    
    is_active = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    _metadata_default = ModelMeta._metadata_default.copy()
    _metadata_default['locale'] = 'dummy_locale'

    _metadata = {
        'title': 'get_title',
        'description': 'get_description',
        'og_description': 'get_description',
        'keywords': 'get_keywords',
        'published_time': 'publish_date',
        'modified_time': 'last_modified_on',
        'url': 'get_full_url'
    }

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.name + ' - Career Articles @ Learning.Shine'
        if not self.heading:
            self.heading = self.name
        if not self.meta_desc:
            self.meta_desc = 'Read Latest Articles on ' + self.name + '. Find the Most Relevant Information, News and other career guidance for ' + self.name +' at learning.shine'
        if self.id:
            self.url = 'https://' + settings.SITE_DOMAIN + self.get_absolute_url()
        super(Category, self).save(*args, **kwargs)

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
        return reverse('articles-by-category', kwargs={'slug': self.slug})

    def article_exists(self):
        q = self.primary_category.filter(status=1) | self.secondary_category.filter(status=1)
        if q.exists():
            return True
        return False


class Tag(AbstractCommonModel, AbstractSEO, ModelMeta):
    name = models.CharField(
        max_length=255, null=False, blank=False, unique=True)
    slug = models.SlugField(
        ('Slug'), unique=True, max_length=255,
        blank=True, null=True, help_text=("Used to build the tag's URL."))
    visibility = models.PositiveIntegerField(
        _('Site Visibilty'),
        choices=SITE_TYPE,
        default=1,
        help_text=_('sites where blog published.'))
    is_active = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    _metadata_default = ModelMeta._metadata_default.copy()
    _metadata_default['locale'] = 'dummy_locale'

    _metadata = {
        'title': 'get_title',
        'description': 'get_description',
        'og_description': 'get_description',
        'keywords': 'get_keywords',
        'published_time': 'publish_date',
        'modified_time': 'last_modified_on',
        'url': 'get_full_url'
    }

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.name + ' - Career Articles @ Learning.Shine'
        if not self.heading:
            self.heading = self.name
        if not self.meta_desc:
            self.meta_desc = 'Read Latest Articles on ' + self.name + '. Find the Most Relevant Information, News and other career guidance for ' + self.name +' at learning.shine'
        if self.id:
            self.url = 'https://' + settings.SITE_DOMAIN + self.get_absolute_url()
        super(Tag, self).save(*args, **kwargs)

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
        return reverse('blog:articles-by-tag', kwargs={'slug': self.slug})


class Author(AbstractCommonModel, AbstractSEO, ModelMeta):
    name = models.CharField(
        max_length=255, null=False, blank=False, unique=True)
    slug = models.SlugField(
        ('Slug'), unique=True, max_length=255,
        blank=True, null=True, help_text=("Used to build the author's URL."))
    visibility = models.PositiveIntegerField(
        _('Site Visibilty'),
        choices=SITE_TYPE,
        default=1,
        help_text=_('sites where blog published.'))
    image = models.FileField(
        "Profile Image", max_length=200, upload_to="images/blog/author/",
        blank=True, null=True, help_text='use this category image')
    image_alt = models.CharField(
        max_length=100, null=True, blank=True)
    about = models.TextField(
        _('About Author'),
        blank=True, default='')
    designation = models.CharField(
        _('Designation'), max_length=255, blank=True)
    company = models.CharField(
        _('Company'), max_length=255, blank=True)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        help_text='for user or writer')
    
    is_active = models.BooleanField(default=False)
    

    _metadata_default = ModelMeta._metadata_default.copy()
    # _metadata_default['locale'] = 'dummy_locale'

    # _metadata = {
    #     'title': 'get_title',
    #     'description': 'get_description',
    #     'og_description': 'get_description',
    #     'keywords': 'get_keywords',
    #     'published_time': 'publish_date',
    #     'modified_time': 'last_modified_on',
    #     'url': 'get_full_url'
    # }

    # class Meta:
    #     ordering = ['priority']

    def __str__(self):
        return self.name

class Blog(AbstractCommonModel, AbstractSEO, ModelMeta):
    
    name = models.CharField(
        ('Name'), max_length=200, blank=False,
        help_text=("Set name for slug generation."))
    p_cat = models.ForeignKey(
        Category, related_name='primary_category',
        blank=False, null=False)
    sec_cat = models.ManyToManyField(
        Category, related_name='secondary_category',
        blank=True)
    slug = models.SlugField(
        ('Slug'), unique=True, max_length=255,
        blank=True, null=True, help_text=("Used to build the tag's URL."))
    image = models.FileField(
        "Image", max_length=200, upload_to="images/blog/",
        blank=True, null=True, help_text='use this banner image')
    image_alt = models.CharField(
        max_length=100, null=True, blank=True)
    content = RichTextUploadingField(
        default="", blank=True, null=True,
        help_text=("content for blog."))
    tags = models.ManyToManyField(
        Tag, blank=True)
    visibility = models.PositiveIntegerField(
        _('Site Visibilty'),
        choices=SITE_TYPE,
        default=1,
        help_text=_('sites where blog published.'))
    summary = models.TextField(
        _('Summary Article'),
        blank=True, default='')
    author = models.ForeignKey(
        Author, null=True, blank=True,
        help_text='for author')
    
    # sites = models.ManyToManyField(Site, blank=True, related_name='related_sites',
    #     help_text=("sites where blog published."))
    
    #do not use#
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        help_text='for user or writer')
    
    status = models.PositiveIntegerField(choices=STATUS, default=0)
    allow_comment = models.BooleanField(default=False)

    no_comment = models.PositiveIntegerField(default=0)
    comment_moderated = models.PositiveIntegerField(default=0)
    no_views = models.PositiveIntegerField(default=0)
    no_shares = models.PositiveIntegerField(default=0)
    score = models.DecimalField(max_digits=10, default=0,
        decimal_places=2, help_text=("popularity score"))

    publish_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    _metadata_default = ModelMeta._metadata_default.copy()
    _metadata_default['locale'] = 'dummy_locale'

    _metadata = {
        'title': 'get_title',
        'description': 'get_description',
        'og_description': 'get_description',
        'keywords': 'get_keywords',
        'published_time': 'publish_date',
        'modified_time': 'last_modified_on',
        'url': 'get_full_url'
    }

    class Meta:
        ordering = ['-score', '-publish_date']
        permissions = (
            ("console_change_learning_article", "Can Change Learning Article From Console"),
            ("console_change_talent_article", "Can Change Talent Article From Console"),
        )

    def __str__(self):
        return str(self.id) + '_' + self.name

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.name + ' - Learning.Shine'
        if not self.heading:
            self.heading = self.name
        if not self.meta_desc:
            # desc = mark_safe(self.content)
            desc = re.sub(re.compile('<.*?>'), '', self.content)
            self.meta_desc = 'Read Article on ' + self.name + '.' + desc[:200]
        if not self.display_name:
            self.display_name = self.name
        if self.id:
            self.url = 'https://' + settings.SITE_DOMAIN + self.get_absolute_url()
        super(Blog, self).save(*args, **kwargs)

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
        return reverse('blog:articles-deatil', kwargs={'slug': self.slug, 'pk': self.pk})

    def update_score(self):
        score = Decimal(self.no_views) * Decimal(0.9)
        score += Decimal(self.no_shares) * Decimal(0.7)
        score = Decimal(round(score, 2))
        self.score = score
        self.save()

    @property
    def get_status(self):
        statusD = dict(STATUS)
        return statusD.get(self.status)

    @property
    def display_name(self):
        return self.heading if self.heading else self.name


class Comment(AbstractCommonModel):
	blog = models.ForeignKey(Blog)
	candidate_id = models.CharField(max_length=255, null=True)
	name = models.CharField(max_length=255, null=True, blank=True)
	message = models.TextField(null=False, blank=False)
	is_published = models.BooleanField(default=False)
	is_removed = models.BooleanField(default=False)
	replied_to = models.ForeignKey("self", on_delete=models.CASCADE, null=True,
		blank=True, related_name="comments")

	class Meta:
		ordering = ['-created_on', ]

	def __str__(self):
		return str(self.id) + '_' + str(self.created_on.date())


