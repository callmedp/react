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

from geolocation.models import Country
from django.db.models import Q
from shop.models import Category
from cms.mixins import UploadInFile
from partner.models import Vendor
from review.models import Review
from shop.models import Product
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
            meta_title = '{} Courses ({} Certification Programs) - ShineLearning'.format(
                self.object.name, products.paginator.count)
        else:
            meta_title = '{} Courses - ShineLearning'.format(
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
