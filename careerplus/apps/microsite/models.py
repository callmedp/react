from django.db import models
from django.conf import settings
import logging
from .config import TYPE_OF_PAGE


class MicrositeBanner(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False)
    image = models.ImageField(max_length=200, upload_to="microsite/banner")
    image_alt = models.CharField(max_length=255, null=True, blank=False)
    active = models.BooleanField(default=False)
    url = models.URLField(null=True, blank=True, help_text='Append http://')
    position = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        super(MicrositeBanner, self).save(*args, **kwargs)

    def get_low_image(self, quality):
        try:
            if self.image:
                extension = self.image.extension
                return self.image.path.split(extension)[0] + "_" + quality + extension
        except Exception as e:
            logging.getLogger('error_log').error('unable to get low image%s' % str(e))
            pass
        return ""


class PartnerPage(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    type_of_page = models.PositiveSmallIntegerField(choices=TYPE_OF_PAGE)
    banner_image = models.ManyToManyField(MicrositeBanner, blank=True)
    
    def __str__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        from .common import SaveSlug
        self.slug = SaveSlug().save_slug(self.slug, self.name)
        return super(PartnerPage, self).save(*args, **kwargs)


class MicroSite(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    home_page = models.ForeignKey(PartnerPage, null=True, blank=True, related_name='home_page',on_delete=models.PROTECT)
    listing_page = models.ForeignKey(PartnerPage, null=True, blank=True, related_name='listing_page',on_delete=models.PROTECT)
    detail_page = models.ForeignKey(PartnerPage, null=True, blank=True, related_name='detail_page',on_delete=models.PROTECT)
    active = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.name

    def save(self, *args, **kwargs):
        from .common import SaveSlug
        self.slug = SaveSlug().save_slug(self.slug, self.name)
        return super(MicroSite, self).save(*args, **kwargs)


class PartnerTestimonial(models.Model):
    microsite = models.ForeignKey(MicroSite,on_delete=models.PROTECT)
    name_of_user = models.CharField(max_length=255, null=True, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name='User(if any)',on_delete=models.PROTECT)
    image = models.ImageField(max_length=200, upload_to="microsite/testimonial")
    title = models.CharField(max_length=255, null=True, blank=True)
    review = models.TextField(max_length=1024)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    added_on = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.microsite.name, self.name_of_user)


class PartnerFaq(models.Model):
    microsite = models.ForeignKey(MicroSite,on_delete=models.PROTECT)
    question = models.CharField(max_length=1024, null=True, blank=False)
    answer = models.TextField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.microsite.name, self.question)
