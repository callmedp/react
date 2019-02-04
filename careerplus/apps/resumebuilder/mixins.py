from django.contrib.sessions.backends.db import SessionStore
from resumebuilder.models import User

class SessionManagerMixin(object):

    def dispatch(self, request, *args, **kwargs):
        #
        # import ipdb;
        # ipdb.set_trace();
        return super(SessionManagerMixin, self).dispatch(
            request, *args, **kwargs)
