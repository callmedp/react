#
from django.http import HttpResponse

# inter app imports

# python imports
import json


class SessionManagerMixin(object):

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated and not request.session.get('email'):
            candidate_email = request.user.email
            if not candidate_email:
                return HttpResponse('Unauthorized', status=401)
            request.session['email'] = candidate_email

        elif request.method == 'POST' and not request.session.get('email'):
            body_data = json.loads(request.body)
            candidate_email = body_data['email']
            if not candidate_email:
                return HttpResponse('Unauthorized', status=401)
            request.session['email'] = candidate_email

        elif not request.session.get('email'):
            return HttpResponse('Unauthorized', status=401)

        return super(SessionManagerMixin, self).dispatch(
            request, *args, **kwargs)

