import json
import logging,numpy
from itertools import zip_longest

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
from django.utils import timezone
from django.shortcuts import reverse

from geolocation.models import Country
from django.db.models import Q
from shop.models import (
    Category, Faculty, Product,SubCategory)
from shop.choices import (
    FACULTY_TEACHER, FACULTY_PRINCIPAL)
from homepage.config import UNIVERSITY_PAGE
from cms.mixins import UploadInFile
from partner.models import Vendor
from homepage.models import Testimonial,TestimonialCategoryRelationship
from review.models import Review
from crmapi.models import UNIVERSITY_LEAD_SOURCE
from .mixins import SkillPageMixin
from review.models import DetailPageWidget
from assessment.models import Test
from shop.models import SubHeaderCategory
from shop.choices import STUDY_MODE

# Create your views here.


class SkillPageView(DetailView, SkillPageMixin):
    model = Category
    template_name = "skillpage/skill-new.html"
    no_of_products = 5

    # def get_object(self, queryset=None):   # format this code ?????????????????????????????????????????????????????????????????
    #     pk = self.kwargs.get('pk')
    #     slug = self.kwargs.get('skill_slug')

    #     if queryset is not None:
    #         return queryset.first()

    #     queryset = self.get_queryset()
    #     return queryset.first()

        # if pk is not None:
        #     queryset = queryset.prefetch_related('categoryproducts').filter(pk=pk, active=True, is_skill=True, type_level__in=[3,4])
        # elif slug is not None:
        #     queryset = queryset.prefetch_related('categoryproducts').filter(slug=slug, active=True, is_skill=True, type_level__in=[3,4])

        # if queryset:
        #     return queryset[0]
        # else:
        #     raise Http404

    # def get_template_names(self):  #amp page required seo ?????????????????????????????????????????????????????????????????????????
    #     if not self.request.amp:
    #         return ["skillpage/skill-new.html"]
    #     return ["skillpage/skill-amp.html"]
        
    # def redirect_if_necessary(self, current_path, skill):
    #     expected_path = skill.get_absolute_url()
    #     if expected_path != urlquote(current_path):
    #         return HttpResponsePermanentRedirect(expected_path)
    #     return None

    def get(self, request, *args, **kwargs):
        # self.pk = self.kwargs.get('pk', None)
        # self.object = self.get_object()
        # redirect = self.redirect_if_necessary(request.path, self.object)
        # if redirect:
        #     return redirect
        context = super(SkillPageView, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(SkillPageView, self).get_context_data(**kwargs)
        subheading = SubHeaderCategory.objects.filter(category=self.object)
        career_outcomes = self.object.split_career_outcomes()
        subheading_id_data_mapping = {}

        courses = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).filter(pCtg=self.object.pk).exclude(pTF=16)
        course_count = courses.count()
        assesments = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).filter(pCtg=self.object.pk, pTF=16)
        assesment_count = assesments.count()
        product_mode_choices = dict(STUDY_MODE)
        country_choices = [(m.phone, m.name) for m in Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
        country_choices = sorted(country_choices, key=lambda x: x[0])

        widget_obj = DetailPageWidget.objects.filter(content_type__model='Category', listid__contains=self.object.pk).first()
        widget_obj_data = widget_obj.widget.iw.indexcolumn_set.filter(column=1) if widget_obj and widget_obj.widget else []
        testimonialcategory = list(TestimonialCategoryRelationship.objects.filter(category=self.object.id,\
                    testimonial__is_active=True).select_related('testimonial'))
        
        for heading in subheading:
            subheading_id_data_mapping.update({
                heading.heading_choice_text : heading
            })
        
        context.update({
            'subheading':subheading_id_data_mapping,
            'category':self.object,
            'career_outcomes':career_outcomes,
            'courses':courses[:self.no_of_products],
            'course_count':course_count,
            'top_3_courses':courses[:3],
            'assesments':assesments[:self.no_of_products],
            'assesment_count':assesment_count,
            'widget_name':widget_obj.name if widget_obj else '',
            'widget_obj_data':widget_obj_data,
            'breadcrumbs':self.get_breadcrumb_data(),
            'country_choices':country_choices,
            'testimonialcategory':testimonialcategory,
            'product_mode_choices':product_mode_choices,
        })
        return context

    def get_breadcrumb_data(self):
        breadcrumbs = []
        breadcrumbs.append({"url": '/', "name": "Home"})
        parent = self.object.get_parent()
        if parent:
            breadcrumbs.append({
                "url": parent.first().get_absolute_url(), "name": parent.first().name,
            })
        breadcrumbs.append({"url": '', "name": self.object.name})
        return breadcrumbs

    # def get_context_data(self, **kwargs):
    #     context = super(SkillPageView, self).get_context_data(**kwargs)
    #     page = self.request.GET.get('page', 1)
    #     api_data = self.get_job_count_and_fuctionan_area(self.object.name)
    #     career_outcomes = self.object.split_career_outcomes()
    #     country_choices = [(m.phone, m.name) for m in
    #                        Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
    #     initial_country = Country.objects.filter(phone='91')[0].phone
    #     top_3_prod, top_4_vendors = None, None
    #     prd_list = []
    #     prd_text = None
    #     meta_desc = None
    #     prod_id_list = []
    #     prod_tests = []

    #     try:
    #         products = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).filter(pCtg=self.pk).exclude(pTF=16)  //exclude tp 16
    #         assesments = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).filter(pCtg=self.pk, pTF=16)
    #         if assesments:
    #             prod_tests = assesments.values_list('id',flat=True)
    #             prod_tests = Test.objects.filter(product__id__in=prod_tests).values_list('product__id','slug')   ///v-skills ke
    #             prod_tests = dict(prod_tests)

    #         for prd in products:
    #             if prd.pTP == 1:  type product variation parent
    #                 prd_vars = json.loads(prd.pVrs)  pvrs child
    #                 var_lists = prd_vars.get('var_list')   
    #                 for var_lst in var_lists:
    #                     prod_id_list.append(var_lst.get('id'))
    #                 prod_id_list.append(prd.id)
    #             if prd.pTP == 3:    combo
    #                 prd_cmbs = json.loads(prd.pCmbs)
    #                 combo_lists = prd_cmbs.get('combo_list')
    #                 for combo_lst in combo_lists:
    #                     prod_id_list.append(combo_lst.get('pk'))
    #                 prod_id_list.append(prd.id)
    #             if prd.pTP in [0, 2, 4, 5]: 
    #                 prod_id_list.append(prd.id)

    #         # prod_id_list = [pv.id for pv in products]
    #         vendor_list = [pv.pPv for pv in products]
    #         vendor_list = list(set(vendor_list))

    #         if not len(prod_id_list):
    #             raise Http404
    #         top_3_prod = products[:3]
    #         for tp_prod in top_3_prod:
    #             prd_list.append(tp_prod.pNm)
    #         top_4_vendors = Vendor.objects.filter(id__in=vendor_list)[:4] if len(vendor_list) >= 4 else Vendor.objects.filter(id__in=vendor_list)
    #     except Exception as e:
    #         logging.getLogger('error_log').error(" MSG:unable to load the list   %s" %str(e))

    #     prd_obj = ContentType.objects.get_for_model(Product)
    #     # all_results = products
    #     prod_reviews = Review.objects.filter(
    #         object_id__in=prod_id_list,
    #         content_type=prd_obj,
    #         status=1)

    #     prod_page = Paginator(all_results, 5)

    #     try:
    #         products = prod_page.page(self.page)
    #     except PageNotAnInteger:
    #         products = prod_page.page(1)
    #     except EmptyPage:
    #         products = prod_page.page(prod_page.num_pages)
    #     for product in products:
    #         if float(product.pPfin):
    #             product.discount = round((float(product.pPfin) - float(product.pPin)) * 100 / float(product.pPfin), 2)

    #     all_cert = assesments
    #     cert_page = Paginator(all_cert, 5)
    #     try:
    #         assesments = cert_page.page(self.page)
    #     except PageNotAnInteger:
    #         assesments = cert_page.page(1)
    #     except EmptyPage:
    #         assesments = cert_page.page(cert_page.num_pages)
    #     for product in assesments:
    #         if float(product.pPfin):
    #             product.discount = round((float(product.pPfin) - float(product.pPin)) * 100 / float(product.pPfin), 2)

    #     prod_review = Paginator(prod_reviews, 5)

    #     try:
    #         page_reviews = prod_review.page(self.page)
    #     except PageNotAnInteger:
    #         page_reviews = prod_review.page(1)
    #     except EmptyPage:
    #         page_reviews = prod_review.page(prod_review.num_pages)

    #     if prd_list:
    #         prd_text = ' , '.join(prd_list)
    #     if self.object.name and prd_text:
    #         meta_desc = "Get online certification in {}. Check discounted price and offers on short term professional courses like {} and more".format(self.object.name, prd_text)
    #     context['meta'] = self.object.as_meta(self.request)
    #     context['canonical_url'] = self.object.get_canonical_url()
    #     context['meta']._url = context.get('canonical_url', '')
    #     meta_dict = context['meta'].__dict__
    #     meta_dict['description'] = meta_desc
    #     meta_dict['og_description'] = meta_desc
    #     if products.paginator.count:
    #         meta_title = '{} Courses ({} Certification Programs) - Shine Learning'.format(
    #             self.object.name, products.paginator.count)
    #     else:
    #         meta_title = '{} Courses - Shine Learning'.format(
    #             self.object.name)
    #     meta_dict['title'] = meta_title

    #     sub headings
    #     subheading = SubHeaderCategory.objects.filter(category=self.object)
    #     subheading_id_data_mapping = {}

    #     for heading in subheading:
    #         subheading_id_data_mapping.update({
    #             heading.heading_choice_text : heading
    #         })
        
    #     context.update({
    #         'subheading':subheading_id_data_mapping,
    #         'category':self.object
    #     })

    #     context.update({
    #         "api_data": api_data,
    #         "career_outcomes": career_outcomes,
    #         "page": page,
    #         "slug": self.object.name,
    #         "category_obj": self.object,
    #         "top_3_prod": top_3_prod,
    #         "top_4_vendors": top_4_vendors,
    #         "products": products,
    #         "assesments": assesments,
    #         'site': settings.SITE_PROTOCOL + "://" + settings.SITE_DOMAIN,
    #         "page_reviews": prod_reviews[0:4] if self.request.flavour else page_reviews,
    #         'url': settings.SITE_PROTOCOL + "://" + self.object.video_link,
    #         'country_choices': country_choices,
    #         'initial_country': initial_country,
    #         'show_chat': True,
    #         'amp': self.request.amp,
    #         'prod_tests':prod_tests,
    #         'subheading':subheading_id_data_mapping
    #     })
    #     try:
    #         widget_obj = DetailPageWidget.objects.get(
    #             content_type__model='Category', listid__contains=self.pk)
    #         widget_objs = widget_obj.widget.iw.indexcolumn_set.filter(
    #             column=1)
    #     except DetailPageWidget.DoesNotExist:
    #         widget_objs = None
    #         widget_obj = None
    #     context['widget_objs'] = widget_objs
    #     context['widget_obj'] = widget_obj
    #     context.update(self.get_breadcrumb_data())
    #     return context

    # def get_breadcrumb_data(self):
    #     breadcrumbs = []
    #     breadcrumbs.append({"url": '/', "name": "Home"})
    #     parent = self.object.get_parent()
    #     if parent:
    #         breadcrumbs.append({
    #             "url": parent[0].get_absolute_url(), "name": parent[0].name,
    #         })
    #     breadcrumbs.append({"url": '', "name": self.object.name})
    #     data = {"breadcrumbs": breadcrumbs}
    #     return data


class ServiceDetailPage(DetailView):
    model = Category
    slug_field = 'slug'
    slug_url_kwarg = 'category_slug'
    pk_url_kwarg = 'category_id'
    context_object_name = "category_obj"
    query_pk_and_slug = True

    PRODUCT_PAGE_SIZE = 5
    REVIEW_PAGE_SIZE = 5

    def get_template_names(self):
        if self.request.amp:
            return ["services/detail-amp.html"]
        return ["services/detail.html"]

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

        cache.set('callback_country_choices', country_choices, 86400)
        return country_choices

    def _get_preselected_country(self):
        cached_initial_country = cache.get('callback_initial_country')
        if cached_initial_country:
            return cached_initial_country

        initial_country = Country.objects.filter(phone='91')[0].phone
        cache.set("callback_initial_country", initial_country, 86400)
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

    PRODUCT_PAGE_SIZE = 6

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
            filter(pTF=14, pCtg=self.object.pk)  # pTF=14, pCtg=self.object.pk
        return products

    def _get_paginated_products(self, products, page=1):
        """
        Return the first 5 results of products list.
        In compliance with Ajax views for Product Load More.
        """
        prod_page = Paginator(products, self.PRODUCT_PAGE_SIZE)
        products = prod_page.page(page)
        for product in products:
            if product.pVrs:
                product.pVrs = json.loads(product.pVrs)
            if product.pUncdl:
                product.pUncdl = json.loads(product.pUncdl[0])
            if not float(product.pPfin): continue
            product.discount = round((float(product.pPfin) - float(product.pPin)) * 100 / float(product.pPfin), 2)

        return products
        
    def _get_subheaders_category(self):
        """
        return the first 5 subheading according to display order
        """
        subheaders = self.object.subheaders.filter(
            active=True).order_by('display_order')
        return subheaders[: 5]

    def _get_university_faculty(self):
        """
        return all faculty of university
        """
        faculty = self.object.faculty_set.filter(
            active=True, role=FACULTY_TEACHER)
        step = 2
        faculty = [faculty[x: x + step] for x in range(0, len(faculty), step)]
        return faculty

    def _get_faculty_principal(self):
        """
        return university principal speak
        """
        principals = self.object.faculty_set.filter(
            role=FACULTY_PRINCIPAL,
            active=True,
        )
        return principals.first()

    def _get_testimonials_category(self):
        testimonials = Testimonial.objects.filter(
            page=UNIVERSITY_PAGE, object_id=self.object.pk,
            is_active=True).order_by('priority')
        return testimonials[: 3]

    def _get_page_meta_data(self):
        meta_dict = self.object.as_meta(self.request).__dict__
        meta_dict['description'] = self.object.get_description()
        meta_dict['og_description'] = self.object.get_description()
        meta_dict["_url"] = self.object.get_canonical_url()
        meta_dict['title'] = self.object.title if self.object.title else \
            '{} - Shine Learning'.format(self.object.heading)
        meta_dict['heading'] = self.object.heading
        return meta_dict

    def get_context_data(self, **kwargs):
        context = super(UniversityPageView, self).get_context_data(**kwargs)
        standalone_products = self._get_all_products_of_category()
        context['products'] = self._get_paginated_products(
            standalone_products)
        context['subheaders'] = self._get_subheaders_category()
        context['faculty'] = self._get_university_faculty()
        context['testimonials'] = self._get_testimonials_category()
        context['principal'] = self._get_faculty_principal()
        context.update({"country_choices": self._get_country_choices()})
        context.update({"initial_country": self._get_preselected_country()})

        context.update({"meta": self._get_page_meta_data()})
        context.update(
            {"canonical_url": self.object.get_canonical_url()})
        context.update({
            "PRODUCT_PAGE_SIZE": self.PRODUCT_PAGE_SIZE,
            "UNIVERSITY_LEAD_SOURCE": UNIVERSITY_LEAD_SOURCE,
            "today_date": timezone.now()\
            .date().strftime('%d %b %Y').upper()})
        return context


class UniversityFacultyView(DetailView):
    model = Faculty
    template_name = "university/detail_faculty.html"
    context_object_name = "faculty_obj"

    # PRODUCT_PAGE_SIZE = 6

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
        Return the first 9 results of products list.
        In compliance with Ajax views for Product Load More.
        """
        if not products:

            products = self.object.products.prefetch_related(
                'facultyproducts').filter(
                type_product__in=[0, 1, 3, 5],
                type_flow=14, is_indexable=True,
                active=True,
                facultyproducts__active=True,
                facultyproducts__faculty=self.object).order_by(
                'facultyproducts__display_order')

            #is_indexed=True
        # prod_page = Paginator(products, self.PRODUCT_PAGE_SIZE)

        # products = prod_page.page(page)
        return products[: 9]

    def _get_page_meta_data(self):
        meta_dict = self.object.as_meta(self.request).__dict__
        meta_dict['description'] = self.object.get_description()
        meta_dict['og_description'] = self.object.get_description()
        meta_dict["_url"] = self.object.get_canonical_url()
        meta_dict['title'] = self.object.title if self.object.title else \
            '{} - Shine Learning'.format(self.object.name)
        meta_dict['heading'] = self.object.heading
        return meta_dict

    def get_context_data(self, **kwargs):
        context = super(UniversityFacultyView, self).get_context_data(**kwargs)
        context.update({"meta": self._get_page_meta_data()})
        context.update({
            "products": self._get_paginated_products(),
            "university": self.object.institute,
            "today_date": timezone.now().date()})
        context.update(
            {"canonical_url": self.object.get_canonical_url()})
        return context


class LocationSkillPageView(DetailView, SkillPageMixin):
    model = SubCategory
    page = 1

    def get_object(self, queryset=None):
        slug = self.kwargs.get('sc_slug')
        if not slug:
            raise Http404
        sub_cat_object = SubCategory.objects.filter(slug=slug,active=True).first()
        if not sub_cat_object:
            raise Http404
        return sub_cat_object




    # def slug_breaker(self,slug):
    #     import  ipdb;
    #     ipdb.set_trace()
    #     if not slug:
    #         return None,None
    #     slug_list = slug.split('-')
    #     loc_id = 0
    #     city = None
    #     for loc_id, slug in enumerate(slug_list,start=1):
    #         slug_to_compare = "-".join(slug_list[loc_id:])
    #         city = cities_slug_dict.get(slug_to_compare,None)
    #         if city:
    #             break
    #     else:
    #         return None, None
    #
    #     cat_slug = "-".join(slug_list[:loc_id])
    #     cat_obj = SubCategory.objects.filter(category__slug=cat_slug).first()
    #     if cat_obj and city:
    #         return cat_obj, city
    #     return None, None




    def get_template_names(self):
        if not self.request.amp:
            return ["locationskillpage/skill.html"]
        return ["locationskillpage/skill-amp.html"]


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = super(LocationSkillPageView, self).get(request, args, **kwargs)
        return context

    def get_context_data(self, **kwargs):
        context = super(LocationSkillPageView, self).get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        api_data = self.get_job_count_and_fuctionan_area(self.object.category.name)
        career_outcomes = self.object.split_career_outcomes()
        country_choices = [(m.phone, m.name) for m in
                           Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
        initial_country = Country.objects.filter(phone='91')[0].phone
        top_3_prod, top_4_vendors = None, None
        prd_list = []
        prd_text = None
        meta_desc = None
        prod_id_list = []
        products = []
        try:
            if self.object.products_id_mapped():
                products = SQS().filter(id__in=self.object.products_id_mapped())
            else:
                products = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).filter(pCtg=self.object.category.id)
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
            top_4_vendors = Vendor.objects.filter(id__in=vendor_list)[:4] if len(
                vendor_list) >= 4 else Vendor.objects.filter(id__in=vendor_list)
        except Exception as e:
            logging.getLogger('error_log').error(" MSG:unable to load the list   %s" % str(e))

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

        # if prd_list:
        #     prd_text = ' , '.join(prd_list)
        # if self.object.category.name and prd_text:
        #     meta_desc = '{skill} courses in {location} - Are you looking for a {skill} courses in {location} - Check complete fee structure, training programme from top institutes.'.format(skill=self.object.category.name,location=self.object.get_location_display())
        context['meta'] = self.object.as_meta(self.request)
        context['canonical_url'] = self.object.get_canonical_url()
        context['meta']._url = context.get('canonical_url', '')
        meta_dict = context['meta'].__dict__
        meta_dict['description'] = self.object.get_meta_description()
        meta_dict['og_description'] = self.object.get_meta_description()
        meta_title = self.object.get_title()
        meta_dict['title'] = meta_title
        context.update({
            "api_data": api_data,
            "career_outcomes": career_outcomes,
            "page": page,
            "slug": self.object.slug,
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
                content_type__model='SubCategory', listid__contains=self.object.pk)
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
            cat_parent = parent.get_parent()[0] if parent.get_parent() else ""
            if cat_parent:
                breadcrumbs.append({'url': cat_parent.get_absolute_url(),'name':cat_parent.name})

            breadcrumbs.append({
                "url": parent.get_absolute_url(), "name": parent.name,
            })
            # breadcrumbs.append({"url": })
        breadcrumbs.append({"url": '', "name": self.object.get_location_display()})
        data = {"breadcrumbs": breadcrumbs}
        return data


