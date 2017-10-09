from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View, TemplateView, DetailView
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.http import urlquote
from haystack.query import SearchQuerySet
from django.conf import settings

from geolocation.models import Country
from django.db.models import Q
from shop.models import Category
from cms.mixins import UploadInFile
from review.models import Review
from shop.models import Product
from .mixins import SkillPageMixin

# Create your views here.


class SkillPageView(DetailView, SkillPageMixin):
    model = Category
    template_name = "skillpage/skill.html"
    page = 1

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('skill_slug')
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
        self.pk = self.kwargs.get('pk', None)
        self.object = self.get_object()
        redirect = self.redirect_if_necessary(request.path, self.object)
        if redirect:
            return redirect
        context = super(self.__class__, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)

        slug = self.kwargs.get('skill_slug', '')
        page = self.request.GET.get('page', 1)

        api_data = self.get_job_count_and_fuctionan_area(slug)
        career_outcomes = self.object.split_career_outcomes()
        country_choices = [(m.phone, m.phone) for m in
                           Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
        initial_country = Country.objects.filter(phone='91')[0].phone
        prod_lists = self.object.categoryproducts.all()
        top_3_prod, top_4_vendors = None, None

        try:
            # top_3_prod = self.object.categoryproducts.all().order_by('-productcategories__prd_order')[0:3]
            top_3_prod = SearchQuerySet().filter(pCtg=self.pk)[0:3]
            top_4_vendors = SearchQuerySet().filter(pCtg=self.pk)[0:4]
        except:
            pass
        prd_obj = ContentType.objects.get_for_model(Product)
        all_results = SearchQuerySet().filter(pCtg=self.pk)
        prod_id_list = self.object.get_products().values_list('id', flat=True)
        prod_reviews = Review.objects.filter(
            object_id__in=prod_id_list, content_type=prd_obj)

        try:
            # prod_lists[0]
            all_results[0]
        except Exception:
            raise Http404

        # prod_page = Paginator(prod_lists, 1)
        prod_page = Paginator(all_results, 1)

        try:
            products = prod_page.page(self.page)
        except PageNotAnInteger:
            products = prod_page.page(1)
        except EmptyPage:
            products = prod_page.page(prod_page.num_pages)

        for product in products:
            if float(product.pPfin):
                product.discount = round((float(product.pPfin) - float(product.pPin)) * 100 / float(product.pPfin), 2)

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
            'site': settings.SITE_PROTOCOL + "://" + settings.SITE_DOMAIN,
            "page_reviews": prod_reviews[0:4] if self.request.flavour else page_reviews,
            'url': settings.SITE_PROTOCOL + "://" + self.object.video_link,
            'country_choices': country_choices,
            'initial_country': initial_country,
        })
        context.update(self.get_breadcrumb_data())
        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        parent = self.object.get_parent() 
        if parent:
            breadcrumbs.append({
                "url": parent[0].get_absolute_url(), "name": parent[0].name,
            })
        breadcrumbs.append({"url": '', "name": self.object.name})
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
