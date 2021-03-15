# Python Core Import
import logging
from datetime import datetime

# Django-Core Import
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator

# Inter-App Import
from core.library.haystack.query import SQS
from wallet.models import ProductPoint
from review.models import Review
from homepage.models import Testimonial
from search.helpers import get_recommendations
from core.common import APIResponse
from shop.views import ProductInformationMixin
from shop.models import (Product, Skill)
from .serializers import (
    ProductDetailSerializer)

# DRF Import
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

# Constant Import
from homepage.config import UNIVERSITY_COURSE
from crmapi.models import UNIVERSITY_LEAD_SOURCE, DEFAULT_SLUG_SOURCE
from shop.choices import APPLICATION_PROCESS, BENEFITS, NEO_LEVEL_OG_IMAGES, SMS_URL_LIST

class ProductInformationAPIMixin(object):

    def get_solor_info(self, product):
        info = {}
        info['prd_img'] = product.pImg
        info['prd_img_alt'] = product.pImA
        info['prd_img_bg'] = product.pIBg
        info['prd_H1'] = product.pHd if product.pHd else product.pNm
        if product.pTF == 16:
            info['prd_about'] = product.pAbx
        else:
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
        elif product.pPc == 'assessment':
            info['prd_service'] = 'assessment'
        else:
            info['prd_service'] = 'other'
        info['prd_product'] = product.pTP
        info['prd_exp'] = product.pEX

        if product.pTF == 5:
            info['prd_dur'] = product.pDM[0] if product.pDM else ''

        if product.pTF == 16 and product.pAsft:
            info['prd_asft'] = eval(product.pAsft[0])
        return info

    def get_program_structure(self, product):
        structure = {
            'prd_program_struct': False,
            'chapter': False
        }
        chapter_list = product.chapter_product.filter(status=True)
        if chapter_list:
            structure.update({
                'prd_program_struct': False,
                'chapter': True,
                'chapter_list': chapter_list
            })
            return structure

    def get_faq(self, product):
        structure = {
            'prd_faq': False
        }
        faqs = product.faqs.filter(productfaqs__active=True, status=2).order_by('productfaqs__question_order')
        if faqs:
            structure.update({
                'prd_faq': True,
                'faq_list': faqs
            })
            return structure

    def get_jobs_url(self, product):
        job_url = 'https://www.shine.com/job-search/{}-jobs'.format(product.slug) \
            if product.slug else None
        return job_url

    def get_recommendation(self, product):
        recommendation = {
            'prd_recommend': False
        }
        rcourses = get_recommendations(
            self.request.session.get('func_area', None),
            self.request.session.get('skils', None)
        )
        if rcourses:
            rcourses = rcourses.exclude(id=product.id)
            rcourses = rcourses[:6]
        if rcourses:
            recommendation.update({
                'prd_recommend': True,
                'recommended_products': rcourses
            })
            return recommendation

    def get_combos(self, product):
        combo = { 'combo': False }
        combos = product.childs.filter(active=True)
        if combo:
            combo.update({
                'combo': True,
                'combos': combos
            })

    def get_frequently_brought(self, product):
        prd_fbt = {
            'prd_fbt': False
        }
        prd_fbt_list = product.related.filter(
            secondaryproduct__active = True,
            secondaryproduct__type_relation=1
        )
        if prd_fbt_list:
            prd_fbt.update({
                'prd_fbt': True,
                'prd_fbt_list': prd_fbt_list
            })
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

    def get_product_information(self, product, sqs, product_main, sqs_main):
        context = {}
        context['product'] = product
        context['num_jobs_url'] = self.get_jobs_url(product)

        # Solar Product Info
        context.update(self.get_solor_info(sqs))

        if product.is_course or product.is_assesment:
            # Solar program structure
            context.update(self.get_program_structure(sqs))

        # Solar FAQ
        context.update(self.get_faq(sqs))

        import json
        if sqs.pPc == 'course':
            context.update(json.loads(sqs_main.pPOP))
            pvrs_data = json.loads(sqs.pVrs)
            # Create get_sorted_products
            pvrs_data = self.get_sorted_products(pvrs_data)

            context['canonical_url'] = product.get_parent_canonical_url()

            if product.type_flow == 14:
                context['university_detail'] = json.loads(sqs.pUncdl[0])
                faculty = [f.faculty for f in product.facultyproducts.all().select_related('faculty', 'faculty_institute')]
                context['faculty'] = [faculty[i:i + 2] for i in range(0, len(faculty), 2)]
                context['institute'] = product.category_main
                app_process = context['university_detail']['app_process']
                context['university_detail']['app_process'] = [
                    APPLICATION_PROCESS.get(proc) for proc in app_process]
                app_process = context['university_detail']['benefits']
                context['university_detail']['benefits'] = [
                    BENEFITS.get(proc) for proc in app_process]
                context['university_testimonial'] = Testimonial.objects.filter(
                    page=UNIVERSITY_COURSE, object_id=product.pk
                )
                product['lead_source'] = UNIVERSITY_LEAD_SOURCE
        else:
            if context.get('prd_exp', None) in ['EP', 'FP']:
                pPOP = json.loads(sqs_main.pPOP)
                pid = None
                for pop in pPOP.get('pop_list'):
                    if pop.get('experience', '') == 'FR' and context.get('prd_exp', None) == 'FP':
                        pid = pop.get('id')
                        break
                    elif pop.get('experience', '') == 'SP' and ctx.get('prd_exp', None) == 'EP':
                        pid = pop.get('id')
                        break
                try:
                    if pid:
                        pid = Product.objects.get(pk=pid)
                        context['canonical_url'] = pid.get_parent_canonical_url()
                    else:
                        context['canonical_url'] = product.get_parent_canonical_url()
                except Exception as e:
                    context['canonical_url'] = product.get_parent_canonical_url()
                    logging.getLogger('error_log').error(
                        "%(msg)s : %(err)s" % {'msg': 'Canonical Url ERROR', 'err': e})
            else:
                context['canonical_url'] = product.get_parent_canonical_url()
            context.update(json.loads(sqs_main.pPOP))
            pvrs_data = json.loads(sqs.pVrs)
            pvrs_data = self.get_sorted_products(pvrs_data)
            context.update(pvrs_data)

        if self.get_combos(sqs):
            context.update(json.loads(sqs.pCmbs))

        context.update(json.loads(sqs.pFBT))
        # update get fake price
        get_fake_price = 00

        context['domain_name'] = '{}//{}'.format(
            settings.SITE_PROTOCOL, settings.SITE_DOMAIN)
        if getattr(product, 'vendor', None):
            context.update({'prd_vendor_slug': product.vendor.slug})
        context.update({'sqs': sqs})
        # context.update({'get_fakeprice': get_fakeprice})
        context['meta'] = product.as_meta(self.request)
        context['meta']._url = context.get('canonical_url', '')
        context['show_chat'] = True
        # context['product_main'] = product_main,
        # context['sqs_main'] = sqs_main
        context['prd_vendor_count'] = SQS().filter(pVid=product.vendor.id). \
            exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).count()
        return context

    def get_other_detail(self, product, sqs):
        context = {}
        pk = product.pk
        context.update(self.get_reviews(product, 1))
        context['is_logged_in'] = True if self.request.session.get('candidate_id') else False
        context['linkedin_resume_services'] = settings.LINKEDIN_RESUME_PRODUCTS
        context['redeem_test'] = False
        context['product_redeem_count'] = 0
        context['redeem_option'] = 'assessment'

        if self.request.session.get('candidate_id'):
            candidate_id = self.request.session.get('candidate_id', None)
            contenttype_obj = ContentType.objects.get_for_model(product)
            context['review_obj'] = Review.objects.filter(object_id=product.id, content_type=contenttype_obj, user_id=candidate_id).first()
            # User_Reviews depicts if user already has a review for this product or not
            user_reviews = Review.objects.filter(content_type=contenttype_obj, object_id=pk, status__in=[0,1],
                                                 user_id=candidate_id).count()
            context['user_reviews'] = True if user_reviews else False

            redeem_option = product.attr.get_attribute_by_name('redeem_option')
            attr_value = product.attr.get_value_by_attribute(redeem_option)

            if not attr_value:
                code = None
            else:
                code = attr_value.value or None

            if code:
                product_point = ProductPoint.objects.filter(candidate_id=candidate_id).first()

                if product_point:
                    redeem_options = eval(product_point.redeem_options)

                    required_obj = [
                        option for option in redeem_options if option['type'] == code
                    ]
                    required_obj = required_obj[0]
                    product_redeem_count = required_obj['product_redeem_count']
                    days = required_obj['product_validity_in_days'] or 0
                    timestamp = required_obj['purchased_at'] or 0
                    days_diff = datetime.now() - datetime.fromtimestamp(int(timestamp))
                    if days_diff.days < days and product_redeem_count != 0:
                        context['redeem_test'] = True
                        context['product_redeem_count'] = product_redeem_count
                        context['redeem_option'] = code
        navigation = True

        if sqs.id in settings.LINKEDIN_RESUME_PRODUCTS:
            navigation = False
        context['navigation'] = navigation
        return context


class ProductDetailAPI(ProductInformationMixin, APIView):
    permission_classes = (AllowAny,)
    serializer_class = ProductDetailSerializer

    def get_object(self, pid):
        try:
            return Product.objects.get(pk=pid)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        pid = self.request.GET.get('pid')
        slug = self.request.GET.get('slug')
        user = self.request.user

        product = self.get_object(pid)

        serializer_obj = ProductDetailSerializer(product)

        return APIResponse(data=serializer_obj.data)
