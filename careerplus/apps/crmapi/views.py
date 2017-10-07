import json
import logging

from django.views.generic import View
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from geolocation.models import Country
from .models import UserQuries


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
            country = request.POST.get('country', '')
            source = request.POST.get('source', '')
            queried_for = request.POST.get('queried_for', '')
            lead_source = request.POST.get('lsource', '0')
            selection = request.POST.get('selection', None)
            path = request.POST.get('path', '')
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