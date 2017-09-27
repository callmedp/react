import logging

from django.template.loader import get_template

from weasyprint import HTML, CSS
from django.template import Context

from django.views.generic import View, TemplateView
from django.http import (HttpResponse,
    HttpResponseRedirect, HttpResponseForbidden)
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
            next1 = request.GET.get('next') or '/'
            email, candidateid, valid = AutoLogin().decode(token)
            if valid:
                if candidateid and next1 == 'dashboard':
                    try:
                        resp_status = ShineCandidateDetail().get_status_detail(
                            email=None, shine_id=candidateid)
                        request.session.update(resp_status)
                        if resp_status:
                            return HttpResponseRedirect('/dashboard/')
                        else:
                            return HttpResponseRedirect('/?login_attempt=fail')
                    except Exception as e:
                        logging.getLogger('error_log').error(
                            "Exception while auto logging in a user with email: %s. " "Exception: %s " % (email, str(e)))
                return HttpResponseRedirect('/?login_attempt=fail')
        return HttpResponseRedirect('/?login_attempt=fail')


class CounsellingSubmit(TemplateView):
    template_name = "linkedin/counselling_form.html"

    def get(self, request, *args, **kwargs):
        return super(CounsellingSubmit, self).get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(CounsellingSubmit, self).get_context_data(**kwargs)
        try:
            orderitem = OrderItem.objects.get(pk=kwargs.get('order_item', ''))
        except:
            orderitem = None

        quiz_resp = orderitem.quizresponse
        context = {
            'ques_dict': ques_dict,
            'quiz_resp': quiz_resp if quiz_resp else None,
            'flag': quiz_resp.submitted if quiz_resp else False,
            "orderitem": orderitem,
        }
        return context

    def post(self, request, *args, **kwargs):
        try:
            orderitem = OrderItem.objects.get(pk=kwargs.get('order_item', ''))
        except:
            orderitem = None
        if request.POST.get('save') == 'save':
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
                quiz_obj.save()
                return HttpResponseRedirect(reverse('console:linkedin-inbox'))
        elif request.POST.get('submit') == 'submit':
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
                    last_oi_status = orderitem.oi_status
                    orderitem.tat_date = datetime.now()
                    orderitem.oi_status = 42
                    orderitem.save()
                    orderitem.orderitemoperation_set.create(
                        oi_status=orderitem.oi_status,
                        last_oi_status=last_oi_status,
                        assigned_to=orderitem.assigned_to)
                return HttpResponseRedirect(reverse('console:linkedin-inbox'))


class CounsellingForm(TemplateView):
    template_name = "linkedin/dashboard_counselling_form.html"
    
    def get(self, request, *args, **kwargs):
        return super(CounsellingForm, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CounsellingForm, self).get_context_data(**kwargs)
        try:
            orderitem = OrderItem.objects.get(pk=kwargs.get('order_item', ''))
        except:
            orderitem = None

        quiz_resp = orderitem.quizresponse
        context = {
            'ques_dict': ques_dict,
            'quiz_resp': quiz_resp if quiz_resp else None,
            'flag': quiz_resp.submitted if quiz_resp else False,
            "orderitem": orderitem,
        }
        return context

    def post(self, request, *args, **kwargs):
        try:
            orderitem = OrderItem.objects.get(pk=kwargs.get('order_item', ''))
        except:
            orderitem = None
        if request.POST.get('save') == 'save':
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
                quiz_obj.save()
                return HttpResponseRedirect(reverse('console:linkedin-inbox'))
        elif request.POST.get('submit') == 'submit':
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
                    last_oi_status = orderitem.oi_status
                    orderitem.tat_date = datetime.now()
                    orderitem.oi_status = 42
                    orderitem.save()
                    orderitem.orderitemoperation_set.create(
                        oi_status=orderitem.oi_status,
                        last_oi_status=last_oi_status,
                        assigned_to=orderitem.assigned_to)
                return HttpResponseRedirect(reverse('console:linkedin-inbox'))


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
            op_id = oi.orderitemoperation_set.filter(linkedin = op_id)[0]
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
                        'op_id':op_id,
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


class DraftAdminView(TemplateView):
    template_name = "linkedin/linkedin-resume-pdf.html"
    
    def get(self,request,*args,**kwargs):
        orderitem_id = kwargs.get('order_item', '')
        op_id = kwargs.get('op_id', '')
        try:
            oi = OrderItem.objects.get(pk=orderitem_id)
            op_id = oi.orderitemoperation_set.get(pk = op_id)
            if self.request.user.is_anonymous():
                return HttpResponseForbidden()
            if not self.request.user:
                return HttpResponseForbidden()

            return super(DraftAdminView, self).get(request, *args, **kwargs)
        except:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(DraftAdminView, self).get_context_data(**kwargs)
        orderitem_id = kwargs.get('order_item', '')
        op_id = kwargs.get('op_id', '')
        try:
            oi = OrderItem.objects.get(pk=orderitem_id)
            op_id = oi.orderitemoperation_set.get(pk = op_id)
            
            try:
                draft = ''
                if op_id:    
                    draft = op_id.linkedin
                    name = draft.candidate_name
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
                        'name': name,
                        'skill_list': skill_list,
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


class DraftDownloadView(View):

    def get(self, request, *args, **kwargs):
        orderitem_id = kwargs.get('order_item', '')
        op_id = kwargs.get('op_id', '')

        try:
            order_item = OrderItem.objects.get(pk=orderitem_id)
            oio = order_item.orderitemoperation_set.get(linkedin = op_id)
            try:
                draft = ''
                if oio:
                    flag2 = False
                    draft = oio.linkedin
                    name = draft.candidate_name
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

                    context_dict = {
                        'pagesize': 'A4',
                        'orderitem': order_item,
                        'draft': draft,
                        'name': name,
                        'skill_list': skill_list.split(','),
                        'organization_list': organization_list,
                        'education_list': education_list,
                        'flag2': flag2,
                        'current_edu': current_edu,
                        'current_org': current_org,
                    }
                    template = get_template('linkedin/linkedin-resume-pdf.html')
                    context = Context(context_dict)
                    html  = template.render(context)
                    pdf_file = HTML(string=html).write_pdf()
                    http_response = HttpResponse(pdf_file, content_type='application/pdf')
                    http_response['Content-Disposition'] = 'filename="report.pdf"'
                    return http_response
                else:
                    return HttpResponseForbidden()
            except:
                return HttpResponseForbidden()
        except:
            return HttpResponseForbidden()