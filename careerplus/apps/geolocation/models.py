from cities_light.abstract_models import (
    AbstractCity, AbstractRegion,
    AbstractCountry)
from django.utils.translation import ugettext_lazy as _
from cities_light.receivers import connect_default_signals
from django.db import models
from seo.models import AbstractAutoDate

CURRENCY_SYMBOL = (
    (0, 'Rs.'),
    (1, '$'),
    (2, 'AED'),
    (3, 'GBP'),)


class Currency(AbstractAutoDate):
    name = models.CharField(
        _('Name'), max_length=100,
        help_text=_('Name of Currency'))
    value = models.PositiveIntegerField(
        _('Symbol'),
        help_text=_('Symbol'),
        choices=CURRENCY_SYMBOL,
        default=0)
    exchange_rate = models.DecimalField(
        _('Exchange'),
        max_digits=8, decimal_places=2,
        default=0.0)
    offset = models.DecimalField(
        _('Offset'),
        max_digits=8, decimal_places=2,
        default=0.0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Country(AbstractCountry):
    currency = models.ForeignKey(
        Currency,
        verbose_name=_('Currency'),
        on_delete=models.SET_NULL,
        related_name='countrycurrency',
        null=True)
    active = models.BooleanField(
        default=True)

    profile_url = models.CharField(
        max_length=400,
        null=True,
        blank=True,
        help_text='comma separated(,) profile url, e.g. www.test1.com, www.test2.com')


connect_default_signals(Country)


class Region(AbstractRegion):
    code_region = models.CharField(
        max_length=40)
    active = models.BooleanField(
        default=True)


connect_default_signals(Region)


class State(AbstractAutoDate):
    """
    Base State model.
    """

    name = models.CharField(max_length=200, db_index=True)
    country = models.ForeignKey(Country)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('country', 'name'),)
        verbose_name = 'State'
        verbose_name_plural = 'States'

    def get_display_name(self):
        return '%s, %s' % (self.name, self.country.name)


class City(AbstractCity):
    code_city = models.CharField(
        max_length=40)
    timezone = models.CharField(max_length=40)
    active = models.BooleanField(
        default=True)


connect_default_signals(City)
