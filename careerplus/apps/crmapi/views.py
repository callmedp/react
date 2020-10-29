import json
import logging
import requests
from django.views.generic import View
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from geolocation.models import Country
from .models import (
    UserQuries, DEFAULT_SLUG_SOURCE,
    UNIVERSITY_LEAD_SOURCE)
from .tasks import create_lead_crm


class ReCaptchaMixin(object):

    def confirm_recaptcha(self, recaptcha_response=None, remoteip=None):
        response = {}
        url = settings.GOOGLE_RECAPTCHA_URL
        payload = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET,
            'response': recaptcha_response,
            'remoteip': remoteip,
        }
        verify = requests.get(url, params=payload, verify=True)
        verify = verify.json()
        response["status"] = verify.get("success", False)
        response['message'] = verify.get('error-codes', None) or "Unspecified error."
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class LeadManagement(View):

    @csrf_exempt
    def dispatch(self,request,*args,**kwargs):
        return super(LeadManagement,self).dispatch(request,*args,**kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        created = False
        try:
            email = request.POST.get('email', '')
            university_course = request.POST.get('uc', 0)
            mobile = request.POST.get('number', '')
            name = request.POST.get('name', '')
            msg = request.POST.get('msg', '')
            prd = request.POST.get('prd', '')
            product_id = request.POST.get('product', 0)
            country = request.POST.get('country', '91')
            source = request.POST.get('source', '')
            queried_for = request.POST.get('queried_for', '')
            lead_source = request.POST.get('lsource', 0)
            selection = request.POST.get('selection', 0)
            company = request.POST.get('cname','')
            path = request.POST.get('path', '')
            rejectlist = ['http', 'www', 'href', '***', 'url', '<html>']
            product_offer = request.POST.get('product_offer', True)

            if any(rejectkey in msg for rejectkey in rejectlist):
                return HttpResponse(json.dumps({'status': False}))

            name = name + ' (' + company+')'if company else name
            try:
                product_id = int(product_id)
            except Exception as e:
                logging.getLogger('error_log').error('unable to get product id%s'%str(e))
                product_id = 0
            try:
                lead_source = int(lead_source)
            except Exception as e:
                logging.getLogger('error_log').error('unable to get lead source%s'%str(e))

                lead_source = 0

            medium = 0

            if request.flavour == 'mobile':
                medium = 1
                source = 'mobile-' + source

            if queried_for:
                source = source + "-" + queried_for

            try:
                country = Country.objects.get(phone=country)
            except Exception as e:
                logging.getLogger('error_log').error('unable to get country object%s'%str(e))
                country = Country.objects.get(phone='91')

            utm = request.session.get('utm', {})
            campaign_slug = request.POST.get('campaign',utm.get('utm_campaign'))
            sub_campaign_slug = utm.get('sub_campaign_slug')
            utm_parameter = json.dumps(utm)
            
            if not campaign_slug:
                slug_source = dict(DEFAULT_SLUG_SOURCE)
                campaign_slug = slug_source.get(int(lead_source))

            if university_course:
                request.session['university_course'] = True
                request.session['lead_email'] = email
                request.session['lead_mobile'] = mobile
                if " " in name:
                    first_name = name.split(" ")[0]
                    last_name = " ".join(name.split(" ")[1:len(name)])
                else:
                    first_name = name
                    last_name = ""
                request.session['lead_first_name'] = first_name
                request.session['lead_last_name'] = last_name

            lead = UserQuries.objects.create(
                name=name,
                email=email,
                country=country,
                phn_number=mobile,
                message=msg,
                lead_source=lead_source,
                product=prd,
                product_id=product_id,
                medium=medium,
                source=source,
                path=path,
                utm_parameter=utm_parameter,
                campaign_slug=campaign_slug,
                sub_campaign_slug=sub_campaign_slug
            )
            created = True
            validate = True if lead.email else False
            create_lead_crm.delay(pk=lead.pk, validate=validate, product_offer=product_offer)
        except Exception as e:
            logging.getLogger('error_log').error('lead creation is failed%s'%str(e))

        response_dict = json.dumps({'status': created, })
        response = HttpResponse(response_dict)
        return response

class LeadManagementWithCaptcha(View, ReCaptchaMixin):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        created = False
        try:
            email = request.POST.get('email', '')
            mobile = request.POST.get('number', '')
            name = request.POST.get('name', '')
            msg = request.POST.get('msg', '')
            prd = request.POST.get('prd', '')
            try:
                product_id = int(request.POST.get('product', 0))
            except Exception as e:
                logging.getLogger('error_log').error('unable to get product id%s'%str(e))

                product_id = 0
                
            country = request.POST.get('country', '91')
            source = request.POST.get('source', '')
            queried_for = request.POST.get('queried_for', '')
            lead_source = request.POST.get('lsource', '0')

            selection = request.POST.get('selection', None)

            path = request.POST.get('path', '')
            rejectlist = ['http', 'www', 'href', '***', 'url', '<html>']
            recaptcha_response = request.POST.get('g-recaptcha-response', None)
            
            if any(rejectkey in msg for rejectkey in rejectlist):
                return HttpResponse(json.dumps({'status': False}))
            remoteip = self.get_client_ip(request=request)
            recaptcha = self.confirm_recaptcha(recaptcha_response=recaptcha_response, remoteip=remoteip) 
            if not recaptcha.get('status', False):
                response_error_dict = json.dumps({'status': False, 'recaptcha': False})
                return HttpResponse(response_error_dict)
            
            try:
                lead_source = int(lead_source)
            except Exception as e:
                logging.getLogger('error_log').error('unable to get lead source %s'%str(e))

                lead_source = 0

            medium = 0

            if request.flavour == 'mobile':
                medium = 1
                source = 'mobile-' + source

            if queried_for:
                source = source + "-" + queried_for

            try:
                country = Country.objects.get(phone=country)
            except Exception as e:
                logging.getLogger('error_log').error('unable to get country object%s'%str(e))

                country = Country.objects.get(phone='91')

            utm = request.session.get('utm', {})
            sub_campaign_slug = utm.get('sub_campaign_slug')
            campaign_slug = utm.get('utm_campaign', '')
            utm_parameter = json.dumps(utm)
            if not campaign_slug:
                slug_source = dict(DEFAULT_SLUG_SOURCE)
                campaign_slug = slug_source.get(int(lead_source))

            lead = UserQuries.objects.create(
                name=name,
                email=email,
                country=country,
                phn_number=mobile,
                message=msg,
                lead_source=lead_source,
                product=prd,
                product_id=product_id,
                medium=medium,
                source=source,
                path=path,
                utm_parameter=utm_parameter,
                campaign_slug=campaign_slug,
                sub_campaign_slug=sub_campaign_slug
            )

            created = True
            create_lead_crm.delay(pk=lead.pk, validate=True)
            response_dict = json.dumps({'status': created, 'recaptcha': True})
            response = HttpResponse(response_dict)
            return response
        except Exception as e:
            logging.getLogger('error_log').error('lead creation with captcha is failed%s'%str(e))

        response_dict = json.dumps({'status': False, 'recaptcha': True})
        response = HttpResponse(response_dict)
        return response

    def dispatch(self, *args, **kwargs):
        return super(LeadManagementWithCaptcha, self).dispatch(*args, **kwargs)