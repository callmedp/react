#python imports
import logging

#django imports

#local imports

#inter app imports

#third party imports
from geolocation.models import Country


def get_country_obj(country_code2):
    try:
        country_objs = Country.objects.filter(code2=country_code2, active=True)
        country_obj = country_objs[0]
    except Exception as e:
        logging.getLogger('error_log').error('unable to get country object %s'%str(e))
        country_obj = Country.objects.get(phone='91', active=True)
    return country_obj


def set_session_currency(country_obj, request):
    session_curreency = request.session.get('country_currency', None)
    if session_curreency and country_obj and country_obj.currency and session_curreency == country_obj.currency.value:
        pass
    elif country_obj:
        if country_obj.currency:
            session_curreency = country_obj.currency.value
        else:
            session_curreency = 1
    else:
        session_curreency = 1

    request.session['country_currency'] = session_curreency


def set_session_country(country_obj, request):
    session_country = request.session.get('country_code2', None)
    if session_country and country_obj.code2 == session_country:
        pass
    else:
        request.session['country_code2'] = country_obj.code2

    set_session_currency(country_obj, request)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_client_device_type(request):
    agent_data = request.META.get('HTTP_USER_AGENT','').lower()
    device_type = "DESKTOP"
    if "android" in agent_data or "ios" in agent_data:
         device_type = "MOBILE"
    return device_type



    