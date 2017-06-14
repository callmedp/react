import json
import logging

from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import Http404
from shinecp.cart.models import ProductVariation
from shinecp.cart.views import CommonContext
from .models import MicroSite, PartnerTestimonial, PartnerFaq
from .mixins import CommonMethodMixin
from .forms import RoundoneRegisterForm
from .roundone import RoundOneAPI
from .tasks import roundone_query_save

class PartnerHomeView(TemplateView, CommonContext, CommonMethodMixin):
    default_template = 'microsite/roundone/home.html'
    partner_template = 'microsite/{partner}/home.html'

    def get_context_data(self, **kwargs):
        context = super(PartnerHomeView, self).get_context_data(**kwargs)
        context.update(self.get_common_context_data(**kwargs))
        partner = kwargs.get('partner', '')

        if partner:
            try:
                microsite = MicroSite.objects.select_related('home_page').get(
                    slug=partner, active=True)
                banner_image_list = microsite.home_page.banner_image.filter(
                    active=True)
                context.update(self.get_partner_context(microsite, **kwargs))
                context.update({
                    'banner_image_list': banner_image_list,
                    })
            except:
                raise Http404()
        return context

    def get(self, request, *args, **kwargs):
        partner = kwargs.get('partner', '')


        if partner:
            self.template_name = self.get_partner_template(partner)
            return super(PartnerHomeView, self).get(request, *args, **kwargs)

        return HttpResponseRedirect(reverse_lazy('gosf:gosf_home'))

    def get_partner_context(self, microsite, **kwargs):
        testimonial_qs = PartnerTestimonial.objects.filter(
            microsite=microsite, active=True)

        faq_qs = PartnerFaq.objects.filter(microsite=microsite, active=True)
        pv = None
        if microsite.slug == 'roundone':
            pv = ProductVariation.objects.get(pk=1295)
        context = {
            'testimonial_qs': testimonial_qs,
            'faq_qs': faq_qs,
            'pv': pv
        }

        try:
            fullpath = self.__module__.split(
                '.')[0] + ".{partner}.get_{partner}_context_home".format(
                partner=microsite.slug)
            context_func = self.import_dynamically(fullpath)
            partner_context = context_func(**kwargs)
            context.update(partner_context)
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return context


class PartnerListView(CommonContext, CommonMethodMixin, TemplateView):
    default_template = 'microsite/roundone/listing.html'
    partner_template = 'microsite/{partner}/listing.html'

    def get_context_data(self, **kwargs):
        context = super(PartnerListView, self).get_context_data(**kwargs)
        context.update(self.get_common_context_data(**kwargs))
        partner = kwargs.get('partner', '')
        if partner:
            context.update(self.get_partner_context(**kwargs))
            try:
                microsite = MicroSite.objects.select_related(
                    'listing_page').get(slug=partner, active=True)
                banner_image_list = microsite.listing_page.banner_image.filter(
                    active=True)
                context.update({
                    'banner_image_list': banner_image_list,
                    })
            except:
                pass
        return context

    def get(self, request, *args, **kwargs):
        partner = kwargs.get('partner', '')
        if partner:
            self.template_name = self.get_partner_template(partner)
            return super(PartnerListView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy('gosf:gosf_home'))

    def get_partner_context(self, **kwargs):
        context = {}
        try:
            fullpath = self.__module__.split('.')[0] + ".{partner}.get_{partner}_context_listing".format(partner=kwargs.get('partner', ''))
            context_func = self.import_dynamically(fullpath)
            partner_context = context_func(self.request, **kwargs)
            context.update(partner_context)
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return context


class PartnerDetailView(CommonContext, CommonMethodMixin, TemplateView):
    default_template = 'microsite/roundone/detail.html'
    partner_template = 'microsite/{partner}/detail.html'

    def get_context_data(self, **kwargs):
        context = super(PartnerDetailView, self).get_context_data(**kwargs)
        context.update(self.get_common_context_data(**kwargs))
        partner = kwargs.get('partner', '')
        if partner:
            context.update(self.get_partner_context(**kwargs))
            try:
                microsite = MicroSite.objects.select_related(
                    'detail_page').get(slug=partner, active=True)
                banner_image_list = microsite.detail_page.banner_image.filter(active=True)
                context.update({
                    'banner_image_list': banner_image_list,
                    })
            except:
                pass
        return context

    def get(self, request, *args, **kwargs):
        partner = kwargs.get('partner', '')
        if partner:
            self.template_name = self.get_partner_template(partner)
            return super(PartnerDetailView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy('gosf:gosf_home'))

    def get_partner_context(self, **kwargs):
        context = {}
        try:
            fullpath = self.__module__.split('.')[0] + ".{partner}.get_{partner}_context_detail".format(partner=kwargs.get('partner', ''))
            context_func = self.import_dynamically(fullpath)
            partner_context = context_func(self.request, **kwargs)
            context.update(partner_context)
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return context


class GetReferenceView(CommonContext, RoundOneAPI, View):

    def get(self, request, *args, **kwargs):
        return super(GetReferenceView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        job_params = request.POST.get('job_params', "").split('-')
        source = request.POST.get('source')

        try:
            if request.user.is_authenticated():
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
                            except:
                                pass
                            if "/dashboard" in origin:
                                return HttpResponse(json.dumps({
                                    'status': True, 'redirect': True,
                                    'redirect_url': roundone_source}))

                    response_json = self.post_referral_request(
                        request, job_params)

                    if response_json.get("response"):
                        status = response_json.get("status")
                        if status and status == "1" or status == "0":
                            return HttpResponse(json.dumps(
                                {'status': True, 'response': True,
                                 'message': response_json.get('msg')}))
                        elif status == "-1":
                            try:
                                return HttpResponse(json.dumps(
                                    {'status': True, 'response': False,
                                     'message': response_json.get('msg').values[0][0]}))
                            except:
                                return HttpResponse(json.dumps(
                                    {'status': True, 'response': False,
                                     'message': response_json.get('msg')}))
                    return HttpResponse(json.dumps(
                        {'status': False, 'message': "Something went wrong."}))

            try:
                if self.add_cart_roundone():
                    request.session.update({
                        "roundone_job_params": '-'.join(job_params),
                        "roundone_source": source
                        })
                    return HttpResponse(
                        json.dumps({'status': True, 'show_cart': True}))
            except Exception as e:
                logging.getLogger('error_log').error(str(e))
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return HttpResponse(
            json.dumps({'status': False, 'message': 'Something went wrong.'}))


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
            "redirect_url": "/dashboard/roundone?tab=tab_roundone_profile"}))


class SaveJobView(CommonContext, RoundOneAPI, View):
    def get(self, request, *args, **kwargs):
        return super(GetReferenceView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
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
                         'message': "Something went wrong."}))
            try:
                if self.add_cart_roundone():
                    return HttpResponse(
                        json.dumps({'status': True, 'show_cart': True}))
            except:
                pass
        else:
            return HttpResponse(
                json.dumps({
                    'status': False, 'show_login': True,
                    'message': 'Log in or Error...'}))
        return HttpResponse(json.dumps({
            'status': False, 'message': 'Something went wrong.'}))


class RoundoneRegisterView(FormView):
    template_name = "microsite/roundone/register.html"
    form_class = RoundoneRegisterForm

    def get_context_data(self, *args, **kwargs):
        context = super(
            RoundoneRegisterView, self).get_context_data(*args, **kwargs)
        context.update({'partner': kwargs.get('partner', 'roundone')})
        return context

    def post(self, request, *args, **kwargs):
        return super(RoundoneRegisterView, self).post(request, *args, **kwargs)


class RoundoneAboutUsView(TemplateView, CommonContext):
    template_name = "microsite/roundone/aboutus.html"
    
    def get(self, request, *args, **kwargs):
        try:
            jobId = request.GET.get('jobId','')
            refId = request.GET.get('refId','')
            appId = request.GET.get('appId','')

            if appId:
                roundone_query_save.delay({
                'appId': appId,
                'jobId': jobId,
                'refId': refId})
        except:
            pass

        return super(RoundoneAboutUsView, self).get(request, *args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super(
            RoundoneAboutUsView, self).get_context_data(*args, **kwargs)
        context.update(self.get_common_context_data(**kwargs))
        partner = 'roundone'

        try:
            microsite = MicroSite.objects.select_related('home_page').get(
                slug=partner, active=True)
            banner_image_list = microsite.home_page.banner_image.filter(
                active=True)
            context.update(self.get_partner_context(microsite, **kwargs))
            context.update({
                'banner_image_list': banner_image_list,
                })
        except:
            raise Http404()
        return context

    def get_partner_context(self, microsite, **kwargs):
        testimonial_qs = PartnerTestimonial.objects.filter(
            microsite=microsite, active=True)

        faq_qs = PartnerFaq.objects.filter(microsite=microsite, active=True)
        pv = None
        if microsite.slug == 'roundone':
            pass
            # pv = ProductVariation.objects.get(pk=1295)

        context = {
            'testimonial_qs': testimonial_qs,
            'faq_qs': faq_qs,
            'pv': pv
            }
        return context





class RoundoneReferralView(TemplateView, CommonContext):
    template_name = "microsite/roundone/jobreferral.html"

    def get(self, request, *args, **kwargs):
        try:
            jobId = request.GET.get('jobId','')
            refId = request.GET.get('refId','')
            appId = request.GET.get('appId','')

            if appId:
                roundone_query_save.delay({
                'appId': appId,
                'jobId': jobId,
                'refId': refId})
        except:
            pass

        return super(RoundoneReferralView, self).get(request, *args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context = super(
            RoundoneReferralView, self).get_context_data(*args, **kwargs)
        context.update(self.get_common_context_data(**kwargs))
        partner = 'roundone'

        try:
            microsite = MicroSite.objects.select_related('home_page').get(
                slug=partner, active=True)
        except:
            raise Http404()
        pv = None
        if microsite.slug == 'roundone':
            pv = ProductVariation.objects.get(pk=1295)

        context.update({
            'pv': pv
            })
        return context

    