from django.utils import timezone
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from seo.models import AbstractSEO
from meta.models import ModelMeta

from .functions import (
    get_upload_path_category,)


class AbstractAutoDate(models.Model):
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(AbstractAutoDate, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Category(AbstractAutoDate, AbstractSEO, ModelMeta):
    name = models.CharField(
        _('Name'), max_length=100,
        help_text=_('Unique name going to decide the slug'))
    slug = models.CharField(
        _('Slug'), unique=True,
        max_length=100, help_text=_('Unique slug'))
    description = models.TextField(
        _('Description'), blank=True, default='')
    banner = models.ImageField(
        _('Banner'), upload_to=get_upload_path_category,
        blank=True, null=True)
    icon = models.ImageField(
        _('Icon'), upload_to=get_upload_path_category,
        blank=True, null=True)
    parent = models.ForeignKey(
        _('Parent'), 'self',
        on_delete=models.SET_NULL,
        related_name='parent',
        null=True)
    sub_parent = models.ManyToManyField(
        _('Sub Parent'),
        'self', symmetrical=False,
        on_delete=models.SET_NULL,
        related_name='sub_parent',
        null=True)
    active = models.BooleanField(default=False)
    display_order = models.IntegerField(default=1)

    _metadata_default = ModelMeta._metadata_default.copy()
    _metadata_default['locale'] = 'dummy_locale'

    _metadata = {
        'title': 'title',
        'description': 'get_description',
        'og_description': 'get_description',
        'keywords': 'get_keywords',
        'published_time': 'created',
        'modified_time': 'modified',
        'url': 'get_full_url',
    }

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ("-modified", "-created")
        get_latest_by = 'created'

    def __str__(self):
        return self.name

    def get_keywords(self):
        return self.meta_keywords.strip().split(",")

    def get_description(self):
        description = self.meta_desc
        if not description:
            description = self.description
        return description.strip()

    def get_full_url(self):
        return self.build_absolute_uri(self.get_absolute_url())

    def get_absolute_url(self):
        return reverse('category-listing', kwargs={'slug': self.slug})

