import logging

from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.utils.text import slugify

from .roundoneapi import RoundOneAPI, RoundOneSEO
from .models import MicroSite, PartnerTestimonial, PartnerFaq


class PartnerHomeView(TemplateView):
    template_name = 'microsite/roundone-home.html'

    def get_context_data(self, **kwargs):
        context = super(PartnerHomeView, self).get_context_data(**kwargs)
        partner = kwargs.get('partner', '')

        try:
            microsite = MicroSite.objects.select_related('home_page').get(
                slug=partner, active=True)
            banner_image_list = microsite.home_page.banner_image.filter(active=True)
            testimonial_qs = PartnerTestimonial.objects.filter(microsite=microsite,
                active=True)
            faq_qs = PartnerFaq.objects.filter(microsite=microsite, active=True)
            pv = None

            # if microsite.slug == 'roundone':
            #     pv = ProductVariation.objects.get(pk=1295)

            context.update({
                "banner_image_list": banner_image_list, "faq_qs": faq_qs,
                "testimonial_qs": testimonial_qs, "pv": pv,
            })

            context.update(RoundOneAPI().get_location_list(**kwargs))
        except:
            raise Http404()

        return context

    def get(self, request, *args, **kwargs):
        return super(PartnerHomeView, self).get(request, *args, **kwargs)


class PartnerListView(TemplateView):
    template_name = 'microsite/roundone-list.html'
    
    def get_context_data(self, **kwargs):
        context = super(PartnerListView, self).get_context_data(**kwargs)
        partner = kwargs.get('partner', '')

        if partner == 'roundone':
            context.update(self.get_partner_context(**kwargs))
            context.update(self.get_breadcrumb_data())

            try:
                microsite = MicroSite.objects.select_related(
                    'listing_page').get(slug=partner, active=True)
                banner_image_list = microsite.listing_page.banner_image.filter(
                    active=True)
                context.update({'banner_image_list': banner_image_list})
            except Exception as e:
                logging.getLogger('error_log').error(str(e))
        return context

    def get(self, request, *args, **kwargs):
        return super(PartnerListView, self).get(request, *args, **kwargs)

    def get_partner_context(self, **kwargs):
        context = {}
        try:
            search_response = RoundOneAPI().get_search_response(self.request, **kwargs)
            context.update({'search_result': search_response})
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
            clean_location = ', '.join(initial_location) or kwargs.get('location', '')

            context.update({
               'clean_keyword': clean_keyword,
               'clean_location': clean_location
            })

            context.update(RoundOneSEO().get_seo_data(data_for="listing", **context))
            context.update(RoundOneAPI().get_location_list(**kwargs))
            context.update(**kwargs)
            if self.request.user.is_authenticated():
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
        breadcrumbs.append({"url": '/partner/roundone/', "name": "Roundone"})

        if keyword and keyword != "all":
            initial_keyword = keyword.replace("-", " ")

        clean_keyword = initial_keyword or keyword

        breadcrumbs.append({"url": None, "name": clean_keyword})
        data = {"breadcrumbs": breadcrumbs}
        return data


class PartnerDetailView(TemplateView):
    template_name = 'microsite/roundone-detail.html'

    def get_context_data(self, **kwargs):
        context = super(PartnerDetailView, self).get_context_data(**kwargs)
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
            return super(PartnerDetailView, self).get(request, *args, **kwargs)
        # return HttpResponseRedirect(reverse_lazy('gosf:gosf_home'))

    def get_partner_context(self, **kwargs):
        context = {}
        try:
            detail_response = RoundOneAPI().get_job_detail(self.request, **kwargs)
            data = detail_response.get("data")
            if data:
                jd = data.get("jobDescription")
                data.update({"jobDescription": jd.replace("\\n", "<br>")})
            context.update({'job_detail': detail_response})

            try:
                jobTitle = detail_response.get('data').get('jobTitle')
                breadcrumb_location = slugify(detail_response.get('data').get('location'))
                context.update({'breadcrumb_location': breadcrumb_location})
            except:
                jobTitle = kwargs.get("job_title", "Job Referral")
            context.update({'jobTitle': jobTitle})

            breadcrumbs = []
            breadcrumbs.append({"url": '/', "name": "Home"})
            breadcrumbs.append({"url": '/partner/roundone/', "name": "Roundone"})

            if context.get('jobTitle') and context.get('breadcrumb_location'):
                breadcrumbs.append({
                    "url": '/partner/roundone/all-jobs-in-'+context.get('breadcrumb_location')+'',
                    "name": "All Jobs in "+context.get('breadcrumb_location')+"",
                })
                breadcrumbs.append({
                    "url": None,
                    "name": context.get('jobTitle')+"-"+context.get('breadcrumb_location'),
                })

            seo_data = RoundOneSEO().get_seo_data(data_for="detail", **context)
            context.update({"breadcrumbs": breadcrumbs})
            context.update(seo_data)
            context.update(**kwargs)
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
        return context
