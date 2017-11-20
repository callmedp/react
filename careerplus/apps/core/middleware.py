# python built-in imports
import logging
import re
import json
import urllib.parse
from datetime import datetime
from django.utils import timezone
from crmapi.tasks import addAdServerLead
from django_mobile import set_flavour

# django imports
from django_mobile.middleware import SetFlavourMiddleware
from django.utils.deprecation import MiddlewareMixin
from shine.core import ShineCandidateDetail
from django.conf import settings
from users.mixins import UserMixin
from core.api_mixin import AdServerShine
from .utils import set_session_country


class UpgradedSetFlavourMiddleware(MiddlewareMixin, SetFlavourMiddleware):
    """
    Makes middleware django 1.10 compatible
    """
    def __init__(self, get_response=None):
        super(UpgradedSetFlavourMiddleware, self).__init__(get_response)


class MobileDetectionMiddleware(object):
    http_accept_regex = re.compile(
        "application/vnd\.wap\.xhtml\+xml", re.IGNORECASE)

    def __init__(self):
        pass

    def process_request(self, request):
        is_mobile = False
        if request.META.get('HTTP_HOST') == settings.MOBILE_SITE_DOMAIN:
            is_mobile = True
        if is_mobile:
            set_flavour(settings.DEFAULT_MOBILE_FLAVOUR, request)
        else:
            set_flavour(settings.FLAVOURS[0], request)


class UpgradedMobileDetectionMiddleware(MiddlewareMixin, MobileDetectionMiddleware):
    """
    Makes middleware django 1.10 compatible
    """
    # TODO: Upgrade regex for tablet to be exempted
    def __init__(self, get_response=None):
        super(UpgradedMobileDetectionMiddleware, self).__init__(get_response)


class LearningShineMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        country_obj = UserMixin().get_client_country(request)
        set_session_country(country_obj, request)
        ad_content = request.GET.get('ad_content', '')
        if ad_content:
            ad_content = ad_content
            request.session['_adserver_'] = ad_content
        elif ad_content == '':
            full_url = request.build_absolute_uri()
            decode_url = urllib.parse.unquote(full_url)
            query = urllib.parse.urlsplit(decode_url).query
            dict_data = dict(urllib.parse.parse_qsl(query))
            utm_parameter = json.dumps({
                "utm_content": dict_data.get('utm_content'),
                "utm_term": dict_data.get('utm_term'),
                "utm_medium": dict_data.get('utm_medium'),
                "utm_campaign": dict_data.get('utm_campaign'),
                "utm_source": dict_data.get('utm_source')
            })
            request.session['_adserver_'] = dict_data.get('ad_content')

        if request.session.get('_adserver_', None):
            try:
                decoded_ad = AdServerShine().decode(
                    request.session.get('_adserver_'))
                if decoded_ad:
                    email = decoded_ad[1]
                    mobile = decoded_ad[2]
                    timestamp = decoded_ad[3]
                    try:
                        url = request.get_full_path().split('?')[0]
                    except:
                        url = ''
                    try:
                        timestamp_obj = datetime.strptime(
                            timestamp, "%Y-%m-%d %H:%M:%S")
                        timestamp_obj = timezone.make_aware(
                            timestamp_obj, timezone.get_current_timezone())
                    except:
                        timestamp_obj = timezone.now()
                    addAdServerLead.delay({
                        'email': email,
                        'mobile': mobile,
                        'timestamp': timestamp,
                        'url': url,
                        'utm_parameter': utm_parameter,
                    })
            except Exception as e:
                logging.getLogger('error_log').error(str(e))
        response = self.get_response(request)
        return response


class LoginMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cookies_data = request.COOKIES.get('_em_', '').split('|')
        resp_status = ShineCandidateDetail().get_status_detail(
            email=cookies_data[0], shine_id=None, token=None)
        if resp_status:
            request.session.update(resp_status)
        response = self.get_response(request)
        return response
