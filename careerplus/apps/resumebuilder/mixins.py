#
from django.http import HttpResponse
from django.template.loader import get_template
from .tasks import generate_image_for_resume

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

class PreviewImageCreationMixin(object):

    initiate_image_upload_task = True

    @classmethod
    def preview_image_task_call(self, sender,instance, **kwargs):
        parent_object_key = getattr(self,"parent_object_key","candidate_id")
        candidate_id = getattr(instance,parent_object_key)
        if kwargs.get('created') or self.initiate_image_upload_task:
            for template_index in range(1,6):
                generate_image_for_resume.delay(candidate_id,template_index)

        

