import json
import logging

from collections import OrderedDict
from decimal import Decimal

from django.core.paginator import Paginator
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
)
from django.urls import reverse
from django.utils import timezone
from django.core.cache import cache
from django.utils.http import urlquote
from django.views.generic import (
    ListView,
    TemplateView,
    View,
    CreateView
)
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from geolocation.models import Country
from django.db.models import Q
from django.template.loader import render_to_string

from haystack.query import SearchQuerySet
from meta.views import MetadataMixin

from console.decorators import (
    Decorate,
    stop_browser_cache,)
from cart.mixins import CartMixin
from core.library.haystack.query import SQS
from search.helpers import get_recommendations
from search.choices import STUDY_MODE
from homepage.models import Testimonial
from review.models import Review
from order.models import OrderItem

from .models import Product
from review.models import DetailPageWidget
from .mixins import CourseCatalogueMixin, LinkedinSeriviceMixin
from users.forms import (
    ModalLoginApiForm
)
from shop.choices import APPLICATION_PROCESS, BENEFITS
from review.forms import ReviewForm


class ProductInformationMixin(object):

    def get_solar_fakeprice(self, inr_price, fake_inr_price):
        if inr_price is not None:
            inr_price = inr_price
            fake_inr_price = fake_inr_price
            if fake_inr_price > Decimal('0.00'):
                diff = float(fake_inr_price) - float(inr_price)
                percent_diff = round((diff / float(fake_inr_price)) * 100, 0)
                return (round(fake_inr_price, 0), percent_diff)
        return None

    def get_breadcrumbs(self, product, category):
        breadcrumbs = []
        breadcrumbs.append(
            OrderedDict({
                'label': 'Home',
                'url': '/',
                'active': True}))
        if category:
            if category.type_level == 4:
                category = category.get_parent()[0] if category.get_parent() else None
        if category:
            if product.is_course:
                parent = category.get_parent()
                if parent:
                    breadcrumbs.append(
                        OrderedDict({
                            'label': parent[0].name,
                            'url': parent[0].get_absolute_url(),
                            'active': True}))

            if product.is_service or product.is_writing:
                if category.is_service and category.type_level == 3:
                    breadcrumbs.append(
                        OrderedDict({
                            'label': category.name,
                            'url': category.get_absolute_url(),
                            'active': True}))
                else:
                    parent = category.get_parent()
                    if parent:
                        breadcrumbs.append(
                            OrderedDict({
                                'label': parent[0].name,
                                'url': reverse('func_area_results', kwargs={'fa_slug':parent[0].slug, 'pk': parent[0].id}),
                            'active': True}))
            else:
                breadcrumbs.append(
                    OrderedDict({
                        'label': category.name,
                        'url': category.get_absolute_url(),
                        'active': True}))
        breadcrumbs.append(
            OrderedDict({
                'label': product.name,
                'active': None}))
        return {
            'breadcrumbs': breadcrumbs
        }

    def solar_info(self, product):
        info = {}
        info['prd_img'] = product.pImg
        info['prd_img_alt'] = product.pImA
        info['prd_img_bg'] = product.pIBg
        info['prd_H1'] = product.pHd if product.pHd else product.pNm
        info['prd_about'] = product.pAb
        info['prd_desc'] = product.pDsc
        info['prd_uget'] = product.pBS
        info['prd_rating'] = round(float(product.pARx), 1)
        info['prd_num_rating'] = product.pRC
        info['prd_num_bought'] = product.pBC
        info['prd_num_jobs'] = product.pNJ
        info['prd_vendor'] = product.pPvn
        info['prd_vendor_img'] = product.pVi
        # info['prd_vendor_img_alt'] = product.vendor.image_alt
        info['prd_rating_star'] = product.pStar
        info['prd_video'] = product.pvurl
        info['start_price'] = product.pPinb
        if product.pPc == 'course':
            info['prd_service'] = 'course'
        elif product.pPc == 'writing':
            info['prd_service'] = 'resume'
        elif product.pPc == 'service':
            info['prd_service'] = 'service'
        else:
            info['prd_service'] = 'other'
        info['prd_product'] = product.pTP
        info['prd_exp'] = product.pEX
        return info

    def get_program_structure(self, product):
        structure = {
            'prd_program_struct': False,
            'chapter': False,
        }
        chapter_list = product.chapter_product.filter(status=True)
        if chapter_list:
            structure.update({
                'prd_program_struct': True,
                'chapter': True,
                'chapter_list': chapter_list
            })
        return structure

    def solar_program_structure(self, product):
        structure = json.loads(product.pPChs)
        return structure

    def get_faq(self, product):
        structure = {
            'prd_faq': False
        }
        faqs = product.faqs.filter(
            productfaqs__active=True, status=2).order_by('productfaqs__question_order')
        if faqs:
            structure.update({
                'prd_faq': True,
                'faq_list': faqs
            })
        return structure

    def get_jobs_url(self, product):
        job_url = 'https://www.shine.com/job-search/{}-jobs'.format(product.slug)\
        if product.slug else None
        return job_url

    def solar_faq(self, product):
        structure = json.loads(product.pFAQs)
        return structure

    def get_recommendation(self, product):
        recommendation = {
            'prd_recommend': False,
        }
        rcourses = get_recommendations(
            self.request.session.get('func_area', None),
            self.request.session.get('skills', None))
        if rcourses:
            rcourses = rcourses.exclude(id=product.id)
            rcourses = rcourses[:6]
        if rcourses:
            recommendation.update({
                'prd_recommend': True,
                'recommended_products': rcourses
            })
        return recommendation

    def get_other_package(self, product, category):
        package = {
            'other_package': False,
        }
        categoryproducts = category.categoryproducts.filter(
            active=True,).exclude(pk=product.pk).distinct()
        if categoryproducts:
            package.update({
                'other_package': True,
                'package_list': categoryproducts[:4]})
        return package

    def get_other_provider(self, product, category):
        provider = {
            'other_provider': False,
        }
        providers = category.categoryproducts.filter(
            active=True).exclude(pk=product.pk).distinct()
        if providers:
            provider.update({
                'other_provider': True,
                'provider_list': providers[:4]})
        return provider

    def get_combos(self, product):
        combos = product.childs.filter(active=True)
        return {'combos': combos}

    def is_combos(self, product):
        combos = json.loads(product.pCmbs)
        if combos['combo']:
            return True
        return False

    def get_variation(self, product):
        if product.is_course:
            course_dict = []
            selected_var = None
            course_list = product.variation.filter(
                siblingproduct__active=True).order_by('-siblingproduct__sort_order')
            if course_list:
                from shop.choices import MODE_CHOICES, COURSE_TYPE_CHOICES
                for course in course_list:
                    fake_price = course.get_fakeprice()
                    if fake_price:
                        fake_price = fake_price[0]
                    else:
                        fake_price = 0

                    if not selected_var:
                        selected_var = course
                    course_dict.append(
                        OrderedDict({
                            'id': course.id,
                            'label': course.name,
                            'mode': getattr(course.attr, 'study_mode', None),
                            'duration': getattr(course.attr, 'duration', None),
                            'type': getattr(course.attr, 'study_type', None),
                            'certify': getattr(course.attr, 'certification', None),
                            'price': course.get_price(),
                            'fake_price': fake_price}))
            return {'course_variation_list': course_dict, 'selected_var': selected_var}
        else:
            service_list = []
            service_list = product.variation.filter(
                siblingproduct__active=True).order_by('-siblingproduct__sort_order')
            return {'country_variation_list': service_list}

    def var_list(self, product):
        course_variation_list = json.loads(product.pVrs)
        return course_variation_list

    def get_frequentlybought(self, product, category):
        prd_fbt = {
            'prd_fbt': False,
        }
        prd_fbt_list = product.related.filter(
            secondaryproduct__active=True,
            secondaryproduct__type_relation=1)
        if prd_fbt_list:
            prd_fbt.update({
                'prd_fbt': True,
                'prd_fbt_list': prd_fbt_list})
        return prd_fbt

    def get_reviews(self, product, page):
        product_type = ContentType.objects.get(
            app_label='shop', model='product')
        try:
            prd_list = []
            if product.type_product in [0, 2, 4, 5]:
                prd_list = [product.pk]
            elif product.type_product == 1:
                prd_id = product.variation.filter(
                    siblingproduct__active=True,
                    active=True).values_list('id', flat=True)
                prd_list = list(prd_id)
                prd_list.append(product.pk)
            elif product.type_product == 3:
                prd_id = product.childs.filter(
                    childrenproduct__active=True,
                    active=True).values_list('id', flat=True)
                prd_list = list(prd_id)
                prd_list.append(product.pk)
            # review_list = Review.objects.filter(
            #     content_type__id=product_type.id,
            #     object_id=product.pk, status=1)
            review_list = Review.objects.filter(
                content_type__id=product_type.id,
                object_id__in=prd_list, status=1)
            rv_total = len(review_list)
            per_page = 5
            rv_paginator = Paginator(review_list, per_page)
            rv_page = int(page if page else 1)
            try:
                review_list = rv_paginator.page(rv_page)
            except Exception as e:
                logging.getLogger('error_log').error(str(e))
                review_list = []
            return {
                'prd_rv_total': rv_total,
                'prd_review_list': review_list,
                'prd_rv_page': rv_page}
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
            return {
                'prd_rv_total': 0,
                'prd_review_list': [],
                'prd_rv_page': page
            }

    def get_product_detail_context(self, product, sqs, product_main, sqs_main):
        pk = product.pk
        ctx = {}

        ctx['product'] = product
        ctx['num_jobs_url'] = self.get_jobs_url(product)
        if product:
            ctx.update(self.get_breadcrumbs(product, product.category_main))
        ctx.update(self.solar_info(sqs))
        if product.is_course:
            ctx.update(self.solar_program_structure(sqs))
        ctx.update(self.solar_faq(sqs))
        ctx.update(self.get_recommendation(product))
        ctx.update(self.get_reviews(product, 1))
        country_choices = [(m.phone, m.name) for m in
                           Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
        initial_country = Country.objects.filter(phone='91')[0].phone
        ctx.update({
            'country_choices': country_choices,
            'initial_country': initial_country,
        })
        if sqs.pPc == 'course':
            ctx.update(json.loads(sqs_main.pPOP))
            pvrs_data = json.loads(sqs.pVrs)
            try:
                selected_var = pvrs_data['var_list'][0]
            except Exception as e:
                selected_var = None
            ctx.update({'selected_var': selected_var})
            ctx.update(pvrs_data)
            ctx['canonical_url'] = product.get_canonical_url()
            if self.product_obj.type_flow == 14:
                ctx['university_detail'] = json.loads(sqs.pUncdl[0])
                faculty = [f.faculty for f in self.product_obj.facultyproducts.all().select_related('faculty','faculty__institute')]
                ctx['faculty'] = [faculty[i:i + 1]for i in range(len(faculty))]
                ctx['institute'] = self.product_obj.category_main
                app_process = ctx['university_detail']['app_process']
                ctx['university_detail']['app_process'] = [APPLICATION_PROCESS.get(proc) for proc in app_process]
                app_process = ctx['university_detail']['benefits']
                ctx['university_detail']['benefits'] = [BENEFITS.get(proc) for proc in app_process]
        else:
            if ctx.get('prd_exp', None) in ['EP', 'FP']:
                pPOP = json.loads(sqs_main.pPOP)
                pid = None
                for pop in pPOP.get('pop_list'):
                    if pop.get('experience', '') == 'FR' and ctx.get('prd_exp', None) == 'FP':
                        pid = pop.get('id')
                        break
                    elif pop.get('experience', '') == 'SP' and ctx.get('prd_exp', None) == 'EP':
                        pid = pop.get('id')
                        break
                try:
                    if pid:
                        pid = Product.objects.get(pk=pid)
                        ctx['canonical_url'] = pid.get_canonical_url()
                    else:
                        ctx['canonical_url'] = product.get_canonical_url()
                except Exception as e:
                    ctx['canonical_url'] = product.get_canonical_url()
                    logging.getLogger('error_log').error(
                        "%(msg)s : %(err)s" % {'msg': 'Canonical Url ERROR', 'err': e})
            else:
                ctx['canonical_url'] = product.get_canonical_url()
            ctx.update(json.loads(sqs_main.pPOP))
            pvrs_data = json.loads(sqs.pVrs)
            ctx.update(pvrs_data)
        if self.is_combos(sqs):
            ctx.update(json.loads(sqs.pCmbs))

        ctx.update(json.loads(sqs.pFBT))
        get_fakeprice = self.get_solar_fakeprice(
            sqs.pPinb, sqs.pPfinb)

        ctx.update(self.getSelectedProduct_solr(sqs))
        # ctx.update(self.getSelectedProductPrice_solr(self.sqs))

        try:
            widget_obj = DetailPageWidget.objects.get(
                content_type__model='Product', listid__contains=pk)
            widget_objs = widget_obj.widget.iw.indexcolumn_set.filter(
                column=1)
        except DetailPageWidget.DoesNotExist:
            widget_objs = None
            widget_obj = None
        ctx['domain_name'] = '{}//{}'.format(settings.SITE_PROTOCOL, settings.SITE_DOMAIN)
        ctx.update({'sqs': sqs})
        ctx.update({'get_fakeprice': get_fakeprice})
        ctx['meta'] = product.as_meta(self.request)
        ctx['meta']._url = ctx.get('canonical_url', '')
        ctx['show_chat'] = True
        ctx['amp'] = self.request.amp
        ctx['widget_objs'] = widget_objs
        ctx['widget_obj'] = widget_obj
        ctx['product_main'] = product_main,
        ctx['sqs_main'] = sqs_main
        ctx['is_logged_in'] = True if self.request.session.get('candidate_id') else False
        ctx["loginform"] = ModalLoginApiForm()
        ctx['linkedin_resume_services'] = settings.LINKEDIN_RESUME_PRODUCTS
        if self.request.session.get('candidate_id'):
            candidate_id = self.request.session.get('candidate_id')
            contenttype_obj = ContentType.objects.get_for_model(product)
            review_obj = Review.objects.filter(
                object_id=product.id, content_type=contenttype_obj, user_id=candidate_id
            )
            if review_obj.count() > 0:
                ctx['review_obj'] = review_obj[0]
            else:
                ctx['review_obj'] = None
            # user_reviews depicts if user already has a review for this product or not
            product_type = ContentType.objects.get(
                app_label='shop', model='product')
            candidate_id = self.request.session.get('candidate_id', None)
            user_reviews = Review.objects.filter(
                content_type=product_type,
                object_id=pk, status__in=[0, 1],
                user_id=candidate_id
            ).count()

            ctx['user_reviews'] = True if user_reviews else False
        navigation = True
        if sqs.id in settings.LINKEDIN_RESUME_PRODUCTS:
            navigation = False
        ctx['navigation'] = navigation

        return ctx


@Decorate(stop_browser_cache())
class ProductDetailView(TemplateView, ProductInformationMixin, CartMixin):
    context_object_name = 'product'
    http_method_names = ['get', 'post']

    model = Product

    def __init__(self, *args, **kwargs):
        # _view_signal = product_viewed
        self.category = None
        self.product_obj = None
        # # Whether to redirect to the URL with the right path
        self._enforce_paths = True
        # # Whether to redirect child products to their parent's URL
        self._enforce_parent = True
        self.sqs = None

        super(ProductDetailView, self).__init__(*args, **kwargs)

    def get_template_names(self):
        if self.product_obj.type_flow==14:
            return['shop/university.html']
        if self.request.amp:
            from newrelic import agent
            agent.disable_browser_autorum()
            return ['shop/detail-amp.html']
        return ['shop/detail1.html']

    def get_context_data(self, **kwargs):
        ctx = super(ProductDetailView, self).get_context_data(**kwargs)
        product_data = self.get_product_detail_context(
            self.product_obj, self.sqs,
            self.product_obj, self.sqs)

        product_detail_content = render_to_string(
            'shop/product-detail.html', product_data,
            request=self.request)

        ctx.update({
            'product_detail': product_detail_content,
            "ggn_contact_full": settings.GGN_CONTACT_FULL,
            "ggn_contact": settings.GGN_CONTACT,
        })

        ctx.update(product_data)

        # pk = self.kwargs.get('pk')
        # product = self.product_obj
        # ctx['product'] = product
        # ctx['num_jobs_url'] = self.get_jobs_url(product)
        # if product:
        #     ctx.update(self.get_breadcrumbs(product, self.category))
        # ctx.update(self.solar_info(self.sqs))
        # if product.is_course:
        #     ctx.update(self.solar_program_structure(self.sqs))
        # ctx.update(self.solar_faq(self.sqs))
        # ctx.update(self.get_recommendation(product))
        # ctx.update(self.get_reviews(product, 1))
        # country_choices = [(m.phone, m.name) for m in
        #                    Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
        # initial_country = Country.objects.filter(phone='91')[0].phone
        # ctx.update({
        #     'country_choices': country_choices,
        #     'initial_country': initial_country,
        # })
        # if self.sqs.pPc == 'course':
        #     ctx.update(json.loads(self.sqs.pPOP))
        #     pvrs_data = json.loads(self.sqs.pVrs)
        #     try:
        #         selected_var = pvrs_data['var_list'][0]
        #     except Exception as e:
        #         selected_var = None
        #     ctx.update({'selected_var': selected_var})
        #     ctx.update(pvrs_data)
        #     ctx['canonical_url'] = self.product_obj.get_canonical_url()
        # else:
        #     if ctx.get('prd_exp', None) in ['EP', 'FP']:
        #         pPOP = json.loads(self.sqs.pPOP)
        #         pid = None
        #         for pop in pPOP.get('pop_list'):
        #             if pop.get('experience', '') == 'FR' and ctx.get('prd_exp', None) == 'FP':
        #                 pid = pop.get('id')
        #                 break
        #             elif pop.get('experience', '') == 'SP' and ctx.get('prd_exp', None) == 'EP':
        #                 pid = pop.get('id')
        #                 break
        #         try:
        #             if pid:
        #                 pid = Product.objects.get(pk=pid)
        #                 ctx['canonical_url'] = pid.get_canonical_url()
        #             else:
        #                 ctx['canonical_url'] = self.product_obj.get_canonical_url()      
        #         except:
        #             ctx['canonical_url'] = self.product_obj.get_canonical_url()
        #             logging.getLogger('error_log').error(
        #                 "%(msg)s : %(err)s" % {'msg': 'Canonical Url ERROR', 'err': e})
        #     else:
        #         ctx['canonical_url'] = self.product_obj.get_canonical_url()
        #     ctx.update(json.loads(self.sqs.pPOP))
        #     pvrs_data = json.loads(self.sqs.pVrs)
        #     ctx.update(pvrs_data)
        # if self.is_combos(self.sqs):
        #     ctx.update(json.loads(self.sqs.pCmbs))

        # ctx.update(json.loads(self.sqs.pFBT))
        # get_fakeprice = self.get_solar_fakeprice(
        #     self.sqs.pPinb, self.sqs.pPfinb)

        # ctx.update(self.getSelectedProduct_solr(self.sqs))
        # # ctx.update(self.getSelectedProductPrice_solr(self.sqs))

        # try:
        #     widget_obj = DetailPageWidget.objects.get(
        #         content_type__model='Product', listid__contains=pk)
        #     widget_objs = widget_obj.widget.iw.indexcolumn_set.filter(
        #         column=1)
        # except DetailPageWidget.DoesNotExist:
        #     widget_objs = None
        #     widget_obj = None
        # ctx['domain_name'] = '{}//{}'.format(settings.SITE_PROTOCOL, settings.SITE_DOMAIN)
        # ctx.update({'sqs': self.sqs})
        # ctx.update({'get_fakeprice': get_fakeprice})
        # ctx['meta'] = self.product_obj.as_meta(self.request)
        # ctx['meta']._url = ctx.get('canonical_url', '')
        # ctx['show_chat'] = True
        # ctx['amp'] = self.request.amp
        # ctx['widget_objs'] = widget_objs
        # ctx['widget_obj'] = widget_obj
        
        # ctx['linkedin_resume_services'] = settings.LINKEDIN_RESUME_PRODUCTS
        # navigation = True
        # if self.sqs.id in settings.LINKEDIN_RESUME_PRODUCTS:
        #     navigation = False
        # ctx['navigation'] = navigation
        return ctx

    def redirect_if_necessary(self, current_path, product):
        if self._enforce_paths:
            expected_path = product.pURL
            if expected_path != urlquote(current_path):
                return HttpResponsePermanentRedirect(expected_path)

    # def send_signal(self, request, response, product):
    #     self.view_signal.send(
    #         sender=self, product=product, user=request.user, request=request,
    #         response=response)

    def return_http404(self, sqs_obj):
        if sqs_obj.count() == 1:
            return False
        return True

    def get(self, request, **kwargs):
        pk = self.kwargs.get('pk')
        try:
            self.product_obj = Product.browsable.get(pk=pk)
        except Exception as e:
            logging.getLogger('error_log').error("404 on product detail.ID:{}".format(pk))
            raise Http404

        try:
            sqs = SearchQuerySet().filter(id=pk)
            self.sqs = sqs[0]
            if not self.sqs:
                raise Http404

            if self.sqs.id in settings.LINKEDIN_RESUME_PRODUCTS:
                linkedin_cid = settings.LINKEDIN_DICT.get('CLIENT_ID', None)
                token = request.GET.get('token', '')
                login_url = reverse('login') + '?next=' + request.get_full_path() + '&linkedin=true'
                if token and request.session.get('email'):
                    validate = LinkedinSeriviceMixin().validate_encrypted_key(
                        token=token,
                        email=request.session.get('email'),
                        prd=self.sqs.id)
                    if validate and linkedin_cid == request.session.get('linkedin_client_id', ''):
                        services = OrderItem.objects.filter(
                            order__status__in=[1, 3],
                            order__candidate_id=request.session.get('candidate_id'),
                            product__id__in=settings.LINKEDIN_RESUME_PRODUCTS)
                        if services.exists():
                            return HttpResponseRedirect(reverse('dashboard:dashboard'))
                    elif not validate and linkedin_cid == request.session.get('linkedin_client_id', ''):
                        request.session['linkedin_modal'] = 1
                        return HttpResponseRedirect('/')
                    elif validate and linkedin_cid != request.session.get('linkedin_client_id', ''):
                        request.session.flush()
                        return HttpResponseRedirect(login_url)
                    elif not validate:
                        request.session.flush()
                        return HttpResponseRedirect(login_url)

                elif token:
                    request.session.flush()
                    return HttpResponseRedirect(login_url)
                else:
                    request.session['linkedin_modal'] = 1
                    return HttpResponseRedirect('/')

        except Exception as e:
            logging.getLogger('error_log').error("SQS query error on product detail.ID:{}".format(pk))
            raise Http404

        if self.product_obj:
            self.category = self.product_obj.category_main

        redirection = self.redirect_if_necessary(request.path, self.sqs)
        if redirection is not None:
            return redirection
        return super(ProductDetailView, self).get(request, **kwargs)
        # self.send_signal(request, response, product)

# @Decorate(stop_browser_cache())
# class ProductDetailView(DetailView, ProductInformationMixin, CartMixin):
#     context_object_name = 'product'
#     http_method_names = ['get', 'post']

#     model = Product

#     def __init__(self, *args, **kwargs):
#         # _view_signal = product_viewed
#         self.category = None
#         # # Whether to redirect to the URL with the right path
#         self._enforce_paths = True
#         # # Whether to redirect child products to their parent's URL
#         self._enforce_parent = True

#         super(ProductDetailView, self).__init__(*args, **kwargs)

#     def get_template_names(self):
#         return ['shop/detail1.html']

#     def get_object(self, queryset=None):
#         if hasattr(self, 'object'):
#             return self.object
#         else:
#             return super(ProductDetailView, self).get_object(queryset)

#     def get_context_data(self, **kwargs):
#         ctx = super(ProductDetailView, self).get_context_data(**kwargs)
#         sqs = SearchQuerySet().filter(id=11)[0]
#         product = self.object
#         category = self.category
#         ctx.update(self.get_breadcrumbs(product, category))
#         ctx.update(self.get_program_structure(product))
#         ctx.update(self.solar_program_structure(sqs))
#         ctx.update(self.get_faq(product))
#         ctx.update(self.get_recommendation(product))
#         ctx.update(self.get_reviews(product, 1))
#         if product.is_course:
#             ctx.update(self.get_other_provider(product, category))
#         else:
#             ctx.update(self.get_other_package(product, category))
#         if product.type_product == 1:
#             ctx.update(self.get_variation(product))
#         if product.is_combo:
#             ctx.update(self.get_combos(product))
#         ctx.update(self.get_frequentlybought(product, category))
#         ctx.update(self.getSelectedProduct(product))
#         ctx.update(self.getSelectedProductPrice(product))
#         return ctx

#     # def send_signal(self, request, response, product):
#     #     self.view_signal.send(
#     #         sender=self, product=product, user=request.user, request=request,
#     #         response=response)

#     def redirect_if_necessary(self, current_path, product, cat_slug=None):
#         if self._enforce_paths:
#             expected_path = product.get_absolute_url(cat_slug)
#             if expected_path != urlquote(current_path):
#                 return HttpResponsePermanentRedirect(expected_path)
    
#     def return_http404(self, product):
#         if not product:
#             return True
#         if not product.active:
#             return True
#         if not self.category:
#             return True
#         if product.var_child:
#             return True
#         if product.is_virtual:
#             return True
#         return False
    
#     def get(self, request, **kwargs):
#         self.object = product = self.get_object()
#         if product:
#             self.category = category = product.verify_category(kwargs.get('cat_slug', None))

#         HTTP404 = self.return_http404(product)
#         if HTTP404:
#             raise Http404
#         redirection = self.redirect_if_necessary(
#             request.path, product, category)
#         if redirection is not None:
#             return redirection

#         response = super(ProductDetailView, self).get(request, **kwargs)
#         # self.send_signal(request, response, product)
#         return response


class ProductReviewListView(ListView, ProductInformationMixin):
    template_name = 'shop/partials/reviews.html'
    model = Review
    paginate_by = 5
    _product = None
    _page_kwarg = 1

    def dispatch(self, request, *args, **kwargs):
        self._product = None
        self._page_kwarg = 1
        return super(
            self.__class__, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Review.objects.none()

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.template_name = 'shop/partials/review_snippet.html'
            self._page_kwarg = self.request.GET.get('pg', 1)
            try:
                self._product = Product.objects.get(
                    pk=self.kwargs['product_pk'])
            except Exception as e:
                logging.getLogger('error_log').error('unable to get product object %s'%str(e))
                pass

            if self._product:
                return super(self.__class__, self).get(request, args, **kwargs)
            else:
                return HttpResponseForbidden()
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['product'] = self._product
        context.update(self.get_reviews(
            self._product, self._page_kwarg))
        return context


class ProductReviewCreateView(CreateView):

    def __init__(self):
        self.oi = None
        self.candidate_id = None
        self.rating = None
        self.sel_rat = None


    def post(self, request, *args, **kwargs):
        """
        This method create reviews for individual product.
        """
        self.candidate_id = request.session.get('candidate_id', None)
        self.product_pk = request.POST.get('product_id')
        self.product = None
        data = {
            "display_message": 'Thank you for posting a review. It will be displayed on the site after moderation',
            "success": False
        }
        review_form = ReviewForm(request.POST)
        if request.is_ajax() and self.product_pk and self.candidate_id:
            if review_form.is_valid():
                try:
                    self.product = Product.objects.get(pk=self.product_pk)
                    contenttype_obj = ContentType.objects.get_for_model(self.product)
                    review_obj = Review.objects.filter(
                        object_id=self.product.id,
                        content_type=contenttype_obj,
                        user_id=self.candidate_id
                    )
                    review = request.POST.get('review', '').strip()
                    rating = int(request.POST.get('rating', 1))
                    title = request.POST.get('title', '')

                    if rating and not review_obj and self.product:
                        name = ''
                        if request.session.get('first_name'):
                            name += request.session.get('first_name')
                        if request.session.get('last_name'):
                            name += ' ' + request.session.get('last_name')
                        product = self.product
                        email = request.session.get('email')
                        content_type = ContentType.objects.get(app_label="shop", model="product")
                        review_obj = Review.objects.create(
                            content_type=content_type,
                            object_id=product.id,
                            user_name=name,
                            user_email=email,
                            user_id=self.candidate_id,
                            content=review,
                            average_rating=rating,
                            title=title
                        )
                        extra_content_obj = ContentType.objects.get(app_label="shop", model="product")

                        review_obj.extra_content_type = extra_content_obj
                        review_obj.extra_object_id = self.product.id
                        review_obj.save()
                        data['success'] = True
                    else:
                        if review_obj:
                            data['display_message'] = "You have already submitted feedback"
                        else:
                            data['display_message'] = "select valid input for feedback"

                except Exception as e:
                    logging.getLogger('error_log').error(str(e))

                    data['display_message'] = "select valid input for feedback"
                    data['success'] = False
                return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                data['display_message'] = None
                return HttpResponse(json.dumps(review_form.errors), content_type="application/json")
        else:
            return HttpResponseForbidden()


class ProductReviewEditView(View):

    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        product_pk = self.request.POST.get('product_id')
        candidate_id = request.session.get('candidate_id', None)
        data = {
            "display_message": 'Thank you for posting a review. It will be displayed on the site after moderation',
            "success": False
        }
        review_form = ReviewForm(request.POST)
        if self.request.is_ajax() and candidate_id and product_pk:
            if review_form.is_valid():
                review = request.POST.get('review', '').strip()
                rating = int(request.POST.get('rating', 1))
                title = request.POST.get('title','').strip()
                try:
                    product_obj = Product.objects.get(pk=product_pk)
                    contenttype_obj = ContentType.objects.get_for_model(product_obj)
                    review_obj = Review.objects.filter(object_id=product_obj.id, content_type=contenttype_obj, user_id=candidate_id).first()

                    # Setting status back to 0 for adding this review again to moderation list
                    if review_obj and review_obj.user_id == candidate_id:
                        review_obj.content = review
                        review_obj.average_rating = rating
                        review_obj.status = 0
                        review_obj.title = title
                        review_obj.created = timezone.now()
                        review_obj.save()
                        data['success'] = True
                    else:
                        data['display_message'] = "Not Allowed"
                except Exception as e:
                    logging.getLogger('error_log').error("%s" % str(e))
            else:
                data = review_form.errors

        return HttpResponse(json.dumps(data), content_type="application/json")


class CourseCatalogueView(TemplateView, MetadataMixin, CourseCatalogueMixin):
    template_name = 'shop/course-catalogue.html'
    use_title_tag = True
    use_og = True
    use_twitter = True
    twitter_site = True
    twitter_card = True
    
    def get_meta_title(self, context=None):
        return 'Online Courses and Certifications : Free Online Education'

    def get_meta_description(self, context=None):
        return 'Join India\'s Largest E-Learning Online Courses and Education Platform. Get Certifications in Top Courses under Finance, IT, Analytics, Marketing and more'
    
    def get_meta_url(self, context=None):
        return settings.MAIN_DOMAIN_PREFIX + '/online-courses.html'

    def get_testimonials(self):
        testimonials = Testimonial.objects.filter(
            page=3, is_active=True)
        testimonials = testimonials[: 3]
        return {"testimonials": testimonials}

    def get_context_data(self, **kwargs):
        context = super(CourseCatalogueView, self).get_context_data(**kwargs)
        context['meta'] = self.get_meta(context=context)
        context.update(self.get_testimonials())
        if cache.get('course_catalogue'):
            context['course_dict'] = cache.get('course_catalogue')
        else:
            context['course_dict'] = self.get_course_catalogue_context()
        context.update({
            "meta_url": self.get_meta_url(),
            "meta_title": self.get_meta_title(),
            "meta_desc": self.get_meta_description(),
        })
        return context


class ProductDetailContent(View, ProductInformationMixin, CartMixin):

    def __init__(self):
        
        self.sqs_obj = None
        self.sqs_main = None
        self.product_obj = None
        self.product_main = None

    def get(self, request, *args, **kwargs):
        data = {'status': 0}
        if request.is_ajax():
            self.main_pk = self.request.GET.get('main_pk', None)
            self.obj_pk = self.request.GET.get('obj_pk', None)

            try:
                self.product_obj = Product.browsable.get(pk=self.obj_pk)
            except:
                logging.getLogger('error_log').error(
                    "Product is not browsable:product-id {}".format(
                        self.obj_pk))

            try:
                self.product_main = Product.browsable.get(pk=self.main_pk)
            except:
                logging.getLogger('error_log').error(
                    "Main Product is not browsable:product-id {}".format(
                        self.main_pk))

            try:
                sqs = SearchQuerySet().filter(id=self.obj_pk)
                self.sqs_obj = sqs[0]
            except:
                logging.getLogger('error_log').error(
                    "SQS query error on product detail.ID :{}".format(
                        self.obj_pk))

            try:
                sqs = SearchQuerySet().filter(id=self.main_pk)
                self.sqs_main = sqs[0]
            except:
                logging.getLogger('error_log').error(
                    "SQS query error on product detail.ID :{}".format(
                        self.main_pk))

            if self.sqs_obj and self.sqs_main and self.product_obj and self.product_main:
                product_data = self.get_product_detail_context(
                    self.product_obj, self.sqs_obj,
                    self.product_main, self.sqs_main)

                product_detail_content = render_to_string(
                    'shop/product-detail.html', product_data,
                    request=request)

                data.update({
                    'status': 1,
                    'url': self.product_obj.get_absolute_url(),
                    'detail_content': product_detail_content,
                    'title': self.product_obj.title,
                })

            return HttpResponse(json.dumps(data), content_type="application/json")
        return HttpResponseForbidden()
