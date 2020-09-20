import logging

from django.views.generic import TemplateView
from django.conf import settings
from django.core.cache import cache
from django.http.response import Http404
from django.db.models import Prefetch

from django_redis import get_redis_connection
from haystack.query import SearchQuerySet


from shop.models import ProductClass, FunctionalArea, Skill
from search.helpers import get_recommendations, get_recommended_products
from core.library.haystack.query import SQS
from core.api_mixin import ShineCandidateDetail

from geolocation.models import Country
from meta.views import MetadataMixin
from .models import TopTrending, Testimonial, TrendingProduct

from .config import STATIC_SITE_SLUG_TO_ID_MAPPING, STATIC_PAGE_NAME_CHOICES, TOPTRENDING_FA_MAPPING

redis_conn = get_redis_connection("search_lookup")


class HomePageView(TemplateView, MetadataMixin):
    template_name = 'homepage/index.html'
    use_title_tag = False
    use_og = True
    use_twitter = False

    def remove_tracking(self):
        if self.request.session('tracking_id',''):
            del self.request.session['tracking_id']
        if self.request.session('product_tracking_mapping_id',''):
            del self.request.session['product_tracking_mapping_id']
        if self.request.session('tracking_product_id',''):
            del self.request.session['tracking_product_id']
        if self.request.session('product_availability',''):
            del self.request.session['product_availability']

    def get_params(self):
        from payment.tasks import make_logging_request, make_logging_sk_request
        tracking_id = self.request.GET.get('t_id', '')
        product_tracking_mapping_id = self.request.GET.get('product', '')
        utm_campaign = self.request.GET.get('utm_campaign', '')
        trigger_point = self.request.GET.get('trigger_point', '')
        u_id = self.request.GET.get('u_id',self.request.session.get('u_id',''))
        position = self.request.GET.get('position', -1)

        if tracking_id and self.request.session.get('candidate_id'):
            self.request.session.update({
                'tracking_id': tracking_id,
                'product_tracking_mapping_id': product_tracking_mapping_id,
                'tracking_product_id':'',
                'trigger_point': trigger_point,
                'utm_campaign' : utm_campaign,
                'u_id':u_id,
                'postion' : position
            })

            if product_tracking_mapping_id :
                make_logging_request.delay(
                '', product_tracking_mapping_id, tracking_id, 'home_page',position, trigger_point, u_id, utm_campaign, 2)
        elif self.request.session.get('tracking_id', '') and self.request.session.get('candidate_id'):
            product_tracking_mapping_id = self.request.session.get(
                'product_tracking_mapping_id', '')
            tracking_product_id = self.request.session.get(
                'tracking_product_id', '')
            tracking_id = self.request.session.get(
                'tracking_id', '')
            trigger_point = self.request.session.get(
            'trigger_point','')
            u_id = self.request.session.get(
            'u_id','')
            position = self.request.session.get(
            'position',1)
            utm_campaign = self.request.session.get(
            'utm_campaign','')
            referal_product = self.request.session.get('referal_product','')
            referal_subproduct = self.request.session.get('referal_subproduct','')
            if product_tracking_mapping_id == 10:
                #remove cart
                self.remove_tracking()
                return

            if product_tracking_mapping_id:
                make_logging_sk_request.delay(
                    tracking_product_id, product_tracking_mapping_id, tracking_id, 'home_page', position, trigger_point, u_id, utm_campaign, 2, referal_product, referal_subproduct)

    def get_meta_title(self, context):
        # return 'Best Resume Writing Services | Online Courses | Linkedin Profile - Shine Learning'
        # return 'Online Courses, Practice Tests, Job Assistance Services | Shine Learning'
        return 'Best Online Courses  & Certification Trainings | Shine Learning'

    def get_meta_description(self, context):
        # return 'Pick up the Best Resume Services - Check out the Latest Resume Format or Templates - Online Professional Certification Courses'
        # return 'Discover a variety of online courses and certification training, practice tests, job assistance services with 24X7 support.'
        return 'Discover a comprehensive variety of online courses, certification training programs, practice tests with 24X7 support to build a successful career or grow your business.'

    def get_meta_url(self, context):
        return 'https://learning.shine.com'

    def get_job_assistance_services(self):
        job_services = []
        job_asst_view_all = None

        try:

            tjob = TopTrending.objects.filter(
                is_active=True, is_jobassistance=True).first()
            # job_services = tjob.get_trending_products()
            # services_class = ProductClass.objects.filter(slug__in=settings.SERVICE_SLUG)
            # job_services = job_services.filter(product__type_product__in=[0, 1, 3])
            # job_services_pks = list(job_services.all().values_list('product', flat=True))
            job_services_pks = list(
                tjob.get_all_active_trending_products_ids())

            job_sqs = SearchQuerySet().filter(id__in=job_services_pks, pTP__in=[0, 1, 3]).exclude(
                id__in=settings.EXCLUDE_SEARCH_PRODUCTS)
            job_services = job_sqs[:5]
            job_asst_view_all = tjob.view_all
        except Exception as e:
            logging.getLogger('error_log').error(
                "unable to load job assistance services%s " % str(e))
        return {"job_asst_services": list(job_services), "job_asst_view_all": job_asst_view_all}

    def get_courses(self):
        tcourses = []
        pcourses = []
        rcourses = []
        t_objects = TopTrending.objects.filter(
            is_active=True, is_jobassistance=False).prefetch_related(Prefetch('trendingproduct_set',
                                                                              queryset=TrendingProduct.objects.select_related('trendingcourse').filter(
                                                                                  is_active=True), to_attr='get_pids'))

        t_objects = t_objects[:4]
        show_pcourses = False

        # recommended
        if self.request.session.get('candidate_id'):
            # rcourses = get_recommendations(self.request.session.get('func_area', None),
            #                                self.request.session.get('skills', None))

            rcourses = get_recommended_products(self.request.session.get(
                'job_title', None), self.request.session.get('all_skill_ids',
                                                             []), self.request.session.get('func_area', None))

            if rcourses:
                rcourses = rcourses[:9]
            else:
                show_pcourses = True
        else:
            show_pcourses = True
        if show_pcourses:
            # pcourses = SQS().filter(
            #     pPc='course').exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).only(
            #     'pTt pURL pHd pAR pNJ pImA pImg pNm pBC pRC').order_by(
            #     '-pBC')[:9]
            # will show the default products if it is not logged in
            pcourses = get_recommended_products()

        i = 0
        tabs = ['home', 'profile', 'message', 'settings']
        # course_classes = ProductClass.objects.filter(slug__in=settings.COURSE_SLUG)
        for tcourse in t_objects:
            # tprds = tcourse.get_trending_products()
            # tprds = tprds.filter(product__product_class__in=course_classes,
            # product__type_product__in=[0, 1, 3])
            # product_pks = list(tprds.all().values_list('product', flat=True))
            product_pks = [prod.product_id for prod in tcourse.get_pids]
            # product_pks = list(tcourse.get_all_active_trending_products_ids())

            tprds = SearchQuerySet().filter(id__in=product_pks, pPc__in=settings.COURSE_SLUG, pTP__in=[0, 1, 3]).exclude(
                id__in=settings.EXCLUDE_SEARCH_PRODUCTS)[:9]

            data = {
                'name': tcourse.name,
                'tprds': list(tprds),
                'view_all': tcourse.view_all,
                'tab': tabs[i]
            }
            tcourses.append(data)
            i += 1
        if not self.request.session.get('candidate_id'):
            pcourses = [pcourses[count:count + 3]
                        for count in range(0, len(pcourses), 3)]
        rcourses = [rcourses[count:count + 3]
                    for count in range(0, len(rcourses), 3)]

        return {'tcourses': tcourses, 'pcourses': pcourses, 'rcourses': rcourses}

    def get_testimonials(self):
        data = cache.get('get_testimonial')
        if data:
            return data
        else:
            data = Testimonial.objects.filter(page=1, is_active=True)
            data = data[: 5]
            data = {"testimonials": data}
            cache.set('get_testimonial', data, timeout=None)
        return data

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        candidate_id = self.request.session.get('candidate_id')
        candidate_detail = None

        session_fa = self.request.session.get('func_area')
        session_skills = self.request.session.get('mid_skills')

        message = self.request.GET.get('message', '')

        if message:
            context.update({'email_response': message})

        if session_fa:
            fa = FunctionalArea.objects.filter(
                id=session_fa).first()
            if fa:
                context.update({'recmnd_func_area': fa.name})
                top_trend = fa.toptrending_set.filter(is_active=True,
                                                      is_jobassistance=False).order_by('-priority').first()
                context['preSelect'] = top_trend.name if top_trend else ""

        if session_skills:
            skills_found = Skill.objects.filter(
                pk__in=session_skills).values_list('name', flat=True)
            context.update({'recmnd_skills': ','.join(skills_found)})

        # if not session_fa:
        #     # Fetch from shine
        #     if candidate_id:
        #         candidate_detail = ShineCandidateDetail().get_candidate_public_detail(shine_id=candidate_id)
        #         if candidate_detail:
        #             func_area = candidate_detail.get('jobs')[0].get("parent_sub_field", "") \
        #                 if len(candidate_detail.get('jobs', [])) else ''
        #             func_area_obj = FunctionalArea.objects.filter(name__iexact=func_area)
        #             if func_area_obj:
        #                 self.request.session.update({
        #                     'func_area': func_area_obj[0].id
        #                 })
        #                 context.update({'recmnd_func_area': func_area})
        # else:
        #     # Pre-populate session FA
        #     try:
        #         context.update({'recmnd_func_area': FunctionalArea.objects.get(id=session_fa).name})
        #     except FunctionalArea.DoesNotExist:
        #         logging.getLogger('error_log').error("FA not in DB - from session %s " % str(session_fa))
        # if not session_skills:
        #     if not candidate_detail and candidate_id:
        #         candidate_detail = ShineCandidateDetail().get_candidate_public_detail(shine_id=candidate_id)
        #     if candidate_detail:
        #         skills = [skill['value'] for skill in candidate_detail['skills']]
        #         skills_obj = Skill.objects.filter(name__in=skills)[:2]
        #         skills_ids = [s.id for s in skills_obj][:2]
        #         if skills_obj:
        #             self.request.session.update({
        #                 'skills': skills_ids
        #             })
        #             context.update({'recmnd_skills': ','.join([skill.name for skill in skills_obj])})
        # else:
        #     skills_found = Skill.objects.filter(pk__in=session_skills).values_list('name', flat=True)
        #     context.update({'recmnd_skills': ','.join(skills_found)})

        func_areas_set = [f.decode()
                          for f in redis_conn.smembers('func_area_set')]
        skills_set = [s.decode() for s in redis_conn.smembers('skills_set')]
        context.update({'func_area_set': func_areas_set,
                        'skills_set': skills_set})
        context.update(self.get_job_assistance_services())
        context.update(self.get_courses())
        context.update(self.get_testimonials())
        self.get_params()
        context['meta'] = self.get_meta()
        context['remove_nav_search'] = True
        context['offer_home'] = True
        context.update({
            'shine_api_url': settings.SHINE_API_URL,
            'tracking_product_id': self.request.session.get('tracking_product_id', ''),
            'product_tracking_mapping_id': self.request.session.get('product_tracking_mapping_id', ''),
            'tracking_id': self.request.session.get('tracking_id', ''),
            'trigger_point':self.request.session.get('trigger_point',''),
            'u_id':self.request.session.get('u_id',''),
            'position':self.request.session.get('position',1),
            'utm_campaign':self.request.session.get('utm_campaign',''),
        })

        linkedin_modal = self.request.session.get('linkedin_modal', 0)
        if linkedin_modal:
            del self.request.session['linkedin_modal']
        context.update({'linkedin_modal': linkedin_modal})
        return context


class AboutUsView(TemplateView):
    template_name = 'homepage/about-us.html'

    def get_context_data(self, **kwargs):
        context = super(AboutUsView, self).get_context_data(**kwargs)
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


class StaticSiteContentView(TemplateView):
    template_name = 'homepage/static-site-content.html'

    def get_context_data(self, **kwargs):
        page_slug = kwargs.get('page_slug', '')
        if not page_slug:
            raise Http404

        page_type = str(STATIC_SITE_SLUG_TO_ID_MAPPING.get(page_slug, ''))
        if not page_type or not page_type.isdigit():
            raise Http404

        page_type = int(page_type)
        context = super(StaticSiteContentView, self).get_context_data(**kwargs)
        context.update({
            "page_type": page_type,
            "page_name": STATIC_PAGE_NAME_CHOICES[page_type-1][1]
        })
        return context
