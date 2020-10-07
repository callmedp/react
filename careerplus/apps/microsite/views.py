import logging
import json
import re
from django.views.generic import TemplateView, View
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from .roundoneapi import RoundOneAPI, RoundOneSEO
from users.forms import (
    ModalLoginApiForm,
    ModalRegistrationApiForm,
    PasswordResetRequestForm
)

from .models import MicroSite, PartnerTestimonial, PartnerFaq
from shop.models import Product
from cart.models import Subscription


class PartnerHomeView(TemplateView):
    template_name = 'microsite/roundone-home.html'

    def get_context_data(self, **kwargs):
        context = super(PartnerHomeView, self).get_context_data(**kwargs)
        partner = kwargs.get('partner', '')
        flag_status = False
        try:
            flag_status = Subscription.objects.filter(
                candidateid=self.request.session.get('candidate_id', ''),
                expire_on__gt=timezone.now()).exists()
        except Exception as e:
            logging.getLogger('error_log').error('unable to get subscription status%s' % str(e))
            pass

        try:
            microsite = MicroSite.objects.select_related('home_page').get(
                slug=partner, active=True)

            testimonial_qs = PartnerTestimonial.objects.filter(
                microsite=microsite, active=True)
            faq_qs = PartnerFaq.objects.filter(
                microsite=microsite, active=True)

            context.update({
                "faq_qs": faq_qs, "testimonial_qs": testimonial_qs,
                "loginform": ModalLoginApiForm(),
                "registerform": ModalRegistrationApiForm(),
                'flag': flag_status
            })

            if partner == 'roundone':
                product = Product.objects.filter(id=settings.ROUNDONE_PRODUCT_ID)
                if len(product):
                    context['product'] = product[0]

            context.update(RoundOneAPI().get_location_list(**kwargs))
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
            raise Http404()

        return context

    def get(self, request, *args, **kwargs):
        return super(PartnerHomeView, self).get(request, *args, **kwargs)


class PartnerListView(TemplateView):
    template_name = 'microsite/roundone-list.html'

    def get_context_data(self, **kwargs):
        context = super(PartnerListView, self).get_context_data(**kwargs)
        partner = kwargs.get('partner', '')
        flag_status = False

        try:
            flag_status = Subscription.objects.filter(
                candidateid=self.request.session.get('candidate_id', ''),
                expire_on__gt=timezone.now()).exists()
        except Exception as e:
            logging.getLogger('error_log').error(str(e))

        if partner == 'roundone':
            context.update(self.get_partner_context(**kwargs))
            context.update(self.get_breadcrumb_data())

            context.update({
                "loginform": ModalLoginApiForm(),
                "registerform": ModalRegistrationApiForm(),
                "flag": flag_status,
                "reset_form": PasswordResetRequestForm()
            })
            product = Product.objects.filter(id=settings.ROUNDONE_PRODUCT_ID)
            if len(product):
                context['product'] = product[0]

        return context

    def get(self, request, *args, **kwargs):
        return super(PartnerListView, self).get(request, *args, **kwargs)

    def get_partner_context(self, **kwargs):
        context = {}
        try:
            search_response = RoundOneAPI().get_search_response(
                self.request, **kwargs)
            jsondict = RoundOneAPI().remove_html_tags(search_response)
            context.update({'search_result': jsondict})
            keyword = kwargs.get('keyword', '')
            location = self.request.GET.get('loc', '').split(',')
            initial_keyword = ""
            initial_location = []

            if keyword and keyword != "all":
                initial_keyword = keyword.replace("-", " ")
                context.update({"initial_keyword": initial_keyword})
            if location and "" not in location:
                initial_location = [x for x in location]
                context.update({"initial_location": str(initial_location)})

            clean_keyword = initial_keyword or keyword
            clean_location = ', '.join(initial_location) or kwargs.get(
                'location', '')

            context.update({
                'clean_keyword': clean_keyword,
                'clean_location': clean_location
            })
            seo_data = RoundOneSEO().get_seo_data(
                data_for="listing", **context)
            context.update(seo_data)
            context.update(RoundOneAPI().get_location_list(**kwargs))
            context.update(**kwargs)
            if self.request.session.get('candidate_id', ''):
                if RoundOneAPI().is_premium_user(self.request):
                    context.update({'is_roundone_premium': True})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return context

    def get_breadcrumb_data(self):
        initial_keyword = ""
        keyword = self.kwargs.get('keyword', '')
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        breadcrumbs.append({
            "url": reverse('partner-home', kwargs={'partner': 'roundone'}),
            "name": "Roundone",
        })

        if keyword and keyword != "all":
            initial_keyword = keyword.replace("-", " ")

        clean_keyword = initial_keyword or keyword
        breadcrumbs.append({"url": None, "name": clean_keyword.title()})
        data = {"breadcrumbs": breadcrumbs}
        return data


class PartnerDetailView(TemplateView):
    template_name = 'microsite/roundone-detail.html'

    def get_context_data(self, **kwargs):
        context = super(PartnerDetailView, self).get_context_data(**kwargs)
        partner = kwargs.get('partner', '')
        flag_status = False
        try:
            flag_status = Subscription.objects.filter(
                candidateid=self.request.session.get('candidate_id', ''),
                expire_on__gt=timezone.now()).exists()
        except Exception as e:
            logging.getLogger('error_log').error(str(e))

        if partner:
            context.update(self.get_partner_context(**kwargs))
            context.update({
                "loginform": ModalLoginApiForm(),
                "registerform": ModalRegistrationApiForm(),
                'flag': flag_status,
                "reset_form": PasswordResetRequestForm()
            })
        return context

    def get(self, request, *args, **kwargs):
        return super(PartnerDetailView, self).get(request, *args, **kwargs)

    def get_partner_context(self, **kwargs):
        context = {}
        try:
            detail_response = RoundOneAPI().get_job_detail(
                self.request, **kwargs)
            data = detail_response.get("data")
            if data:
                jd = data.get("jobDescription")
                clean = re.compile('<.*?>')
                text = re.sub(clean, '', jd)
                data.update({"jobDescription": text})
            context.update({'job_detail': detail_response})

            try:
                jobTitle = detail_response.get('data').get('jobTitle')
                breadcrumb_location = slugify(detail_response.get('data').get(
                    'location'))
                context.update({'breadcrumb_location': breadcrumb_location})
            except Exception as e:
                jobTitle = kwargs.get("job_title", "Job Referral")
                logging.getLogger('error_log').error(
                    "%s-%s" % (str(e), jobTitle))

            context.update({
                'jobTitle': jobTitle,
                'job_params': kwargs.get('job_params'),
            })

            breadcrumbs = []
            breadcrumbs.append({"url": '/', "name": "Home"})
            breadcrumbs.append({
                "url": reverse('partner-home', kwargs={'partner': 'roundone'}),
                "name": "Roundone"
            })

            if context.get('jobTitle') and context.get('breadcrumb_location'):
                breadcrumbs.append({
                    "url": '/partner/roundone/all-jobs-in-' + context.get(
                        'breadcrumb_location') + '',
                    "name": "All Jobs in " + context.get(
                        'breadcrumb_location') + "",
                })
                breadcrumbs.append({
                    "url": None,
                    "name": context.get('jobTitle') + "-" + context.get(
                        'breadcrumb_location'),
                })

            seo_data = RoundOneSEO().get_seo_data(data_for="detail", **context)
            context.update({"breadcrumbs": breadcrumbs})
            context.update(seo_data)
            context.update(**kwargs)
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return context


class GetReferenceView(View, RoundOneAPI):

    def get(self, request, *args, **kwargs):
        return super(GetReferenceView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        job_params = request.POST.get('job_params', "").split('-')
        source = request.POST.get('source')
        try:
            if 'candidate_id' in request.session:
                if self.is_premium_user(request):
                    roundone_job_params = request.session.get(
                        "roundone_job_params", "").split('-')
                    roundone_source = request.session.get("roundone_source")
                    origin = request.POST.get("origin")
                    if roundone_job_params and roundone_source:

                        redirect_response = self.post_referral_request(
                            request, roundone_job_params)
                        if redirect_response.get("response"):
                            if redirect_response.get("status") == "-1":
                                return HttpResponse(json.dumps({
                                    "status": False,
                                    "message": redirect_response.get("msg")}))
                            try:
                                del request.session['roundone_job_params']
                                del request.session['roundone_source']
                            except Exception as e:
                                logging.getLogger('error_log').error(str(e))
                                pass
                            if "/dashboard" in origin:
                                return HttpResponse(json.dumps({
                                    'status': True, 'redirect': True,
                                    'redirect_url': roundone_source}))
                    response_json = self.post_referral_request(
                        request, job_params)
                    if response_json.get("response"):
                        status = response_json.get("status")
                        if status == "1" or status == "0":
                            return HttpResponse(json.dumps(
                                {
                                    'status': True, 'response': True,
                                    'message': response_json.get('msg')}))
                        elif status == "-1":
                            msg = self.roundone_message(response_json)
                            return HttpResponse(json.dumps(
                                {'status': True, 'response': False,
                                 'message': msg}))
                    return HttpResponse(json.dumps(
                        {'status': False, 'message': "Sorry! Something went wrong. "
                                                     "You can also use your services on http://www.roundone.in/ "
                                                     "or you can reach out at support@roundone.in"}))
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return HttpResponse(
            json.dumps({'status': False, 'message': 'Sorry! Something went wrong. You can also use your services on '
                                                    'http://www.roundone.in/ or you can reach out at support@roundone.in'}))


class RedirectProfileView(View):

    def post(self, request, *args, **kwargs):
        roundone_job_params = request.POST.get("job_params")
        roundone_source = request.POST.get("source")
        if roundone_job_params and roundone_source:
            request.session.update({
                "roundone_job_params": roundone_job_params,
                "roundone_source": roundone_source
            })
        return HttpResponse(json.dumps({
            "redirect": True,
            "redirect_url": "/dashboard/roundone/profile/"}))


class SaveJobView(View, RoundOneAPI):

    def post(self, request, *args, **kwargs):
        if 'candidate_id' in request.session:
            if self.is_premium_user(request):
                job_params = request.POST.get('job_params', '')
                kwargs.update({'job_params': job_params})
                response_json = self.save_job(request, **kwargs)
                if response_json.get("response"):
                    return HttpResponse(
                        json.dumps(
                            {'status': True, 'response': True,
                             'message': response_json.get('msg')}))
                return HttpResponse(
                    json.dumps(
                        {'status': True, 'response': False,
                        'message': "Roundone is experiencing some technical issues. Please try again later"}))
        return HttpResponseRedirect(reverse('users:login'))
