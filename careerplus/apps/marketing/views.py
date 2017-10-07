from urllib.parse import parse_qs

from django.views.generic import TemplateView

from geolocation.models import Country


class MarketingPages(TemplateView):
    template_name = 'marketing/'

    def get(self, request, *args, **kwargs):
        return super(MarketingPages, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MarketingPages, self).get_context_data(**kwargs)
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
        context.update({'source': source, 'lead_source': 6})
        countries = Country.objects.filter(active=True)
        countries = countries.exclude(phone='')
        context.update({
            "countries": countries,
        })
        return context
