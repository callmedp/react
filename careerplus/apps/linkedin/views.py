from django.views.generic import View, TemplateView
from django.http import (HttpResponse,
    HttpResponseRedirect)
from django.core.urlresolvers import reverse
from datetime import datetime

from shine.core import ShineToken, ShineCandidateDetail
from linkedin.autologin import AutoLogin
from .utills import ques_dict
from order.models import Order, OrderItem, OrderItemOperation
from quizs.models import QuizResponse

class AutoLoginView(View):

    def get_context_data(self, **kwargs):
        context = {}
        return context

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token', '')
        context = self.get_context_data(**kwargs)
        if token:
            next = request.GET.get('next') or '/'
            email, candidateid, orderid = AutoLogin().decode(token)
            if candidateid:
                try:
                    resp_status = ShineCandidateDetail().get_status_detail(
                        email=None, shine_id=candidateid)
                    
                    if resp_status:
                        return HttpResponseRedirect(next, {'orderid':orderid})
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
            orderitem = OrderItem.objects.get(pk=kwargs.get('order_item', ''))
        except:
            orderitem = None

        quiz_resp = orderitem.quizresponse
        context={
            'ques_dict': ques_dict,
            'quiz_resp': quiz_resp if quiz_resp else None,
            'flag': quiz_resp.submitted if quiz_resp else False,
            "orderitem":orderitem,
        } 
        return context

    def post(self, request, *args, **kwargs):
        try:
            orderitem = OrderItem.objects.get(pk=kwargs.get('order_item', ''))
        except:
            orderitem = None

        if orderitem:
            quiz_obj = orderitem.quizresponse
            quiz_obj.question1 = ques_dict.get('q1', '')
            quiz_obj.question2 = ques_dict.get('q2', '')
            quiz_obj.question3 = ques_dict.get('q3', '')
            quiz_obj.question4 = ques_dict.get('q4', '')
            quiz_obj.question5 = ques_dict.get('q5', '')
            quiz_obj.anser1 = request.POST.get('q1', '')
            quiz_obj.anser2 = request.POST.get('q2', '')
            quiz_obj.anser3 = request.POST.get('q3', '')
            quiz_obj.anser4 = request.POST.get('q4', '')
            quiz_obj.anser5 = request.POST.get('q5', '')
            quiz_obj.submitted = True
            quiz_obj.save()
            if not orderitem.tat_date:
                orderitem.tat_date = datetime.now()
                orderitem.counselling_form_status = 42
                orderitem.save()
            return HttpResponseRedirect(reverse('console:linkedin-inbox'))


class DraftView(TemplateView):
    template_name = "linkedin/counselling_form.html"
    
    def get(self,request,*args,**kwargs):
        return super(DraftView, self).get(request, *args, **kwargs)
        

    def get_context_data(self, **kwargs):
        context = super(DraftView, self).get_context_data(**kwargs)
        context['ques_dict'] = ques_dict
        return context


class LinkedinDraftView(TemplateView):
    template_name = "linkedin/linkedin_draft.html"
    
    def get(self,request,*args,**kwargs):
        return super(LinkedinDraftView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LinkedinDraftView, self).get_context_data(**kwargs)
        orderitem_id = kwargs.get('order_item', '')
        op_id = kwargs.get('op_id', '')
        try:
            oi = OrderItem.objects.get(pk=orderitem_id)
            op_id = oi.orderitemoperation_set.get(pk = op_id)
            try:
                draft = ''
                if op_id:    
                    draft = op_id.linkedin
                    flag2 = False
                    skill_list = draft.key_skills
                    organization_list = draft.from_organization.filter(org_current=False).order_by('-work_to')
                    education_list = draft.from_education.filter(edu_current=False).order_by('-study_to')
                    current_org = draft.from_organization.filter(org_current=True)
                    current_edu = draft.from_education.filter(edu_current=True)
                    if current_edu:
                        current_edu = current_edu[0]
                    if current_org:
                        current_org = current_org[0]
                    if draft.profile_photo:
                        flag2 = True
                    if draft.public_url:
                        flag2 = True
                    if draft.recommendation:
                        flag2 - True
                    if draft.follow_company:
                        flag2 = True
                    if draft.join_group:
                        flag2 = True
                    context.update({
                        'flag2': flag2,
                        'orderitem': oi,
                        'draft': draft,
                        'skill_list': skill_list.split(','),
                        'organization_list': organization_list,
                        'education_list': education_list,
                        'current_edu': current_edu,
                        'current_org': current_org
                    })
                else:
                    context.update({'draft':''})
            except:
                context.update({'draft':''})        
            
        except:
            context.update({'draft':''})
        return context
