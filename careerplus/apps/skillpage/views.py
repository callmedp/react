from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View, TemplateView, DetailView
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.http import urlquote

from shop.models import Category
from cms.mixins import UploadInFile
from review.models import Review
from partner.models import Vendor
from shop.models import Product
from .mixins import SkillPageMixin

# Create your views here.

class SkillPageView(DetailView, SkillPageMixin):
    model = Category
    template_name = "skillpage/skill.html"
    page = 1

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('slug')
        if queryset is None:
            queryset = self.get_queryset()

        if pk is not None:
            queryset = queryset.prefetch_related('categoryproducts').filter(pk=pk, active=True, is_skill=True)
        elif slug is not None:
            queryset = queryset.prefetch_related('categoryproducts').filter(slug=slug, active=True, is_skill=True)
        try:
            obj = queryset.get()
        except:
            raise Http404
        return obj

    def redirect_if_necessary(self, current_path, skill):
        expected_path = skill.get_absolute_url()
        if expected_path != urlquote(current_path):
            return HttpResponsePermanentRedirect(expected_path)
        return None

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', None)
        pk = self.kwargs.get('pk', None)
        self.object = self.get_object()
        redirect = self.redirect_if_necessary(request.path, self.object)

        # try:
        #     self.category_obj = Category.objects.prefetch_related('categoryproducts').get(
        #         pk=pk, active=True, is_skill=True, slug=slug)
        # except Exception:
        #     raise Http404
        if redirect:
            return redirect
        context = super(self.__class__, self).get(request, args, **kwargs)
        return context
        
    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)

        slug = self.kwargs.get('slug', '')
        page = self.request.GET.get('page', 1)

        api_data = self.get_job_count_and_fuctionan_area(slug)
        career_outcomes = self.object.split_career_outcomes()
        prod_lists = self.object.categoryproducts.all()
        top_3_prod, top_4_vendors = None, None

        try:    
            top_3_prod = self.object.categoryproducts.all().order_by('-productcategories__prd_order')[0:3]
            top_4_vendors = Vendor.objects.all()[0:4]
        except:
            pass
        
        prd_obj = ContentType.objects.get_for_model(Product)
        prod_id_list = self.object.categoryproducts.values_list('id', flat=True)
        prod_reviews = Review.objects.filter(
            object_id__in=prod_id_list, content_type=prd_obj)

        try:
            prod_lists[0]
        except Exception:
            raise Http404

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
        context['meta'] = self.object.as_meta(self.request)
        context.update({
            "api_data": api_data,
            "career_outcomes": career_outcomes,
            "prod": prod_lists,
            "page": page,
            "slug": slug,
            "category_obj": self.object,
            "top_3_prod": top_3_prod,
            "top_4_vendors": top_4_vendors,
            "products": products,
            "page_reviews":prod_reviews[0:4] if self.request.flavour else page_reviews,
            'url': 'https://' + self.object.video_link
        })
        context.update(self.get_breadcrumb_data())
        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        if self.object.get_parent():
            breadcrumbs.append({
                "url": reverse('skillpage:skill-page-listing',
                kwargs={'slug': self.object.slug, 'pk':self.object.pk}),
               "name": self.object.get_parent()[0].name,
            })
        breadcrumbs.append({"url": None, "name": self.object.name})
        data = {"breadcrumbs": breadcrumbs}
        return data


class SkillQueryLead(View, UploadInFile):
    http_method_names = [u'post']

    def post(self, request, *args, **kwargs):
        data_dict = {}
        name = request.POST.get('name', '')
        mobile = request.POST.get('mobile_number', '')
        message = request.POST.get('message_box', '')

        data_dict = {
            "name": name,
            "mobile": mobile,
            "message": message,
        }
        self.write_in_file(data_dict=data_dict)
        return HttpResponse(status=200)
