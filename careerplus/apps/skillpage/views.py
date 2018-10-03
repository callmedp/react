import json
import logging
from django.http import (
    Http404, HttpResponse,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect
)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View, DetailView
from django.contrib.contenttypes.models import ContentType
from django.utils.http import urlquote
from core.library.haystack.query import SQS
from django.conf import settings
from django.core.cache import cache

from geolocation.models import Country
from django.db.models import Q
from shop.models import (
    Category, Faculty, Product)
from cms.mixins import UploadInFile
from partner.models import Vendor
from review.models import Review
from .mixins import SkillPageMixin
from review.models import DetailPageWidget

# Create your views here.


class SkillPageView(DetailView, SkillPageMixin):
    model = Category
    # template_name = "skillpage/skill.html"
    page = 1

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('skill_slug')
        if queryset is None:
            queryset = self.get_queryset()

        if pk is not None:
            queryset = queryset.prefetch_related('categoryproducts').filter(pk=pk, active=True, is_skill=True, type_level__in=[3,4])
        elif slug is not None:
            queryset = queryset.prefetch_related('categoryproducts').filter(slug=slug, active=True, is_skill=True, type_level__in=[3,4])

        if queryset:
            return queryset[0]
        else:
            raise Http404

    def get_template_names(self):
        if self.request.amp:
            from newrelic import agent
            agent.disable_browser_autorum()
            return ["skillpage/skill-amp.html"]
        return ["skillpage/skill.html"]
        
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
        context = super(SkillPageView, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(SkillPageView, self).get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        api_data = self.get_job_count_and_fuctionan_area(self.object.name)
        career_outcomes = self.object.split_career_outcomes()
        country_choices = [(m.phone, m.name) for m in
                           Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
        initial_country = Country.objects.filter(phone='91')[0].phone
        top_3_prod, top_4_vendors = None, None
        prd_list = []
        prd_text = None
        meta_desc = None
        prod_id_list = []
        try:
            products = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).filter(pCtg=self.pk)
            for prd in products:
                if prd.pTP == 1:
                    prd_vars = json.loads(prd.pVrs)
                    var_lists = prd_vars.get('var_list')
                    for var_lst in var_lists:
                        prod_id_list.append(var_lst.get('id'))
                    prod_id_list.append(prd.id)
                if prd.pTP == 3:
                    prd_cmbs = json.loads(prd.pCmbs)
                    combo_lists = prd_cmbs.get('combo_list')
                    for combo_lst in combo_lists:
                        prod_id_list.append(combo_lst.get('pk'))
                    prod_id_list.append(prd.id)
                if prd.pTP in [0, 2, 4, 5]:
                    prod_id_list.append(prd.id)

            # prod_id_list = [pv.id for pv in products]
            vendor_list = [pv.pPv for pv in products]
            vendor_list = list(set(vendor_list))

            if not len(prod_id_list):
                raise Http404
            top_3_prod = products[:3]
            for tp_prod in top_3_prod:
                prd_list.append(tp_prod.pNm)
            top_4_vendors = Vendor.objects.filter(id__in=vendor_list)[:4] if len(vendor_list) >= 4 else Vendor.objects.filter(id__in=vendor_list)
        except Exception as e:
            logging.getLogger('error_log').error(" MSG:unable to load the list   %s" %str(e))

        prd_obj = ContentType.objects.get_for_model(Product)
        all_results = products
        prod_reviews = Review.objects.filter(
            object_id__in=prod_id_list,
            content_type=prd_obj,
            status=1)

        prod_page = Paginator(all_results, 5)

        try:
            products = prod_page.page(self.page)
        except PageNotAnInteger:
            products = prod_page.page(1)
        except EmptyPage:
            products = prod_page.page(prod_page.num_pages)
        for product in products:
            if float(product.pPfin):
                product.discount = round((float(product.pPfin) - float(product.pPin)) * 100 / float(product.pPfin), 2)

        prod_review = Paginator(prod_reviews, 5)

        try:
            page_reviews = prod_review.page(self.page)
        except PageNotAnInteger:
            page_reviews = prod_review.page(1)
        except EmptyPage:
            page_reviews = prod_review.page(prod_review.num_pages)

        if prd_list:
            prd_text = ' , '.join(prd_list)
        if self.object.name and prd_text:
            meta_desc = "Get online certification in {}. Check discounted price and offers on short term professional courses like {} and more".format(self.object.name, prd_text)
        context['meta'] = self.object.as_meta(self.request)
        context['canonical_url'] = self.object.get_canonical_url()
        context['meta']._url = context.get('canonical_url', '')
        meta_dict = context['meta'].__dict__
        meta_dict['description'] = meta_desc
        meta_dict['og_description'] = meta_desc
        if products.paginator.count:
            meta_title = '{} Courses ({} Certification Programs) - Shine Learning'.format(
                self.object.name, products.paginator.count)
        else:
            meta_title = '{} Courses - Shine Learning'.format(
                self.object.name)
        meta_dict['title'] = meta_title
        context.update({
            "api_data": api_data,
            "career_outcomes": career_outcomes,
            "page": page,
            "slug": self.object.name,
            "category_obj": self.object,
            "top_3_prod": top_3_prod,
            "top_4_vendors": top_4_vendors,
            "products": products,
            'site': settings.SITE_PROTOCOL + "://" + settings.SITE_DOMAIN,
            "page_reviews": prod_reviews[0:4] if self.request.flavour else page_reviews,
            'url': settings.SITE_PROTOCOL + "://" + self.object.video_link,
            'country_choices': country_choices,
            'initial_country': initial_country,
            'show_chat': True,
            'amp': self.request.amp
        })
        try:
            widget_obj = DetailPageWidget.objects.get(
                content_type__model='Category', listid__contains=self.pk)
            widget_objs = widget_obj.widget.iw.indexcolumn_set.filter(
                column=1)
        except DetailPageWidget.DoesNotExist:
            widget_objs = None
            widget_obj = None
        context['widget_objs'] = widget_objs
        context['widget_obj'] = widget_obj
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


class ServiceDetailPage(DetailView):
    model = Category
    template_name = "services/detail.html"
    slug_field = 'slug'
    slug_url_kwarg = 'category_slug'
    pk_url_kwarg = 'category_id'
    context_object_name = "category_obj"
    query_pk_and_slug = True

    PRODUCT_PAGE_SIZE = 5
    REVIEW_PAGE_SIZE = 5

    def get_queryset(self):
        return Category.objects.filter(is_service=True)

    def get_object(self, queryset=None):
        cat_slug = self.request.path.split("/")[-3]
        cat_id = self.request.path.split("/")[-2]

        if not cat_id.isdigit() or not settings.SERVICE_PAGE_ID_SLUG_MAPPING.get(cat_id):
            raise Http404()

        if queryset is None:
            queryset = self.get_queryset()

        return queryset.get(id=int(cat_id),slug=cat_slug)

    def _get_country_choices(self):
        cached_country_choices = cache.get('callback_country_choices')
        if cached_country_choices:
            return cached_country_choices

        country_choices = [(m.phone, m.name) for m in
                           Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]

        cache.set('callback_country_choices',country_choices,86400)
        return country_choices

    def _get_preselected_country(self):
        cached_initial_country = cache.get('callback_initial_country')
        if cached_initial_country:
            return cached_initial_country

        initial_country = Country.objects.filter(phone='91')[0].phone
        cache.set("callback_initial_country",initial_country,86400)
        return initial_country

    def _get_all_products_of_category(self):
        """
        Fetch all products with category same as that of object.
        """
        products = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).\
                filter(pCtg=self.object.pk)
        return products

    def _get_product_variation_combo_ids(self, products):
        """
        Fetch ids of all products which are variations/combos for the given category.
        """
        prod_id_list = []
        
        for prd in products:
            if prd.pTP == 1:
                prd_vars = json.loads(prd.pVrs)
                [prod_id_list.append(var_lst.get('id')) for var_lst in prd_vars.get('var_list') ]
                    
            if prd.pTP == 3:
                prd_cmbs = json.loads(prd.pCmbs)
                [prod_id_list.append(combo_lst.get('pk')) for combo_lst in prd_cmbs.get('combo_list') ]
            
            if prd.pTP in [0, 1, 2, 3, 4, 5]:
                prod_id_list.append(prd.id)

        return prod_id_list

    def _get_paginated_products(self, products, page=1):
        """
        Return the first 5 results of products list.
        In compliance with Ajax views for Product Load More.
        """
        prod_page = Paginator(products, self.PRODUCT_PAGE_SIZE)

        products = prod_page.page(page)
        for product in products:
            if not float(product.pPfin): continue
            product.discount = round((float(product.pPfin) - float(product.pPin)) * 100 / float(product.pPfin), 2)

        return products
        
    def _get_paginated_reviews(self, prod_id_list, page=1):
        """
        Return the first 5 results of reviews list.
        In compliance with Ajax views for Review Load More.
        """
        content_obj = ContentType.objects.get_for_model(Product)
        prod_reviews = Review.objects.filter(object_id__in=prod_id_list,\
                content_type=content_obj,status=1)

        review_page = Paginator(prod_reviews, self.REVIEW_PAGE_SIZE)
        reviews = review_page.page(page)
        return reviews

    def _get_page_meta_data(self):
        meta_dict = self.object.as_meta(self.request).__dict__
        meta_dict['description'] = self.object.get_description()
        meta_dict['og_description'] = self.object.get_description()
        meta_dict["_url"] = self.object.get_canonical_url()
        meta_dict['title'] = self.object.title if self.object.title else \
                '{} Services - Shine Learning'.format(self.object.name) 
        meta_dict['heading'] = self.object.heading
        return meta_dict

    def get_context_data(self,**kwargs):
        context = super(ServiceDetailPage,self).get_context_data(**kwargs)
        standalone_products = self._get_all_products_of_category()
        all_product_ids = self._get_product_variation_combo_ids(standalone_products)
        context['products'] = self._get_paginated_products(standalone_products)
        context['reviews'] = self._get_paginated_reviews(all_product_ids)
        context.update({"meta": self._get_page_meta_data()})
        context.update({"canonical_url": self.object.get_canonical_url()})
        context.update({"country_choices": self._get_country_choices()})
        context.update({"initial_country": self._get_preselected_country()})
        return context


class UniversityPageView(DetailView):
    model = Category
    template_name = "university/university.html"
    context_object_name = "category_obj"

    PRODUCT_PAGE_SIZE = 5
    REVIEW_PAGE_SIZE = 5

    def get_queryset(self):
        return Category.objects.filter(
            is_university=True, active=True)

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('university_slug')
        if queryset is None:
            queryset = self.get_queryset()

        if pk is not None:
            queryset = queryset.filter(
                pk=pk, active=True, is_university=True,
                type_level__in=[3, 4])
        elif slug is not None:
            queryset = queryset.filter(
                slug=slug, active=True, is_university=True,
                type_level__in=[3, 4])

        if queryset.exists():
            return queryset.first()
        else:
            raise Http404

    def _get_country_choices(self):
        cached_country_choices = cache.get('callback_country_choices')
        if cached_country_choices:
            return cached_country_choices

        country_choices = [(m.phone, m.name) for m in
                           Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]

        cache.set('callback_country_choices', country_choices, 86400)
        return country_choices

    def _get_preselected_country(self):
        cached_initial_country = cache.get('callback_initial_country')
        if cached_initial_country:
            return cached_initial_country

        initial_country = Country.objects.filter(
            phone='91')[0].phone
        cache.set(
            "callback_initial_country", initial_country, 86400)
        return initial_country

    def _get_all_products_of_category(self):
        """
        Fetch all products with category same as that of object.
        """
        products = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).\
                filter(pCtg=self.object.pk)
        return products

    def _get_product_variation_combo_ids(self, products):
        """
        Fetch ids of all products which are variations/combos for the given category.
        """
        prod_id_list = []

        for prd in products:
            if prd.pTP == 1:
                prd_vars = json.loads(prd.pVrs)
                [prod_id_list.append(var_lst.get('id')) for var_lst in prd_vars.get('var_list') ]

            if prd.pTP == 3:
                prd_cmbs = json.loads(prd.pCmbs)
                [prod_id_list.append(combo_lst.get('pk')) for combo_lst in prd_cmbs.get('combo_list') ]

            if prd.pTP in [0, 1, 2, 3, 4, 5]:
                prod_id_list.append(prd.id)

        return prod_id_list

    def _get_paginated_products(self, products, page=1):
        """
        Return the first 5 results of products list.
        In compliance with Ajax views for Product Load More.
        """
        prod_page = Paginator(products, self.PRODUCT_PAGE_SIZE)

        products = prod_page.page(page)
        for product in products:
            if not float(product.pPfin): continue
            product.discount = round((float(product.pPfin) - float(product.pPin)) * 100 / float(product.pPfin), 2)

        return products
        
    def _get_paginated_reviews(self, prod_id_list, page=1):
        """
        Return the first 5 results of reviews list.
        In compliance with Ajax views for Review Load More.
        """
        content_obj = ContentType.objects.get_for_model(Product)
        prod_reviews = Review.objects.filter(
            object_id__in=prod_id_list,
            content_type=content_obj, status=1)

        review_page = Paginator(prod_reviews, self.REVIEW_PAGE_SIZE)
        reviews = review_page.page(page)
        return reviews

    def _get_subheaders_category(self):
        subheaders = self.object.subheaders.filter(
            active=True).order_by('display_order')
        return subheaders

    def _get_university_faculty(self):
        faculty = self.object.faculty_set.filter(
            active=True)
        return faculty

    def _get_testimonials_category(self):
        testimonials = self.object.testimonials(
            is_active=True).order_by('priority')
        return testimonials

    def _get_page_meta_data(self):
        meta_dict = self.object.as_meta(self.request).__dict__
        meta_dict['description'] = self.object.get_description()
        meta_dict['og_description'] = self.object.get_description()
        meta_dict["_url"] = self.object.get_canonical_url()
        meta_dict['title'] = self.object.title if self.object.title else \
            '{} University - Shine Learning'.format(self.object.name)
        meta_dict['heading'] = self.object.heading
        return meta_dict

    def get_context_data(self, **kwargs):
        context = super(UniversityPageView, self).get_context_data(**kwargs)
        standalone_products = self._get_all_products_of_category()
        all_product_ids = self._get_product_variation_combo_ids(
            standalone_products)
        context['products'] = self._get_paginated_products(
            standalone_products)
        context['reviews'] = self._get_paginated_reviews(
            all_product_ids)
        context.update({"meta": self._get_page_meta_data()})
        context.update(
            {"canonical_url": self.object.get_canonical_url()})
        context.update(
            {"country_choices": self._get_country_choices()})
        context.update(
            {"initial_country": self._get_preselected_country()})
        return context


class UniversityFacultyView(DetailView):
    model = Faculty
    template_name = "university/detail_faculty.html"
    context_object_name = "faculty_obj"

    PRODUCT_PAGE_SIZE = 6

    def get_queryset(self):
        return Faculty.objects.filter(
            active=True)

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        slug = self.kwargs.get('faculty_slug')
        if queryset is None:
            queryset = self.get_queryset()

        if pk is not None:
            queryset = queryset.filter(
                pk=pk, active=True)
        elif slug is not None:
            queryset = queryset.filter(
                slug=slug, active=True)

        if queryset.exists():
            return queryset.first()
        else:
            raise Http404

    def _get_paginated_products(self, products=[], page=1):
        """
        Return the first 5 results of products list.
        In compliance with Ajax views for Product Load More.
        """
        if not products:
            products = self.object.facultyproducts.filter(
                is_indexable=True, active=True,
                type_product__in=[0, 1, 3, 5],
                type_flow=14)
        prod_page = Paginator(products, self.PRODUCT_PAGE_SIZE)

        products = prod_page.page(page)
        for product in products:
            if not float(product.pPfin): continue
            product.discount = round((float(product.pPfin) - float(product.pPin)) * 100 / float(product.pPfin), 2)
        return products

    def _get_page_meta_data(self):
        meta_dict = self.object.as_meta(self.request).__dict__
        meta_dict['description'] = self.object.get_description()
        meta_dict['og_description'] = self.object.get_description()
        meta_dict["_url"] = self.object.get_canonical_url()
        meta_dict['title'] = self.object.title if self.object.title else \
            '{} University - Shine Learning'.format(self.object.name)
        meta_dict['heading'] = self.object.heading
        return meta_dict

    def get_context_data(self, **kwargs):
        context = super(UniversityFacultyView, self).get_context_data(**kwargs)
       
        context['products'] = self._get_paginated_products(
            standalone_products)
        context.update({"meta": self._get_page_meta_data()})
        context.update(
            {"canonical_url": self.object.get_canonical_url()})
        return context
