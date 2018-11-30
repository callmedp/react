from geolocation.models import Country,Currency
import factory
import datetime



class CurrencyFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Currency
        django_get_or_create = ('name','value')

    name = 'rupees'
    value = 0


class CountryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Country
        django_get_or_create = ('phone',)

    currency = factory.SubFactory(CurrencyFactory)

    name='india'
    code2='91'
    code3 ='ind'
    phone='91'










