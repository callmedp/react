from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View, TemplateView
from shop.models import Category
from cms.mixins import UploadInFile
from .mixins import SkillPageMixin

# Create your views here.

class SkillPageView(TemplateView, SkillPageMixin):
    model = Category
    template_name = "skillpage/skill.html"
    page = 1

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        try:
            self.category_obj = Category.objects.prefetch_related('categoryproducts').get(
                slug=slug, active=True)
        except Exception:
            raise Http404
        return super(self.__class__, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['category_obj'] = self.category_obj
        slug = kwargs.get('slug', '')
        page = self.request.GET.get('page', 1)
        context['api_data'] = self.get_job_count_and_fuctionan_area(slug)
        context['career_outcomes'] = self.category_obj.split_career_outcomes()
        prod_lists = self.category_obj.categoryproducts.all()
        context['prod'] = prod_lists
        context['page'] = page
        context['slug'] = slug 

        paginator = Paginator(prod_lists, 2)
        try:
            products = paginator.page(self.page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context['products'] = products

        return context


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
