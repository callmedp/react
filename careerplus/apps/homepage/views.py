import logging

from django.views.generic import TemplateView
from django.conf import settings

from django_redis import get_redis_connection
from haystack.query import SearchQuerySet


from shop.models import ProductClass, FunctionalArea, Skill
from search.helpers import get_recommendations
from core.library.haystack.query import SQS
from core.api_mixin import ShineCandidateDetail
from geolocation.models import Country

from .models import TopTrending, Testimonial

redis_conn = get_redis_connection("search_lookup")


class HomePageView(TemplateView):
    template_name = 'homepage/index.html'

    def get_job_assistance_services(self):
        job_services = []
        job_asst_view_all = None
        try:
            tjob = TopTrending.objects.filter(
                is_active=True, is_jobassistance=True)[0]
            job_services = tjob.get_trending_products()
            # services_class = ProductClass.objects.filter(slug__in=settings.SERVICE_SLUG)
            job_services = job_services.filter(product__type_product__in=[0, 1, 3])
            job_services_pks = list(job_services.all().values_list('product', flat=True))
            job_sqs = SearchQuerySet().filter(id__in=job_services_pks)
            job_services = job_sqs[:5]
            job_asst_view_all = tjob.view_all
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass
        return {"job_asst_services": list(job_services), "job_asst_view_all": job_asst_view_all}

    def get_courses(self):
        tcourses = []
        pcourses = []
        rcourses = []
        t_objects = TopTrending.objects.filter(
            is_active=True, is_jobassistance=False)
        t_objects = t_objects[:4]
        show_pcourses = False
        # recommended
        if self.request.session.get('candidate_id'):
            rcourses = get_recommendations(self.request.session.get('func_area', None),
                                           self.request.session.get('skills', None))
            if rcourses:
                rcourses = rcourses[:9]
            else:
                show_pcourses = True
        else:
            show_pcourses = True
        if show_pcourses:
            pcourses = SQS().only('pTt pURL pHd pAR pNJ pImA pImg pNm').order_by('-pBC')[:9]

        i = 0
        tabs = ['home', 'profile', 'message', 'settings']
        for tcourse in t_objects:
            tprds = tcourse.get_trending_products()
            course_classes = ProductClass.objects.filter(slug__in=settings.COURSE_SLUG)

            tprds = tprds.filter(product__product_class__in=course_classes, product__type_product__in=[0, 1, 3])
            product_pks = list(tprds.all().values_list('product', flat=True))
            tprds = SearchQuerySet().filter(id__in=product_pks)[:9]
            data = {
                'name': tcourse.name,
                'tprds': list(tprds),
                'view_all': tcourse.view_all,
                'tab': tabs[i]
            }
            tcourses.append(data)
            i += 1
        return {'tcourses': tcourses, 'pcourses': pcourses, 'rcourses': rcourses}

    def get_testimonials(self):
        testimonials = Testimonial.objects.filter(page=1, is_active=True)
        testimonials = testimonials[: 5]
        return {"testimonials": testimonials}

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        candidate_id = self.request.session.get('candidate_id')
        if candidate_id:
            candidate_detail = ShineCandidateDetail().get_candidate_public_detail(shine_id=candidate_id)
            if candidate_detail:
                func_area = candidate_detail.get('jobs')[0].get("sub_field", "") \
                    if len(candidate_detail.get('jobs', [])) else ''
                skills = [skill['value'] for skill in candidate_detail['skills']]
                func_area_obj = FunctionalArea.objects.filter(name__iexact=func_area)
                if func_area_obj:
                    self.request.session.update({
                        'func_area': func_area_obj[0].id
                    })
                    context.update({'recmnd_func_area': func_area})
                skills_obj = [s.id for s in Skill.objects.filter(name__in=skills)]
                if skills_obj:
                    self.request.session.update({
                        'skills': skills_obj
                    })
                    context.update({'recmnd_skills': ','.join(skills)})
        func_areas_set = [f.decode() for f in redis_conn.smembers('func_area_set')]
        skills_set = [s.decode() for s in redis_conn.smembers('skills_set')]
        context.update({'func_area_set': func_areas_set, 'skills_set': skills_set})
        context.update({"search_context": redis_conn.smembers('product_set')})
        context.update(self.get_job_assistance_services())
        context.update(self.get_courses())
        context.update(self.get_testimonials())
        return context


class AboutUsView(TemplateView):
    template_name = 'homepage/about-us.html'

    def get_context_data(self, **kwargs):
        context = super(AboutUsView, self).get_context_data(**kwargs)
        return context


class PrivacyPolicyView(TemplateView):
    template_name = 'homepage/privacy-policy.html'

    def get_context_data(self, **kwargs):
        context = super(PrivacyPolicyView, self).get_context_data(**kwargs)
        return context


class TermsConditionsView(TemplateView):
    template_name = 'homepage/tnc.html'

    def get_context_data(self, **kwargs):
        context = super(TermsConditionsView, self).get_context_data(**kwargs)
        return context


class ContactUsView(TemplateView):
    template_name = 'homepage/contact-us.html'

    def get_context_data(self, **kwargs):
        context = super(ContactUsView, self).get_context_data(**kwargs)
        countries = Country.objects.filter(active=True)
        countries = countries.exclude(phone='')
        context.update({
            "countries": countries,
        })
        return context