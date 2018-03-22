import json
import logging
from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.template.loader import render_to_string
from django.middleware.csrf import get_token
from shine.core import ShineCandidateDetail
from .mixins import UpdateShineProfileMixin

from microsite.roundoneapi import RoundOneAPI
from microsite.common import ShineUserDetail
from search.helpers import get_recommendations
from core.library.haystack.query import SQS
from .config import ROUNDONE_INTERACTION_RESULT


month_dict = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5,
    'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9,
    'Oct': 10, 'Nov': 11, 'Dec': 12
}


class RoundoneDashboardView(RoundOneAPI, TemplateView):
    template_name = 'dashboard/dashboard-roundone.html'

    def get_context_data(self, **kwargs):
        context = super(RoundoneDashboardView, self).get_context_data(**kwargs)
        pending = []
        accepted = []
        referral_status = self.get_referral_status(self.request)

        if referral_status:
            if referral_status.get("status") == "1":
                for data in referral_status.get('data'):
                    try:
                        status = data.get("status", "")
                        data.update({"status": status})
                        data.update({
                            "requestedDate": datetime.utcfromtimestamp(
                                int(data.get(
                                    'requestedDate', 0))).strftime("%d %b, %Y")
                        })

                        data.update({
                            "expiryDate": datetime.utcfromtimestamp(
                                int(data.get(
                                    'expiryDate', 0))).strftime("%d %b, %Y")})

                        if data.get("acceptedDate") and str(status) == "1":
                            data.update({
                                "acceptedDate": datetime.utcfromtimestamp(
                                    int(data.get(
                                        'acceptedDate', 0))).strftime("%d %b, %Y")})
                            accepted.append(data)
                        else:
                            pending.append(data)
                    except:
                        pass
        context['accepted'] = accepted
        context['pending'] = pending
        rcourses = get_recommendations(
            self.request.session.get('func_area', None),
            self.request.session.get('skills', None))

        if rcourses:
            rcourses = rcourses[:6]
            context['recommended_products'] = rcourses
        return context

    def get(self, request, *args, **kwargs):
        return super(RoundoneDashboardView, self).get(request, *args, **kwargs)


class DashboardUpcomingView(RoundOneAPI, View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            upcoming_interaction = self.get_upcoming_status(request)
            context = {'upcoming_interaction': upcoming_interaction}
            template_html = render_to_string("include/roundone_upcoming.html", context)
            return HttpResponse(json.dumps({'status': True, 'response': upcoming_interaction.get('response'), 'template': template_html}))
        else:
            pass
        return HttpResponse(json.dumps({'status': False, 'response': False}))


class DashboardPastView(RoundOneAPI, View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            past_interaction = self.get_past_interaction(request)

            if past_interaction:

                if past_interaction.get("status") == "1":

                    for data in past_interaction.get('data'):
                        try:
                            status = data.get("status", "")
                            data.update({"status_str": status})
                            data.update({"action": status})
                        except:
                            pass
            context = {"past_interaction": past_interaction}

            template_html = render_to_string(
                "include/roundone_past.html", context)
            return HttpResponse(json.dumps({
                'status': True, 'response': past_interaction.get('response'), 'template': template_html}))
        else:
          pass
        return HttpResponse(json.dumps({'status': False, 'response': False}))


class DashboardSavedView(RoundOneAPI, View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            csrf_token_value = get_token(request)
            saved_history = self.get_saved_history(request)
            context = {'saved_history': saved_history, 'partner': 'roundone', "csrf_token_value": csrf_token_value}
            template_html = render_to_string("include/roundone_save.html", context)
            return HttpResponse(json.dumps({'status': True, 'response': saved_history.get('response'), 'template': template_html}))
        else:
            pass
        return HttpResponse(json.dumps({'status': False, 'response': False}))


class DashboardResultView(RoundOneAPI, TemplateView):
    template_name = "include/roundone_feedback.html"

    def get_context_data(self, **kwargs):
        show_feedback = True
        context = super(DashboardResultView, self).get_context_data(**kwargs)
        past_interaction = str(self.request.GET.get('status', ''))

        if past_interaction == '1' or past_interaction == '0':
            show_feedback = False
            context.update({'show_feedback': show_feedback})
        else:

            context.update({'show_feedback': show_feedback})

        try:
            data_dict = {
                'userEmail': self.request.session.get('email', ''),
                'orderId': kwargs.get("order_id"),
            }
            result_html = self.get_result_template(
                self.request, data_dict, show_feedback)
            context.update({'result_html': result_html})
        except Exception as e:
            logging.getLogger('error_log').error('unable to load result template %s' %str(e))
            pass
        context.update(kwargs)
        return context

    def post(self, request, *args, **kwargs):
        interviewerRating = request.POST.get('interviewerRating')
        roundoneRating = request.POST.get('roundoneRating')
        comments = request.POST.get('comments')
        orderId = kwargs.get('order_id')

        userEmail = request.session.get('email', '')

        data_dict = {
            'userEmail': userEmail,
            'interviewerRating': interviewerRating,
            'roundoneRating': roundoneRating,
            'comments': comments,
            'orderId': orderId
        }

        response_json = self.feedback_submit(request, data_dict)

        if response_json.get("status") == "1":
            template_html = self.get_result_template(request, data_dict, False)
            return HttpResponse(json.dumps({
                'status': True, 'template': template_html}))

        return HttpResponse(json.dumps({
            'status': False, 'message': response_json.get('msg')}))

    def get_result_template(self, request, data_dict, show_feedback):
        result_json = self.interaction_result(request, data_dict)
        status = result_json.get('status')
        if result_json.get("status") == "1":
            try:
                data = result_json.get("data", {})

                feedback = data.get("referrerFeedback", {})

                commSkills = feedback.get("commSkills")
                subjectKnowledge = feedback.get("subjectKnowledge")
                culturalFit = feedback.get("culturalFit")
                status = data.get("status", '')

                commSkills_str = ROUNDONE_INTERACTION_RESULT.get(
                    str(commSkills))
                subjectKnowledge_str = ROUNDONE_INTERACTION_RESULT.get(
                    str(subjectKnowledge))
                culturalFit_str = ROUNDONE_INTERACTION_RESULT.get(
                    str(culturalFit))
                feedback.update({
                    "commSkills": commSkills_str,
                    "subjectKnowledge": subjectKnowledge_str,
                    "culturalFit": culturalFit_str
                })
            except Exception as e:
                logging.getLogger('error_log').error('unable to fetch details from result template function %s' %
                                                     str(e))
                pass

        context = {
            'result': result_json,
            'show_feedback': show_feedback,
            "status": status}

        template_html = render_to_string(
            "include/roundone_result.html", context)
        return template_html


class DashboardSavedDeleteView(RoundOneAPI, View):

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            job_params = request.POST.get('job_params').split('-')
            response_json = self.delete_saved_job(request, job_params)
            if response_json.get("status") and response_json.get("status") == "1":
                return HttpResponse(json.dumps({'status': True}))
            return HttpResponse(json.dumps({'status': False, "message": "Error Deleting This Job"}))
        else:
            pass
        return HttpResponse(json.dumps({'status': False}))


class DashboardMyProfileView(ShineCandidateDetail, ShineUserDetail, TemplateView):
    template_name = "include/roundone_profile.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardMyProfileView, self).get_context_data(**kwargs)
        try:
            request = self.request
            shine_profile = request.session.get('candidate_profile', '')
            if not shine_profile:
                email = request.session.get('email', '')
                if email:
                    shine_profile = self.get_candidate_detail(email=email)
                    f_area = self.get_functional_area(email=email)
                    request.session.update({
                        'candidate_profile': shine_profile, 'f_area': f_area,
                    })
                else:
                    shine_profile = {}
            personal_detail = self.get_shine_user_profile_detail(request)
            education_detail = shine_profile.get('education', '')
            experience_detail = shine_profile.get('jobs', '')
            total_exp = shine_profile.get('total_experience', '')
            resumes = self.get_resume_file(request)
            skill_detail = self.get_skills(request)
            context.update({
                "personal_detail": personal_detail,
                "education_detail": education_detail,
                "experience_detail": experience_detail,
                "skill_detail": skill_detail,
                'skill_len': len(skill_detail),
                'total_exp': total_exp,
                'years': [i for i in range(12)],
                'st_years': [i for i in range(1960, 2017)],
                'csrf_token_value': get_token(request),
                'month_dict': month_dict,
                # 'f_area': f_area,
                "resumes": resumes,
                "passout_yr": [yr for yr in range(1960, 2017)]
            })
        except Exception as e:
            logging.getLogger('error_log').error('unable to load profile in dashboard %s'%str(e))
        context.update({"myprofile_active": True})
        return context

    def get(self, request, *args, **kwargs):
        if not request.session.get('candidate_id'):
            return HttpResponseRedirect('/login/?next=/dashboard/roundone/profile/')
        return super(DashboardMyProfileView, self).get(request, *args, **kwargs)


class UpdateShineProfileView(UpdateShineProfileMixin, View):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            if request.is_ajax() and request.session.get('candidate_id'):
                shine_id = request.session.get("candidate_id", '')
                email = request.session.get('email', '')
                user_access_token = request.session.get("user_access_token", '')
                skill = request.POST.getlist('skill')
                old_skill = request.POST.get('skilllength')
                if not user_access_token:
                    user_access_token = self.get_access_token(email, '123456')

                client_token = self.get_client_token()
                edit_for = request.POST.get('edit_type')
                if shine_id and user_access_token and client_token and edit_for:
                    if edit_for == "editpersonal":
                        if len(skill) > len(old_skill):
                            update_status, update_msg =\
                                self.update_candidate_skills(
                                    shine_id=shine_id,
                                    user_access_token=user_access_token,
                                    client_token=client_token, data=request.POST,
                                    type_of='edit', token=None)
                        else:
                            update_status, update_msg =\
                                self.update_candidate_personal(
                                    shine_id=shine_id,
                                    user_access_token=user_access_token,
                                    client_token=client_token, data=request.POST,
                                    type_of='edit', token=None)

                    elif edit_for == "editeducation":
                        update_status, update_msg =\
                            self.update_candidate_education(
                                shine_id=shine_id,
                                user_access_token=user_access_token,
                                client_token=client_token, data=request.POST,
                                type_of='edit', token=None)

                    elif edit_for == "editworkexp":
                        update_status, update_msg = self.update_candidate_jobs(
                            shine_id=shine_id,
                            user_access_token=user_access_token,
                            client_token=client_token, data=request.POST,
                            type_of='edit', token=None)

                    elif edit_for == "uploadresume":
                        update_status, update_msg = self.upload_resume(
                            shine_id=shine_id,
                            user_access_token=user_access_token,
                            client_token=client_token, data=request.FILES,
                            type_of='edit', token=None)

                    if update_status:
                        return HttpResponse(json.dumps({'status': True, "msg": update_msg}))
                    else:
                        return HttpResponse(json.dumps({'status': False, "msg": update_msg}))
        except Exception as e:
            logging.getLogger("error_log").error(' unable to update ShineUserProfile %s'%str(e))

        return HttpResponse(json.dumps({'status': False, "msg": "Something went wrong, Please Try Again."}))
