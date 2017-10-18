# python built-in imports
import re
from datetime import datetime
from django.utils import timezone
from crmapi.tasks import addAdServerLead

# django imports
from django_mobile.middleware import MobileDetectionMiddleware, SetFlavourMiddleware
from django.utils.deprecation import MiddlewareMixin

from .utils import set_session_country


class UpgradedSetFlavourMiddleware(MiddlewareMixin, SetFlavourMiddleware):
    """
    Makes middleware django 1.10 compatible
    """
    def __init__(self, get_response=None):
        super(UpgradedSetFlavourMiddleware, self).__init__(get_response)


class UpgradedMobileDetectionMiddleware(MiddlewareMixin, MobileDetectionMiddleware):
    """
    Makes middleware django 1.10 compatible
    """
    # TODO: Upgrade regex for tablet to be exempted
    def __init__(self, get_response=None):
        super(UpgradedMobileDetectionMiddleware, self).__init__(get_response)
        user_agents_test_match = r'^(?:%s)' % '|'.join(self.user_agents_test_match)
        self.user_agents_test_match_regex = re.compile(user_agents_test_match, re.IGNORECASE)
        self.user_agents_test_search_regex = re.compile(self.user_agents_test_search, re.IGNORECASE)
        self.user_agents_exception_search_regex = re.compile(self.user_agents_exception_search, re.IGNORECASE)


class LearningShineMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from users.mixins import UserMixin
        country_obj = UserMixin().get_client_country(request)
        set_session_country(country_obj, request)
        response = self.get_response(request)
        return response

    def process_request(self, request):
        from core.api_mixin import AdServerShine, AcrossShine
        cpem = request.COOKIES.get('_cpem_', '')

        try:
            cpem_mail = AcrossShine().decode(cpem)
        except:
            cpem_mail = None
        ad_content = request.GET.get('ad_content', '')
        if ad_content:
            ad_content = ad_content
            request.session['_adserver_'] = ad_content
        if request.session.get('_adserver_', None):
            try:
                decoded_ad = AdServerShine().decode(request.session.get('_adserver_', None))
                if decoded_ad:
                    email = decoded_ad[1]
                    mobile = decoded_ad[2]
                    timestamp = decoded_ad[3]
                    try:
                        url = request.get_full_path().split('?')[0]
                    except:
                        url = ''
                    try:
                        timestamp_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                        timestamp_obj = timezone.make_aware(timestamp_obj, timezone.get_current_timezone())
                    except:
                        timestamp_obj = timezone.now()
                    timediff = timezone.now() - timestamp_obj
                    minute_diff = timediff.seconds / 60
                    addAdServerLead.delay({
                        'email': email,
                        'mobile': mobile,
                        'timestamp': timestamp,
                        'url': url
                    })
                    if minute_diff < 30:
                        if email:
                            cpem_mail = email

            except:
                pass