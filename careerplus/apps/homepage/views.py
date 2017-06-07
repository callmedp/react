from django.views.generic import TemplateView

from shop.models import Product
from review.models import Review


class HomePageView(TemplateView):
	template_name = 'homepage/index.html'

	def get_job_assistance_services(self):
		job_services = Product.objects.filter(
			type_service=2, type_product__in=[0, 1, 3], active=True)
		job_services = job_services[: 5]
		return {"job_asst_services": job_services}

	def get_courses(self):
		pass

	def get_recommend_courses(self):
		pass

	def get_testimonials(self):
		testimonials = Review.objects.filter(is_testimonial=True)[: 10]
		return {"testimonials": testimonials}

	def get(self, request, *args, **kwargs):
		return super(self.__class__, self).get(request, args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(self.__class__, self).get_context_data(**kwargs)
		context.update(self.get_job_assistance_services())
		context.update(self.get_testimonials())
		return context