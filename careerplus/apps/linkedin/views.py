from django.views.generic import View, TemplateView
from django.http import (HttpResponse,
    HttpResponseRedirect)
from django.core.urlresolvers import reverse

from shine.core import ShineToken, ShineCandidateDetail
from linkedin.autologin import AutoLogin
from .utills import ques_dict
from order.models import Order
from linkedin.models import QuizResponse

class AutoLoginView(View):

    def get_context_data(self, **kwargs):
        context = {}
        return context

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token', '')
        context = self.get_context_data(**kwargs)
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
        flag = False
        try:
            quiz_resp = QuizResponse.objects.get(oi=kwargs.get('order_item', ''))
        except:
            quiz_resp = None

        context={
            'ques_dict': ques_dict,
            'quiz_resp': quiz_resp if quiz_resp else None,
            'flag': quiz_resp.submitted if quiz_resp else False,
        } 
        return context

    def post(self, request, *args, **kwargs):

        try:
            quiz_resp = QuizResponse.objects.get(oi=kwargs.get('order_item', ''))
        except:
            quiz_resp = None

        if quiz_resp:
            quiz_resp.question1 = ques_dict.get('q1', '')
            quiz_resp.question2 = ques_dict.get('q2', '')
            quiz_resp.question3 = ques_dict.get('q3', '')
            quiz_resp.question4 = ques_dict.get('q4', '')
            quiz_resp.question5 = ques_dict.get('q5', '')
            quiz_resp.anser1 = request.POST.get('q1', '')
            quiz_resp.anser2 = request.POST.get('q2', '')
            quiz_resp.anser3 = request.POST.get('q3', '')
            quiz_resp.anser4 = request.POST.get('q4', '')
            quiz_resp.anser5 = request.POST.get('q5', '')
            quiz_resp.submitted = True
            quiz_resp.save()
            return HttpResponseRedirect(reverse('dashboard'))


class DraftView(TemplateView):
    template_name = "linkedin/counselling_form.html"
    
    def get(self,request,*args,**kwargs):
        return super(DraftView, self).get(request, *args, **kwargs)
        

    def get_context_data(self, **kwargs):
        context = super(DraftView, self).get_context_data(**kwargs)
        context['ques_dict'] = ques_dict
        return context
