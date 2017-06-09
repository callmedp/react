from django.db.models import Q

from geolocation.models import Country


def get_country_code():
    try:
        country_choices = []
        for m in Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact='')):
            country_choices.append((m.phone, m.phone))
    except:
        country_choices = ['91']
    return country_choices
    

def default_code():
    return '91'


def get_country():
    try:
        CHOICE_COUNTRY = []
        for m in Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact='')):
            CHOICE_COUNTRY.append((m.phone, m.name))
    except:
        CHOICE_COUNTRY = ['91']
    return CHOICE_COUNTRY


def default_country():
    return '91'