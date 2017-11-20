import json
import logging
import requests
from django.views.generic import View
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from geolocation.models import Country
from .models import UserQuries


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
    def post(self, request, *args, **kwargs):
        created = False
        try:
            email = request.POST.get('email', '')
            mobile = request.POST.get('number', '')
            name = request.POST.get('name', '')
            msg = request.POST.get('msg', '')
            prd = request.POST.get('prd', '')
            product = request.POST.get('product', 0)
            country = request.POST.get('country', '')
            source = request.POST.get('source', '')
            queried_for = request.POST.get('queried_for', '')
            lead_source = request.POST.get('lsource', '0')
            selection = request.POST.get('selection', None)
            path = request.POST.get('path', '')
            rejectlist = ['http', 'www', 'href', '***', 'url', '<html>']
            if any(rejectkey in msg for rejectkey in rejectlist):
                return HttpResponse(json.dumps({'status': False}))
            try:
                product = int(product)
            except:
                product = 0
            try:
                lead_source = int(lead_source)
            except:
                lead_source = 0

            medium = 0

            if request.flavour == 'mobile':
                medium = 1
                source = 'mobile-' + source

            if queried_for:
                source = source + "-" + queried_for

            try:
                country = Country.objects.get(phone=country)
            except:
                country = Country.objects.get(phone='91')

            utm_parameter = json.dumps({
                "utm_content": request.GET.get("utm_content", ''),
                "utm_term": request.GET.get("utm_term", ''),
                "utm_medium": request.GET.get("utm_medium", ''),
                "utm_campaign": request.GET.get("utm_campaign", ''),
                "utm_source": request.GET.get("utm_source", '')
            })
            UserQuries.objects.create(
                name=name,
                email=email,
                country=country,
                phn_number=mobile,
                message=msg,
                lead_source=lead_source,
                product=prd,
                product_id=product,
                medium=medium,
                source=source,
                path=path,
                utm_parameter=utm_parameter,
                campaign_slug=request.GET.get("utm_campaign", '')
            )
            created = True
        except Exception as e:
            logging.getLogger('error_log').error(str(e))

        # try:
        #     if selection:
        #         prd_var = ProductVariation.objects.get(pk=selection)
        #         order = self.get_or_create_order()
        #         units = 1
        #         order_items = order.add_order_items(prd_var, [], units)
        # except Exception as e:
        #     logging.getLogger('error_log').error("%s - %s" % (e, 'Fail to add Product'))
        #     pass

        response_dict = json.dumps({'status': created, })
        response = HttpResponse(response_dict)
        return response

    def dispatch(self, *args, **kwargs):
        return super(LeadManagement, self).dispatch(*args, **kwargs)


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
            country = request.POST.get('country', '')
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
            except:
                lead_source = 0

            medium = 0

            if request.flavour == 'mobile':
                medium = 1
                source = 'mobile-' + source

            if queried_for:
                source = source + "-" + queried_for

            try:
                country = Country.objects.get(phone=country)
            except:
                country = Country.objects.get(phone='91')

            UserQuries.objects.create(
                name=name,
                email=email,
                country=country,
                phn_number=mobile,
                message=msg,
                lead_source=lead_source,
                product=prd,
                medium=medium,
                source=source,
                path=path,
            )
            created = True
            response_dict = json.dumps({'status': created, 'recaptcha': True})
            response = HttpResponse(response_dict)
            return response
        except Exception as e:
            logging.getLogger('error_log').error(str(e))

        # try:
        #     if selection:
        #         prd_var = ProductVariation.objects.get(pk=selection)
        #         order = self.get_or_create_order()
        #         units = 1
        #         order_items = order.add_order_items(prd_var, [], units)
        # except Exception as e:
        #     logging.getLogger('error_log').error("%s - %s" % (e, 'Fail to add Product'))
        #     pass

        response_dict = json.dumps({'status': False, 'recaptcha': True})
        response = HttpResponse(response_dict)
        return response

    def dispatch(self, *args, **kwargs):
        return super(LeadManagementWithCaptcha, self).dispatch(*args, **kwargs)