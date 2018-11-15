from django.db import models
from django.db import IntegrityError
from django.core.exceptions import ImproperlyConfigured
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
import logging
class AbstractAutoDate(models.Model):
    created = models.DateTimeField(editable=False, auto_now_add=True,)
    modified = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        abstract = True


class AbstractSEO(models.Model):
    """
    This class automatically genarate unique slug using name field with handling of collision in DB. It also manages SEO elements at Models/Objects Levels. 
    * url_value_name - the value to slugify, default 'name'
    * url_slug_name - the field to store the slugified value in, default 'slug'
    * max_interations - how many iterations to search for an open slug before raising IntegrityError, default 1000
    * separator - the character to put in place of spaces and other non url friendly characters, default '-'

    """
    url = models.CharField(
        _('Url'), max_length=255, blank=True)
    title = models.CharField(
        _('Title'), max_length=255, blank=True)
    meta_desc = models.TextField(
        _('Meta Description'), blank=True, default='')
    meta_keywords = models.TextField(
        _('Keywords'), blank=True, default='')
    heading = models.CharField(
        _('H1'), max_length=255, blank=True)
    image_alt = models.CharField(
        _('Image Alt'), max_length=255, blank=True)
    
    class Meta:
        abstract = True

    def get_domain(self):
        if not settings.SITE_DOMAIN:
            raise ImproperlyConfigured('SITE_DOMAIN is not set')
        return settings.SITE_DOMAIN

    def get_protocol(self):
        if not settings.SITE_PROTOCOL:
            raise ImproperlyConfigured('SITE_PROTOCOL is not set')
        return settings.SITE_PROTOCOL

    def get_full_url(self, url):
        if not url:
            return None
        if url.startswith('http'):
            return url
        if url.startswith('//'):
            return '%s:%s' % (
                self.get_protocol(),
                url
            )
        if url.startswith('/'):
            return '%s://%s%s' % (
                self.get_protocol(),
                self.get_domain(),
                url
            )
        return '%s://%s/%s' % (
            self.get_protocol(),
            self.get_domain(),
            url
        )

    def save(self, *args, **kwargs):
        pk_field_name = self._meta.pk.name
        url_value_name = getattr(self, 'url_value_name', 'name')
        url_slug_name = getattr(self, 'url_slug_name', 'slug')
        url_slug_fix = getattr(self, 'url_slug_fix', 'fixed_slug')
        
        max_interations = getattr(self, 'max_iterations', 1000)
        slug_separator = getattr(self, 'separator', '-')
        # fields, query set, other setup variables
        fix_field = getattr(self, url_slug_fix,False)
        if not fix_field:    
            slug_field = self._meta.get_field(url_slug_name)
            slug_len = slug_field.max_length
            queryset = self.__class__.objects.all()
            # if the pk of the record is set, exclude it from the slug search
            current_pk = getattr(self, pk_field_name)
            if current_pk:
                queryset = queryset.exclude(**{pk_field_name: current_pk})

            # setup the original slug, and make sure it is within the allowed length
            slug = slugify(getattr(self, url_value_name))
            if slug_len:
                slug = slug[:slug_len]
            original_slug = slug

            # iterate until a unique slug is found, or max_iterations
            counter = 2
            while queryset.filter(**{url_slug_name: slug}).count() > 0 and counter < max_interations:
                slug = original_slug
                suffix = '%s%s' % (slug_separator, counter)
                if slug_len and len(slug) + len(suffix) > slug_len:
                    slug = slug[:slug_len - len(suffix)]
                slug = '%s%s' % (slug, suffix)
                counter += 1

            if counter == max_interations:
                raise IntegrityError('Unable to locate unique slug')

            setattr(self, slug_field.attname, slug)

        super(AbstractSEO, self).save(*args, **kwargs)
