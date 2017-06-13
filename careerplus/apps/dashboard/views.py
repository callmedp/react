import json

from django.views.generic import TemplateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.template.loader import render_to_string
from django.middleware.csrf import get_token

from microsite.roundoneapi import RoundOneAPI
from django.conf import settings


class RoundoneDashboardView(RoundOneAPI, TemplateView):
    template_name = 'roundone/dashboard-roundone.html'

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
                        data.update(
                            {"requestedDate": datetime.utcfromtimestamp(
                                int(data.get(
                                    'requestedDate', 0))
                                ).strftime("%d %b, %Y")})

                        data.update(
                            {"expiryDate": datetime.utcfromtimestamp(
                                int(data.get(
                                    'expiryDate', 0))
                                ).strftime("%d %b, %Y")})
                        if data.get("acceptedDate") and str(status) == "1":
                            data.update(
                                {"acceptedDate": datetime.utcfromtimestamp(
                                    int(data.get('acceptedDate', 0))
                                    ).strftime("%d %b, %Y")})
                            accepted.append(data)
                        else:
                            pending.append(data)
                    except:
                        pass
        context['accepted'] = accepted
        context['pending'] = pending
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
        context = super(DashboardResultView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        interviewerRating = request.POST.get('interviewerRating')
        roundoneRating = request.POST.get('roundoneRating')
        comments = request.POST.get('comments')
        orderId = kwargs.get('order_id')

        userEmail = request.user.email

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
            except:
                pass

        context = {
            'result': result_json,
            'show_feedback': show_feedback,
            "status": status}

        template_html = render_to_string(
            "dashboard/roundone_result.html", context)
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



class DashboardRoundoneProfileView(RoundOneAPI, TemplateView):
    template_name = "include/roundone_profile.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardRoundoneProfileView, self).get_context_data(**kwargs)
        roundone_profile = self.get_roundone_profile(self.request)

        if roundone_profile.get("response"):
            rouser = roundone_profile.get("user")
            employments = {}
            education = {}
            skill_list = []
            if rouser:
                education = rouser.get("education")
                employments = rouser.get("employments")
                skill_str = rouser.get("skills", "")
                skill_list = skill_str.split(",")
                csrf_token_value = get_token(self.request)

            context.update({
                "rouser": rouser, "education_list": education,
                "employment_list": employments,
                'csrf_token_value': csrf_token_value,
                'skill_list': skill_list
            })
        return context

    def get(self, request, *args, **kwargs):
        return super(DashboardRoundoneProfileView, self).get(request, *args, **kwargs)


class RoundonePersonalSubmit(RoundOneAPI, View):

    def post(self, request, *args, **kwargs):
        try:
            name = request.POST.get("name")
            contact = request.POST.get("mobile")
            total_exp = request.POST.get("total_exp")
            roundone_profile = request.session.get("roundone_profile")
            if not roundone_profile:
                roundone_profile = self.get_roundone_profile(request)
            if roundone_profile.get("response"):
                rouser = roundone_profile.get("user")
                rouser.update({
                    "name": name,
                    "mobile": contact,
                    "total_exp": total_exp,
                    "skills": request.POST.get("skill_str")
                })
                response_json = self.post_roundone_profile(
                    request, roundone_profile)
                if response_json.get("response"):
                    request.session.update({
                        "roundone_profile": roundone_profile})
                    return HttpResponse(json.dumps({
                        "status": True,
                        "message": response_json.get("msg")}))
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return HttpResponse(json.dumps({
            "status": False, "message": "Profile Not Updated"}))