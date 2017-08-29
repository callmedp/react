# python built-in imports
import re

# django imports
from django_mobile.middleware import MobileDetectionMiddleware, SetFlavourMiddleware
from django.utils.deprecation import MiddlewareMixin

from .functions import set_session_country_currency


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
        set_session_country_currency(country_obj, request)
        response = self.get_response(request)
        return response