# python built-in imports
import logging
import re
import json
import urllib.parse
from datetime import datetime, timedelta
from django.utils import timezone
from crmapi.tasks import add_server_lead_task
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


class LoginMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        em_data = request.COOKIES.get('_em_', '')
        if em_data and '|' in em_data:
            cookies_data = em_data.split('|')
            resp_status = ShineCandidateDetail().get_status_detail(
                email=cookies_data[0], shine_id=None, token=None)
            if resp_status:
                request.session.update(resp_status)
        response = self.get_response(request)
        return response


class TrackingMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        dict_data = {}
        full_url = request.build_absolute_uri()
        decode_url = urllib.parse.unquote(full_url)
        query = urllib.parse.urlsplit(decode_url).query
        dict_data = dict(urllib.parse.parse_qsl(query))
        max_age = 24 * 60 * 60
        expires = datetime.strftime(
            datetime.now() + timedelta(seconds=max_age), "%Y-%m-%d %H:%M:%S")

        if not request.is_ajax():
            utm = request.session.get('utm', {})
            expiry = utm.get('expires', None)
            if expiry:
                try:
                    expiry = timezone.make_aware(
                        datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S"),
                        timezone.get_current_timezone())
                    if timezone.now() > expiry:
                        utm = {}
                except Exception as e:
                    pass
            ref_url = request.get_full_path()
            if '?' in ref_url:
                ref_url = ref_url.split('?')[0]
                if ref_url:
                    utm['ref_url'] = ref_url[:1048]

            if 'utm_source' in request.GET or 'utm_source' in dict_data:
                source = request.GET.get('utm_source') or dict_data.get('utm_source')
                if source:
                    utm['utm_source'] = source[:100]
                    utm['expires'] = expires

            if 'utm_term' in request.GET or 'utm_term' in dict_data:
                term = request.GET.get('utm_term') or dict_data.get('utm_term')
                if term:
                    utm['utm_term'] = term[:50]
                    utm['expires'] = expires

            if 'utm_content' in request.GET or 'utm_content' in dict_data:
                content = request.GET.get('utm_content') or dict_data.get('utm_content')
                if content:
                    utm['utm_content'] = content[:50]
                    utm['expires'] = expires

            if 'utm_medium' in request.GET or 'utm_medium' in dict_data:
                medium = request.GET.get('utm_medium') or dict_data.get('utm_medium')
                if medium:
                    utm['utm_medium'] = medium[:50]
                    utm['expires'] = expires

            if 'utm_campaign' in request.GET or 'utm_campaign' in dict_data:
                campaign = request.GET.get('utm_campaign') or dict_data.get('utm_campaign')
                if campaign:
                    utm['utm_campaign'] = campaign[:100]
                    utm['expires'] = expires

            if 'keyword' in request.GET:
                keyword = request.GET.get('keyword')
                if keyword:
                    utm['keyword'] = keyword[:100]

            if 'placement' in request.GET:
                placement = request.GET.get('placement')
                if placement:
                    utm['placement'] = placement[:100]

            request.session['utm'] = utm

        response = self.get_response(request)

        # if not request.is_ajax():
        #     if utm.get('utm_source'):
        #         response.set_cookie(
        #             '_us', utm.get('utm_source'), max_age=max_age, expires=expires )
        #     if utm.get('utm_content'):
        #         response.set_cookie(
        #             '_uo', utm.get('utm_content'), max_age=max_age, expires=expires)
        #     if utm.get('utm_medium'):
        #         response.set_cookie(
        #             '_um', utm.get('utm_medium'), max_age=max_age, expires=expires)
        #     if utm.get('utm_term'):
        #         response.set_cookie(
        #             '_ut', utm.get('utm_term'), max_age=max_age, expires=expires)
        #     if utm.get('utm_campaign'):
        #         response.set_cookie(
        #             '_uc', utm.get('utm_campaign'), max_age=max_age, expires=expires)
        # print(utm)
        return response


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
            request.session['_adserver_'] = dict_data.get('ad_content')

        if request.session.get('_adserver_', None):
            try:
                decoded_ad = AdServerShine().decode(
                    request.session.get('_adserver_'))
                if len(decoded_ad) == 4:
                    email = decoded_ad[1]
                    mobile = decoded_ad[2]
                    timestamp = decoded_ad[3]
                    utm_dict = request.session.get('utm')
                    utm_parameter = json.dumps({
                        "utm_content": utm_dict.get('utm_content'),
                        "utm_term": utm_dict.get('utm_term'),
                        "utm_medium": utm_dict.get('utm_medium'),
                        "utm_campaign": utm_dict.get('utm_campaign'),
                        "utm_source": utm_dict.get('utm_source')
                    })
                    campaign_slug = utm_dict.get('utm_campaign')
                    try:
                        # url = utm_dict.get('ref_url').split('/')
                        url = request.path.split('/')
                        last_ele = url[-1]
                        product_id = re.findall('\d+', last_ele)[0]
                        product = url[-2]
                    except:
                        url = ''
                        product_id = 0
                        product = ''

                    add_server_lead_task.delay({
                        'email': email,
                        'mobile': mobile,
                        'timestamp': timestamp,
                        'url': request.path,
                        'product_id': product_id,
                        'product': product,
                        'utm_parameter': utm_parameter,
                        'campaign_slug': campaign_slug,
                    })
                else:
                    logging.getLogger('info_log').info(
                        "decoded list length less than four")
            except Exception as e:
                logging.getLogger('error_log').error(str(e))
        response = self.get_response(request)
        return response


class AmpMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        flag = False
        if 'type' in request.GET:
            amp_content = request.GET.get('type', '')
            if amp_content == 'amp':
                flag = True
        request.amp = flag
        response = self.get_response(request)
        return response