# Python Imports
import json
import logging

# Core Django Imports
from crmapi.models import (UserQuries, DEFAULT_SLUG_SOURCE)
from crmapi.tasks import create_lead_crm
# Third Party Imports
from geolocation.models import Country
from rest_framework import permissions, status
# Core RestFramework Imports
from rest_framework.views import APIView

# Local Imports
from .helper import APIResponse


# Inter App Imports


class LeadManagementAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        """
        Need help Section:
        Getting the request from user like email, mobile, name, msg etc to create a lead
        in the back-end.
        Variables can be dynamic but the email or mobile should be neccessary.
        """

        # Specify the lead is not created yet
        created = False

        try:
            email = request.POST.get('email', '')
            university_course = request.POST.get('uc', 0)
            mobile = request.POST.get('number', '')
            name = request.POST.get('name', '')
            msg = request.POST.get('msg', '')
            prd = request.POST.get('prd', '')
            product_id = request.POST.get('product', '')
            country = request.POST.get('country', '91')
            source = request.POST.get('source', '')
            queried_for = request.POST.get('queried_for', '')
            lead_source = request.POST.get('lsource', 0)
            selection = request.POST.get('selection', 0)
            company = request.POST.get('cname', '')
            path = request.POST.get('path', '')
            rejectlist = ['http', 'www', 'href', '***', 'url', '<html>']
            product_offer = request.POST.get('product_offer', True)
            name = name + '(' + company + ')' if company else name
            medium = 0

            if any(rejectkey in msg for rejectkey in rejectlist):
                return APIResponse(message='Something went wrong', status=status.HTTP_400_BAD_REQUEST)

            try:
                # In case not able to find product
                product_id = int(product_id)
            except Exception as e:
                logging.getLogger('error_log').error('Unable to get the product id {}'.format(str(e)))
                product_id = 0

            try:
                # In case not able to get the lead source
                lead_source = int(lead_source)
            except Exception as e:
                logging.getLogger('error_log').error('Unable to get lead source'.format(str(e)))
                lead_source = 0

            if request.flavour == 'mobile':
                medium = 1
                source = 'mobile-' + source

            if queried_for:
                source = source + '-' + queried_for

            try:
                country = Country.objects.get(phone=country)
            except Exception as e:
                logging.getLogger('error_log').error('unable to get country object%s' % str(e))
                country = Country.objects.get(phone='91')

            utm = request.session.get('utm', {})
            campaign_slug = request.POST.get('campaign', utm.get('utm_campaign'))
            sub_campaign_slug = utm.get('sub_campaign_slug')
            utm_parameter = json.dumps(utm)

            if not campaign_slug:
                slug_source = dict(DEFAULT_SLUG_SOURCE)
                campaign_slug = slug_source.get(int(lead_source))

            if university_course:
                request.session['university_course'] = True
                request.session['lead_mail'] = email
                request.session['lead_mobile'] = mobile

                if " " in name:
                    first_name = name.split(" ")[0]
                    last_name = " ".join(name.split(" ")[1:len(name)])
                else:
                    first_name = name
                    last_name = ""
                request.session['lead_first_name'] = first_name
                request.session['lead_last_name'] = last_name

            # Lead Storing Queries
            lead = UserQuries.objects.create(name=name,
                                             email=email,
                                             country=country,
                                             phn_numnber=mobile,
                                             message=msg,
                                             lead_source=lead_source,
                                             product=prd,
                                             product_id=product_id,
                                             medium=medium,
                                             source=source,
                                             path=path,
                                             utm_parameter=utm_parameter,
                                             campaign_slug=campaign_slug,
                                             sub_campaign_slug=sub_campaign_slug)
            created = True
            validate = True if lead.email else False
            create_lead_crm.delay(pk=lead.pk, validate=validate, product_offer=product_offer)
            return APIResponse(message='Thank you for your response', status=status.HTTP_201_CREATED)

        except Exception as e:
            logging.getLogger('error_log').error('Lead Creation failed {}'.format(str(e)))
            return APIResponse(message='Something went wrong, \n Please try again!', status=status.HTTP_400_BAD_REQUEST)