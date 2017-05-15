from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View, TemplateView
from django.urls import reverse

from shop.models import Category
from cms.mixins import UploadInFile
from review.models import Review
from .mixins import SkillPageMixin

# Create your views here.

class SkillPageView(TemplateView, SkillPageMixin):
    model = Category
    template_name = "skillpage/skill.html"
    page = 1

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        pk = kwargs.get('pk', None)

        try:
            self.category_obj = Category.objects.prefetch_related('categoryproducts').get(
                pk=pk, active=True, is_skill=True, slug=slug)
        except Exception:
            raise Http404

        return super(self.__class__, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        slug = kwargs.get('slug', '')
        page = self.request.GET.get('page', 1)
        api_data = self.get_job_count_and_fuctionan_area(slug)
        career_outcomes = self.category_obj.split_career_outcomes()
        prod_lists = self.category_obj.categoryproducts.all()
        prod_id_list = self.category_obj.categoryproducts.values_list('id', flat=True)
        prod_reviews = Review.objects.filter(id__in=prod_id_list)
        
        prod_page = Paginator(prod_lists, 1)

        try:
            products = prod_page.page(self.page)
        except PageNotAnInteger:
            products = prod_page.page(1)
        except EmptyPage:
            products = prod_page.page(prod_page.num_pages)

        prod_review = Paginator(prod_reviews, 1)

        try:
            page_reviews = prod_review.page(self.page)
        except PageNotAnInteger:
            page_reviews = prod_review.page(1)
        except EmptyPage:
            page_reviews = prod_review.page(prod_review.num_pages)

        context['meta'] = self.category_obj.as_meta(self.request)
        context.update({
            "api_data": api_data,
            "career_outcomes": career_outcomes,
            "prod": prod_lists,
            "page": page,
            "slug": slug,
            "category_obj": self.category_obj,
            "products": products,
            "page_reviews":page_reviews
        })
        context.update(self.get_breadcrumb_data())
        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        breadcrumbs.append({
            "url": reverse('skillpage:skill-page-listing',
            kwargs={'slug': self.category_obj.slug, 'pk':self.category_obj.pk}),
           "name": self.category_obj.get_main_parent()[0].name if self.category_obj.get_main_parent() else None,
        })
        breadcrumbs.append({"url": None, "name": self.category_obj.name})
        data = {"breadcrumbs": breadcrumbs}
        return data


class SkillQueryLead(View, UploadInFile):
    http_method_names = [u'post']

    def post(self, request, *args, **kwargs):
        data_dict = {}
        name = request.POST.get('name', '')
        mobile = request.POST.get('mobile_no', '')
        message = request.POST.get('message', '')

        data_dict = {
            "name": name,
            "mobile": mobile,
            "message": message,
        }
        self.write_in_file(data_dict=data_dict)
        return HttpResponse(status=200)
