from django.views.generic import TemplateView

from shop.models import Product

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
			job_services = job_services.filter(product__type_service=2)
			job_services = job_services[: 5]
			job_asst_view_all = tjob.view_all
		except:
			pass
		return {"job_asst_services": list(job_services), "job_asst_view_all": job_asst_view_all}

	def get_courses(self):
		tcourses = []
		try:
			courses = TopTrending.objects.filter(
				is_active=True, is_jobassistance=False)
			courses = courses[: 4]
			i = 0
			tabs = ['home', 'profile', 'message', 'settings']
			for course in courses:
				tprds = course.get_trending_products()
				tprds = tprds.filter(product__type_service=3)[: 9]
				data = {
					'name': course.name,
					'tprds': list(tprds),
					'view_all': course.view_all,
					'tab': tabs[i]
				}
				tcourses.append(data)
				i += 1
		except:
			pass
		return {'tcourses': tcourses}

	def get_recommend_courses(self):
		recommended_courses = Product.objects.filter(
			type_service=3, type_product__in=[0, 1, 3],
			active=True)[: 6]
		return {"recommended_courses": recommended_courses, }

	def get_testimonials(self):
		testimonials = Testimonial.objects.filter(page=1, is_active=True)
		testimonials = testimonials[: 5]
		return {"testimonials": testimonials}

	def get(self, request, *args, **kwargs):
		return super(self.__class__, self).get(request, args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(self.__class__, self).get_context_data(**kwargs)
		context.update(self.get_job_assistance_services())
		context.update(self.get_courses())
		if self.request.session.get('candidate_id'):
			context.update(self.get_recommend_courses())
		context.update(self.get_testimonials())
		return context