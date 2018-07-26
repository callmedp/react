from django.db import models
from seo.models import AbstractAutoDate
from geolocation.models import Country


LEAD_LOCATION = (
    (0, 'Default'),
    (1, 'Skill Page'),
    (2, 'Course Detail Page'),
    (3, 'Contact Us Page'),
    (4, 'SEM'),  # marketing pages
    (6, 'Chat Lead'),
    (7, 'CMS Page'),
    (8, 'Resume Detail Page'),
    (20, 'Miss Call Lead'),
    (21, 'AdServerLead'),
    (26, 'Email Marketing Course Leads'),
    (27, 'Email Marketing Resume Leads'),
    (22, 'CartLead'),
    (23, 'Overlay'),
)

DEFAULT_SLUG_SOURCE = (
    (0, ''),
    (1, 'skillleads'),
    (2, 'courseonline'),
    (3, ''),
    (4, 'semdefault'),  # marketing pages
    (6, 'defaultchatleads'),
    (7, 'cmsonline'),
    (8, 'resumeonline'),
    (21, 'adserverdefault'),
    (20, 'missedcalldefault'),
    (26, 'coursemailerdefault'),
    (27, 'resmdefault'),  # resume mailer default
    (22, 'cartleads'),
)


DEVICE = ((0, 'Desktop'), (1, 'Mobile'))


class UserQuries(AbstractAutoDate):
    """
    Contains the data for candidate who wants to contact, data got from call_me
    """
    name = models.CharField(
        max_length=255, null=True, blank=True)
    email = models.CharField(
        max_length=255, null=True, blank=True)
    country = models.ForeignKey(
        Country, null=True)
    phn_number = models.CharField(
        max_length=50)
    message = models.TextField()
    lead_created = models.BooleanField(default=False)
    lead_source = models.SmallIntegerField(choices=LEAD_LOCATION, default=0)
    product = models.CharField(max_length=100, null=True, blank=True)
    product_id = models.IntegerField(null=True, blank=True)
    path = models.CharField(
        max_length=255, null=True, blank=True)
    medium = models.SmallIntegerField(choices=DEVICE, default=0)
    source = models.CharField(
        max_length=255, null=True, blank=True)
    utm_parameter = models.TextField(
        blank=True,
        default='')
    campaign_slug = models.CharField(
        max_length=255, null=True, blank=True)
    inactive = models.BooleanField(default=False)
    timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'User Queries'
        ordering = ['-modified']

    def get_lead_source(self):
        return dict(LEAD_LOCATION).get(self.lead_source)

    def get_medium(self):
        return dict(DEVICE).get(self.medium)


SOURCE_CHOICE = (
    (21, 'AdServerLead'),
)


class AdServerLead(models.Model):
    email = models.EmailField(max_length=255, null=True, blank=True)
    country_code = models.CharField(
        max_length=10, verbose_name='Country Code', default='91')
    mobile = models.CharField(max_length=15, verbose_name='Mobile')
    timestamp = models.DateTimeField(null=True, blank=True)
    source = models.PositiveSmallIntegerField(
        choices=SOURCE_CHOICE, default=21)
    url = models.CharField(max_length=800, null=True, blank=True)
    created = models.BooleanField(default=False)
    inactive = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_on = models.DateTimeField(auto_now=True, null=True, blank=True)
    utm_parameter = models.TextField(
        ('utm_parameter'),
        blank=True,
        default='')

    def __str__(self):
        return str(self.mobile) + ' ' + str(self.timestamp.date())
