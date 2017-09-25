from django.views.generic import TemplateView
from django.conf import settings

from shop.models import Product, ProductClass, FunctionalArea, Skill
from search.helpers import get_recommendations
from core.library.haystack.query import SQS
from core.api_mixin import ShineCandidateDetail

from .models import TopTrending, Testimonial


class HomePageView(TemplateView):
    template_name = 'homepage/index.html'

    def get_job_assistance_services(self):
        job_services = []
        job_asst_view_all = None
        try:
            tjob = TopTrending.objects.filter(
                is_active=True, is_jobassistance=True)[0]
            job_services = tjob.get_trending_products()
            services_class = ProductClass.objects.filter(slug__in=settings.SERVICE_SLUG)
            job_services = job_services.filter(product__product_class__in=services_class, product__type_product__in=[0, 1, 3])
            job_services = job_services[: 5]
            job_asst_view_all = tjob.view_all
        except:
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
                                           self.request.session.get('skills', None),
                                           SQS().only('pTt pURL pHd pAR pNJ pImA pImg'))
            if rcourses:
                rcourses = rcourses[:9]
            else:
                show_pcourses = True
        else:
            show_pcourses = True
        if show_pcourses:
            pcourses = SQS().only('pTt pURL pHd pAR pNJ pImA pImg').order_by('-pBC')[:9]

        i = 0
        tabs = ['home', 'profile', 'message', 'settings']
        for tcourse in t_objects:
            tprds = tcourse.get_trending_products()
            course_classes = ProductClass.objects.filter(slug__in=settings.COURSE_SLUG)
            tprds = tprds.filter(product__product_class__in=course_classes)[:9]
            data = {
                'name': tcourse.name,
                'tprds': list(tprds),
                'view_all': tcourse.view_all,
                'tab': tabs[i]
            }
            tcourses.append(data)
            i += 1

        return {'tcourses': tcourses, 'pcourses': pcourses, 'rcourses': rcourses}

    def get_recommend_courses(self):
        course_classes = ProductClass.objects.filter(slug__in=settings.COURSE_SLUG)
        recommended_courses = Product.objects.filter(
            product_class__in=course_classes, type_product__in=[0, 1, 3],
            active=True)[: 6]
        return {"recommended_courses": recommended_courses, }

    def get_testimonials(self):
        testimonials = Testimonial.objects.filter(page=1, is_active=True)
        testimonials = testimonials[: 5]
        return {"testimonials": testimonials}

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        candidate_id = self.request.session.get('candidate_id')
        if candidate_id:
            candidate_detail = ShineCandidateDetail().get_candidate_detail(shine_id=candidate_id)
            if candidate_detail:
                func_area = candidate_detail.get('functional_area')[0] if len(candidate_detail.get('functional_area', [])) else 'Real Estate'
                skills = [skill['value'] for skill in candidate_detail['skills']]
                context.update({'recmd_func_area': func_area, 'recmd_skills': skills})
                func_area = FunctionalArea.objects.filter(name__iexact=func_area)
                if func_area:
                    self.request.session.update({
                        'func_area': func_area[0].id
                    })
                skills = [s.id for s in Skill.objects.filter(name__iregex=r'(' + '|'.join(skills) + ')')]
                if skills:
                    self.request.session.update({
                        'skills': skills
                    })
        context.update(self.get_job_assistance_services())
        context.update(self.get_courses())
        if self.request.session.get('candidate_id'):
            context.update(self.get_recommend_courses())
        context.update(self.get_testimonials())
        return context
