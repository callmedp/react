#python imports
import django,logging,sys,os
from datetime import datetime
#django imports

#Settings imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careerplus.config.settings_live') 
#local imports

#inter app imports

#third party imports
from geolocation.models import Country

from django.conf import settings
from django.core.mail import EmailMessage

TEAM_EMAILS = ["Nidhish Sharma<nidhish.sharma@hindustantimes.com>",
               "Priya Kharb<Priya.Kharb@hindustantimes.com> ",
               "Sahil Singla<sahil.singla@hidustantimes.com>",
               "Heena Afshan<heena.afshan@hindustantimes.com>"
               ]

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



def send_failure_mail(cron_name,exception):
    html_content =  """<html><title></title><body><h3>Following CRON has Failed, please act on it as soon as possible.</h3><br>
                Cron Name: {} <br>
                Date: {}<br>
                Reason: {}<br>
                </body></html>""".format(cron_name.title(),datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),exception)
    email = EmailMessage(
        subject = "Cron in Shine Learning has failed", body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL, to=TEAM_EMAILS)
    email.content_subtype = "html"
    logging.getLogger('error_log').error('CRON: {} HAS FAILED'.format(cron_name.title()))
    return email.send(fail_silently=False)