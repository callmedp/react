# Python Core Import
import logging

# Django-Core Import
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator

# Inter-App Import
from review.models import Review
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
