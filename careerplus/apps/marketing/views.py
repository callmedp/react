#python imports

#django imports
from django.views.generic import TemplateView
from django.http.response import HttpResponsePermanentRedirect
from django.core.cache import cache
from urllib.parse import urlencode
from django.conf import settings
#local imports

#inter app imports
from core.mixins import EncodeDecodeUserData
from linkedin.autologin import AutoLogin
from shine.core import ShineCandidateDetail
from .data import *

from shop.models import Product

#third party imports
from urllib.parse import parse_qs
from geolocation.models import Country
from users.models import User
from haystack.query import SearchQuerySet

class MarketingPages(TemplateView):

    template_name = 'marketing/'
    cache_key='cache_key_country'

    def _decode_user_info_from_token(self,alt):
        decoded_tuple = EncodeDecodeUserData().decode(alt)
        if not decoded_tuple:
            return {}
        return {"alt_email": decoded_tuple[0],
                "alt_name": decoded_tuple[1],
                "alt_contact": decoded_tuple[2]}

    def get(self, request, *args, **kwargs):
        valid = False
        email = None
        candidateid = None

        if request.GET.get("token",""):
            try:
                email, candidateid, valid = AutoLogin().decode(request.GET.get("token",""))
            except Exception as e:
                pass

            if valid and email and candidateid:
                resp_status = ShineCandidateDetail().get_status_detail(email=None, shine_id=candidateid)
                if resp_status:
                    request.session.update(resp_status)
        
        non_terminating_url_slugs = ['aws-cert','ban-cert','data-science','international-resume-writing',
                                     'linkedin','linkedin-1','international-resume-writing-1']
        redirect_mapping = {
                            "/digital-marketing": "/online-marketing",
                            "/gst-cert": "/gst-certification",
                            "/pmp-cert": "/pmp-certification",
                            "/data-science-certification": "/data-science-cert",
                            "/resume-writing": "/resume-writing-services",
                            }
        redirect_mapping.update({"/"+value+".html" :"/"+value for value in non_terminating_url_slugs})
        redirect_path = redirect_mapping.get(self.request.path)
        if redirect_path:
            redirect_path += '?' + urlencode(self.request.GET)
            return HttpResponsePermanentRedirect(redirect_path)
        return super(MarketingPages, self).get(request, *args, **kwargs)

    def get_template_names(self):

        full_path = self.request.get_full_path()
        path = full_path.lstrip('/').split('?')
        return ["marketing/" + path[0] + '.html']

    def get_context_data(self, **kwargs):
        context = super(MarketingPages, self).get_context_data(**kwargs)
        alt = self.request.GET.get('alt')
        if alt:
            context.update(self._decode_user_info_from_token(alt))
        full_path = self.request.get_full_path()
        path = full_path.lstrip('/').split('?')
        # tpl_path = path[0]
        # if '.html' not in path[0]:
        #     tpl_path = tpl_path + '.html'
        prod_keys, select = settings.URL_MAPPING_TO_PRODUCT.get(path[0],(None,None))
        if prod_keys:
            prod_obj = []
            for pk in prod_keys:
                cache_map_prod = cache.get('detail_solr_product_' + str(pk))
                if cache_map_prod:
                    prod_obj.append(cache_map_prod)
                else:
                    prd = SearchQuerySet().filter(id=pk)
                    if prd:
                        prd = prd[0]
                        cache.set('detail_solr_product_' + str(pk), prd, 60*60*4)
                        prod_obj.append(prd)
            context.update({'products_lists': prod_obj})
            context.update({'select': select})
        # self.template_name = self.template_name + tpl_path
        params_dict = parse_qs(full_path)
        allowed_keys = ['cmp', 'keyword', 'placement']
        allowed_val = [path[0]]
        for key in allowed_keys:
            allowed_val.append(key + ': ' + str(params_dict.get(key, [0])[0]))
        source = ', '.join(allowed_val)
        context.update({'source': source, 'lead_source': 4})
        count_obj = cache.get(self.cache_key, "")
        if count_obj:
            context['countries'] = count_obj
            return context
        else:
            country_object_list = list(Country.objects.filter(active=True)\
                .values_list('phone', flat=True))
            countries = [int(countr) for countr in country_object_list if countr and countr.isdigit()]
            countries = list(set(countries))
            countries.sort()
            # countries.values_list('phone', flat=True).order_by('phone').distinct()
            context.update({
                "countries": countries,
            })
            cache.set(self.cache_key, countries, 86400*30)
            return context