from django.views.generic import View, TemplateView
from django.http import (HttpResponse,
    HttpResponseRedirect)

from shine.core import ShineToken, ShineCandidateDetail
from linkedin.autologin import AutoLogin


class AutoLoginView(View):

    def get_context_data(self, **kwargs):
        context = super(AutoLoginView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({
            'messages': alert,
        })
        return context

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token', '')
        
        if token:
            next = request.GET.get('next') or '/'
            email, candidateid = AutoLogin().decode(token)
            if candidateid:
                try:
                    resp_status = ShineCandidateDetail().get_status_detail(
                        email=None, shine_id=candidateid)
                    if resp_status:
                        return HttpResponseRedirect(next)
                    else:
                        return HttpResponseRedirect('/?login_attempt=fail')
                except Exception as e:
                    logging.getLogger('error_log').error(
                        "Exception while auto logging in a user with email: %s. " "Exception: %s " % (email, str(e)))


class CounsellingSubmit(TemplateView):
    template_name = "linkedin/counselling_form.html"
    
    def get(self,request,*args,**kwargs):
        return super(CounsellingSubmit, self).get(request, *args, **kwargs)
        

    def get_context_data(self, **kwargs):
        context = super(CounsellingSubmit, self).get_context_data(**kwargs)    
        return context
