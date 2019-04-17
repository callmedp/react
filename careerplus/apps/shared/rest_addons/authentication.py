# python imports
import pickle

# django imports
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.signals import user_login_failed
from django.contrib.auth import _get_backends, _clean_credentials

# local imports

# inter app imports
from shared.utils import ShineCandidate

# third party imports
from rest_framework import exceptions
from django_redis import get_redis_connection
from rest_framework.authentication import SessionAuthentication, get_authorization_header

# Global constants
conn = get_redis_connection('token')


class ShineUserAuthentication(SessionAuthentication):
    """
    User authentication for APIs.
    Sets user in request else raises AuthenticationFailure
    """

    def authenticate(self, request):
        candidate_id = getattr(request._request.session, 'candidate_id', '')
        candidate_profile = getattr(request._request.session, 'candidate_profile', {})

        # For session authentication.
        # Makes browsable APIs usable.
        if candidate_id and candidate_profile:
            shine_candidate_obj = ShineCandidate(**candidate_profile)
            return (shine_candidate_obj, None)

        auth = get_authorization_header(request).split()
        if not auth:
            return None

        return self.authenticate_credentials(auth[0])

    def authenticate_credentials(self, key):
        candidate_profile = conn.get(key)
        if not candidate_profile:
            return
        shine_candidate_obj = pickle.loads(candidate_profile)
        return (shine_candidate_obj, None)

    def authenticate_header(self, request):
        return 'Token'
