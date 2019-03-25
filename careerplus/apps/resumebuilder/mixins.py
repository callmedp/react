#
from django.http import HttpResponse

# inter app imports

# python imports
import json


class SessionManagerMixin(object):

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated and not request.session.get('email'):
            user_email = request.user.email
            if not user_email:
                return HttpResponse('Unauthorized', status=401)
            request.session['email'] = user_email

        elif request.method == 'POST' and not request.session.get('email'):
            body_data = json.loads(request.body)
            user_email = body_data['email']
            if not user_email:
                return HttpResponse('Unauthorized', status=401)
            request.session['email'] = user_email

        elif not request.session.get('email'):
            return HttpResponse('Unauthorized', status=401)

        return super(SessionManagerMixin, self).dispatch(
            request, *args, **kwargs)
