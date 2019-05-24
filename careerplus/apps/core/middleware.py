# python built-in imports
import logging
import re
import json
import socket
import ipaddress
import urllib.parse
from datetime import datetime, timedelta

# django imports
from django_mobile.middleware import SetFlavourMiddleware
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.conf import settings
from django_mobile import set_flavour
from django.utils import timezone

# local imports
from shop.models import Skill, FunctionalArea
from .utils import set_session_country
from users.mixins import UserMixin
from core.api_mixin import AdServerShine, ShineCandidateDetail
from crmapi.tasks import add_server_lead_task


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
        is_mobile = True
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
        if request.path.startswith('/console/'):
            response = self.get_response(request)
            return response

        em_data = request.COOKIES.get('_em_', '')
        if em_data and '|' in em_data:
            cookies_data = em_data.split('|')
            resp_status = ShineCandidateDetail().get_status_detail(
                email=cookies_data[0], shine_id=None, token=None)
            if resp_status:
                request.session.update(resp_status)

        session_fa = False
        session_skills = False

        if 'func_area' in request.session.keys():
            session_fa = True
        if 'skills' in request.session.keys():
            session_skills = True
        candidate_id = request.session.get('candidate_id')
        candidate_detail = None

        if not session_fa and candidate_id:
            candidate_detail = ShineCandidateDetail().get_candidate_public_detail(
                shine_id=candidate_id)
            if candidate_detail:
                func_area = candidate_detail.get('jobs')[0].get("parent_sub_field", "") \
                    if len(candidate_detail.get('jobs', [])) else ''
                func_area_obj = FunctionalArea.objects.filter(name__iexact=func_area)
                fa_id = None
                if func_area_obj:
                    fa_id = func_area_obj[0].id
                request.session.update({
                    'func_area': fa_id
                })
        if not session_skills:
            if not candidate_detail and candidate_id:
                candidate_detail = ShineCandidateDetail().get_candidate_public_detail(
                    shine_id=candidate_id)
            if candidate_detail:
                skills = [skill['value'] for skill in candidate_detail['skills']]
                skills_in_ascii = []
                for skill in skills:
                    try:
                        skills_in_ascii.append(skill.encode('ascii','replace').decode('ascii','replace'))
                    except Exception as e:
                        logging.getLogger('error_log').error('error in decrypting skills into ascii {}'.format(str(e)))
                        skills_in_ascii.append("")
                skills_obj = Skill.objects.filter(name__in=skills_in_ascii)[:15]
                skills_ids = [str(s.id) for s in skills_obj]
                request.session.update({
                    'mid_skills': skills_ids,
                    'mid_skills_name': skills[:15],
                })
        response = self.get_response(request)
        return response


class TrackingMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/console/'):
            response = self.get_response(request)
            return response
            
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
                    logging.getLogger('error_log').error(str(e))
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

            utm['sub_campaign_slug'] = request.GET.get('sub_campaign_slug','')[:50] or utm.get('sub_campaign_slug')
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
        if request.path.startswith('/console/'):
            response = self.get_response(request)
            return response

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
                    except Exception as e:
                        logging.getLogger('error_log').error(str(e))
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

class RemoveSessionCookieMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if 'remove_cookie' in  response.__dict__:
            if response.remove_cookie:
                response.delete_cookie('sessionid',  path='/')
        return response






def is_valid_ip(ip_address):
    """
    Check Validity of an IP address
    """
    valid = True
    try:
        socket.inet_aton(ip_address.strip())
    except:
        valid = False
    return valid


def get_ip_address_from_request(request):
    """
    Makes the best attempt to get the client's real IP or return the loopback
    """
    ip_address = ''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if x_forwarded_for and ',' not in x_forwarded_for:
        if is_valid_ip(x_forwarded_for):
            ip_address = x_forwarded_for.strip()
    else:
        ips = [ip.strip() for ip in x_forwarded_for.split(',')]
        ip_address = next((ip for ip in ips if is_valid_ip(ip)), '')

    if not ip_address:
        x_real_ip = request.META.get('HTTP_X_REAL_IP', '')
        if x_real_ip and is_valid_ip(x_real_ip):
            ip_address = x_real_ip.strip()

    if not ip_address:
        remote_addr = request.META.get('REMOTE_ADDR', '')
        if remote_addr and is_valid_ip(remote_addr):
            ip_address = remote_addr.strip()

    if not ip_address: return '127.0.0.1'
    return ip_address


class LocalIPDetectionMiddleware(object):
    """
   This Middleware detects the internal ip address
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_ip = get_ip_address_from_request(request)
        logging.getLogger('info_log').info('request ip:{}'.format(request_ip))
        ip_flag = False
        for ip_range in settings.LOCAL_NETWORK_IPS_RANGE:
            if ipaddress.ip_address(request_ip) in ipaddress.ip_network(ip_range):
                ip_flag = True
                break
        if request_ip in settings.LOCAL_NETWORK_IPS: ip_flag = True
        request.ip_restricted = ip_flag
        return self.get_response(request)


