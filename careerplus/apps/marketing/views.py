#python imports

#django imports
from django.views.generic import TemplateView
from django.http.response import HttpResponsePermanentRedirect
from django.core.cache import cache

#local imports

#inter app imports
from core.mixins import EncodeDecodeUserData

#third party imports
from urllib.parse import parse_qs
from geolocation.models import Country

class MarketingPages(TemplateView):
    template_name = 'marketing/'
    cache_key='countri'
    def _decode_user_info_from_token(self,alt):
        decoded_tuple = EncodeDecodeUserData().decode(alt)
        if not decoded_tuple:
            return {}
        return {"alt_email":decoded_tuple[0],
                "alt_name":decoded_tuple[1],
                "alt_contact":decoded_tuple[2]}
    def get(self, request, *args, **kwargs):
        redirect_mapping = {
                            "/digital-marketing":"/online-marketing",
                            "/gst-cert":"/gst-certification",
                            "/pmp-cert":"/pmp-certification",
                            "/data-science-certification":"/data-science-cert",
                            "/resume-writing":"/resume-writing-services"
                            }
        redirect_path = redirect_mapping.get(self.request.path)
        if redirect_path:
            return HttpResponsePermanentRedirect(redirect_path)
        return super(MarketingPages, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(MarketingPages, self).get_context_data(**kwargs)
        alt = self.request.GET.get('alt')
        if alt:
            context.update(self._decode_user_info_from_token(alt))
        full_path = self.request.get_full_path()
        path = full_path.lstrip('/').split('?')
        tpl_path = path[0]
        if '.html' not in path[0]:
            tpl_path = tpl_path + '.html'
        self.template_name = self.template_name + tpl_path
        params_dict = parse_qs(full_path)
        allowed_keys = ['cmp', 'keyword', 'placement']
        allowed_val = [path[0]]
        for key in allowed_keys:
            allowed_val.append(key + ': ' + str(params_dict.get(key, [0])[0]))
        source = ', '.join(allowed_val)
        context.update({'source': source, 'lead_source': 4})
        count_obj = cache.get("countri", "")
        if count_obj:
            context['countries'] = count_obj
            return context
        else:
            countreey = list(Country.objects.filter(active=True)\
                .values_list('phone', flat=True))
            countries = [int(countr) for countr in countreey if countr and countr.isdigit()]
            countries = list(set(countries))
            countries.sort()
            # countries.values_list('phone', flat=True).order_by('phone').distinct()
            context.update({
                "countries": countries,
            })
            cache.set(self.cache_key, countries, 86400*30)
            return context