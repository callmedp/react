# Python Core Import
import logging
import json
from datetime import datetime

# Django-Core Import
from django.core.cache import cache
from django.db.models import Count, Avg, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

# Inter-App Import
from core.library.haystack.query import SQS
from decimal import Decimal
from payment.tasks import make_logging_request, make_logging_sk_request
from crmapi.tasks import create_lead_crm
from haystack.query import SearchQuerySet
from wallet.models import ProductPoint
from review.models import Review
from homepage.models import Testimonial
from search.helpers import get_recommendations
from core.common import APIResponse
from shop.models import (Product, Skill)

# DRF Import
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

# Constant Import
from homepage.config import UNIVERSITY_COURSE
from crmapi.config import PRODUCT_SOURCE_MAPPING
from crmapi.models import UNIVERSITY_LEAD_SOURCE, DEFAULT_SLUG_SOURCE
from shop.choices import APPLICATION_PROCESS, BENEFITS, NEO_LEVEL_OG_IMAGES, SMS_URL_LIST, PRODUCT_TAG_CHOICES


# TODO
# 1. Redirect handling
# 2. more information need to be handled
# 3. Pluck out unwanted data
# 4. fixed variable part

class ProductInformationAPIMixin(object):
    """
    Product Mixin to fetch all the information from different
    objects and model and save it to the cache key to get the data
    more frequent
    """

    def get_solor_info(self, product):
        """
        Solar Info function will fetch all the information from Solar Queryset
        index on product
        """
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
        info['pTg'] = dict(PRODUCT_TAG_CHOICES).get(product.pTg)
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
        """
        Function will fetch the program structure of product
        i.e heading, content, ordering
        """
        structure = {
            'prd_program_struct': False,
            'chapter': False
        }
        chapter_list = product.chapter_product.filter(status=True)
        if chapter_list:
            structure.update({
                'prd_program_struct': False,
                'chapter': True,
                'chapter_list': list(chapter_list.values('heading', 'content', 'ordering'))
            })
            return structure

    def get_solar_program_structure(self, product):
        """
        Function will fetch the program structure of solar
        i.e heading, content, ordering
        """
        structure = json.loads(product.pPChs)
        return structure

    def get_faq(self, product):
        """
        Function will fetch the product faq added from product object
        """
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

    def get_solor_faq(self, product):
        """
        Function will fetch the product faq added from product object
        """
        structure = json.loads(product.pFAQs)
        return structure

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

    def is_combos(self, product):
        combos = json.loads(product.pCmbs)
        if combos['combo']:
            return True
        return False

    def get_combos(self, product):
        combo = {'combo': False}
        combos = product.childs.filter(active=True)
        if combo:
            combo.update({
                'combo': True,
                'combos': combos
            })

    def get_frequently_brought(self, product):
        """
        Function will Frequntly brought product based on the product
        """
        prd_fbt = {
            'prd_fbt': False
        }
        prd_fbt_list = product.related.filter(
            secondaryproduct__active=True,
            secondaryproduct__type_relation=1
        )
        if prd_fbt_list:
            prd_fbt.update({
                'prd_fbt': True,
                'prd_fbt_list': prd_fbt_list
            })
        return prd_fbt



    def get_reviews(self, product, page):
        """
        Function will get all the reviews given on the product
        May need to pluck it down
        """
        context = {}
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
            per_page = 3
            try:
                rv_paginator = Paginator(review_list, per_page)
                review_list = rv_paginator.page(page)
            except PageNotAnInteger:
                review_list = rv_paginator.page(1)
            except EmptyPage:
                review_list = rv_paginator.page(1)

            return {
                'prd_rv_total': rv_paginator.num_pages,
                'prd_rv_current_page': review_list.number,
                'prd_rv_has_next': review_list.has_next(),
                'prd_rv_has_prev': review_list.has_previous(),
                'prd_review_list': [
                    {'title': review.title, 'user_email': review.user_email, 'user_name:': review.user_name,
                     'average_rating': review.average_rating, 'rating': review.get_ratings(),
                     'created': review.created.strftime("%b %d, %Y")}
                    for review in review_list
                ]
            }
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
            return {
                'prd_rv_total': 0,
                'prd_review_list': [],
                'prd_rv_page': page
            }

    def get_sorted_products(self, pvrs_data):
        # Study Mode & Access Duration
        if pvrs_data.get('var_list'):
            sort_pvrs = sorted(pvrs_data.get('var_list'), key=lambda i: i['inr_price'])
            pvrs_data['var_list'] = sort_pvrs
        return pvrs_data

    def get_product_information(self, product, sqs, product_main, sqs_main):
        """
        Main function used to fetch and combine all the product data used in API
        study mode & duration
        """
        context = {}
        # context['product'] = product
        context['num_jobs_url'] = self.get_jobs_url(product)

        # Solar Product Info
        context.update(self.get_solor_info(sqs))

        if product.is_course or product.is_assesment:
            # Solar program structure
            context.update(self.get_solar_program_structure(sqs))

        # Solar FAQ
        context.update(self.get_solor_faq(sqs))

        if sqs.pPc == 'course':
            context.update(json.loads(sqs_main.pPOP))
            pvrs_data = json.loads(sqs.pVrs)
            # Create get_sorted_products
            pvrs_data = self.get_sorted_products(pvrs_data)
            try:
                selected_var = pvrs_data['var_list'][0]  # Study Mode
            except Exception:
                selected_var = None
            context.update({'selected_var': selected_var})
            context.update(pvrs_data)
            context['canonical_url'] = product.get_parent_canonical_url()

            if product.type_flow == 14:
                context['university_detail'] = json.loads(sqs.pUncdl[0])
                faculty = [f.faculty for f in
                           product.facultyproducts.all().select_related('faculty', 'faculty_institute')]
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
                    elif pop.get('experience', '') == 'SP' and context.get('prd_exp', None) == 'EP':
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

        if self.is_combos(sqs):
            context.update(json.loads(sqs.pCmbs))

        context.update(json.loads(sqs.pFBT))
        # update get fake price
        get_fake_price = 00

        context['domain_name'] = '{}//{}'.format(
            settings.SITE_PROTOCOL, settings.SITE_DOMAIN)
        if getattr(product, 'vendor', None):
            context.update({'prd_vendor_slug': product.vendor.slug})
        # context.update({'sqs': sqs})
        # context.update({'get_fakeprice': get_fakeprice})
        context['show_chat'] = True
        # context['product_main'] = product_main,
        # context['sqs_main'] = sqs_main
        context['prd_vendor_count'] = SQS().filter(pVid=product.vendor.id). \
            exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).count()
        return context

    def get_other_detail(self, product, sqs):
        """
        Other Detail like
        reviews, loggedin_status, redeem_test, redeem_options will be fetched from here
        """
        context = {}
        pk = product.pk
        context['is_logged_in'] = True if self.request.session.get('candidate_id') else False
        context['linkedin_resume_services'] = settings.LINKEDIN_RESUME_PRODUCTS
        context['redeem_test'] = False
        context['product_redeem_count'] = 0
        context['redeem_option'] = 'assessment'

        if self.request.session.get('candidate_id'):
            candidate_id = self.request.session.get('candidate_id', None)
            contenttype_obj = ContentType.objects.get_for_model(product)
            context['review_obj'] = Review.objects.filter(object_id=product.id, content_type=contenttype_obj,
                                                          user_id=candidate_id).first()
            # User_Reviews depicts if user already has a review for this product or not
            user_reviews = Review.objects.filter(content_type=contenttype_obj, object_id=pk, status__in=[0, 1],
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

    def get_product_detail_context(self, product, sqs, product_main, sqs_main):
        """
        Function using cache to get the data from redis if available else
        will summarise the data and save it to redis-server to used furthur
        """
        main_context = {}
        key = 'context_product_detail' + str(product.pk)
        useragent = self.request.META.get('HTTP_USER_AGENT', [])
        if cache.get(key) and 'facebookexternalhit' not in useragent:
            main_context.update(cache.get(key))
        else:
            data = self.get_product_information(product, sqs, product_main, sqs_main)
            main_context.update(data)
            cache.set(key, data, 60 * 60 * 4)
        main_context.update(self.get_other_detail(product, sqs))
        return main_context


class ProductDetailAPI(ProductInformationAPIMixin, APIView):
    permission_classes = (AllowAny,)

    def __init__(self):
        self.category = None
        self.product_obj = None
        self._enforce_paths = True
        self.sqs = None
        self.skill = False
        self.key = None
        self.cache_dict = {}

    def get_object(self, pid):
        try:
            return Product.objects.get(pk=pid)
        except Product.DoesNotExist:
            raise Http404

    def create_product_detail_leads(self, data_dict={}):
        if not data_dict:
            logging.getLogger('info_log').info('No data found')
            return
        from crmapi.models import UserQueries
        lead = UserQueries.objects.create(**data_dict)
        if not lead:
            logging.getLogger('info_log').info('user query not created')
            return

        create_lead_crm.apply_async(
            (lead.pk,), countdown=settings.PRODUCT_LEADCREATION_COUNTDOWN)
        return lead

    def maintain_tracking_info(self, product=None):
        if not product:
            return -1
        if product.sub_type_flow == 501:
            return 1
        if product.sub_type_flow == 503:
            return 2
        if product.sub_type_flow == 504:
            return 3
        if product.type_flow == 18:
            return 4
        if product.type_flow == 19:
            return 5
        if product.type_flow == 1:
            return 6
        if product.sub_type_flow == 502:
            return 7
        if product.type_flow == 16:
            return 8
        if product.type_flow == 2:
            return 9
        if product.type_flow == 17:
            return 11

    def get(self, request, *args, **kwargs):
        """
        API Get function to populate the product detail, function contains
        1. creating the product_lead_details
        2. storing the tracking information
        3. Managing the campaign availability
        4.
        """

        context = {}
        pid = self.request.GET.get('pid')
        tracking_id = request.GET.get('t_id', '')
        utm_campaign = request.GET.get('utm_campaign', '')
        trigger_point = request.GET.get('trigger_point', '')
        u_id = request.GET.get('u_id', request.session.get('u_id', ''))
        position = self.request.GET.get('position', -1)
        self.skill = self.request.session.get('skills_name', [])

        try:
            if not pid:
                return APIResponse(message='Product id is required', error=True, status=status.HTTP_400_BAD_REQUEST)

            if self.request.GET.get('lc') and self.request.session.get('candidate_id'):
                if not pid:
                    return
                prod = Product.objects.filter(id=pid).first()
                if not prod:
                    return

                lead_source = PRODUCT_SOURCE_MAPPING.get(
                    prod.product_class.slug, 0
                )
                slug_source = dict(DEFAULT_SLUG_SOURCE)
                utm_params = self.request.GET.get('utm', {})
                campaign_slug = self.request.GET.get('utm_content', slug_source.get(int(lead_source)))

                data_dict = {
                    'name': "{} {}".format(self.request.session.get('first_name', ''), self.request.session.get(
                        'last_name', '')),
                    'email': self.request.session.get('email', ''),
                    'phn_number': self.request.session.get('mobile_no', ''),
                    'product_id': prod.id,
                    'utm_parameter': json.dumps(utm_params),
                    'product': prod.name,
                    'lead_source': lead_source,
                    'path': request.path,
                    'campaign_slug': campaign_slug,
                }

                lead = self.create_product_detail_leads(data_dict)

                try:
                    self.request.session.update({'product_lead_dropout': lead.id})
                except:
                    logging.getLogger('error_log').error(
                        'error in updating session for product lead drop out {}'.format(data_dict))

            if tracking_id and self.request.session.get('candidate_id'):
                if not pid:
                    return
                prod = Product.objects.filter(id=pid).first()
                if not prod:
                    return
                request.session.update({
                    'tracking_product_id': prod.id,
                    'tracking_id': tracking_id,
                    'trigger_point': trigger_point,
                    'u_id': u_id,
                    'position': position,
                    'utm_campaign': utm_campaign
                })
                product_tracking_mapping_id = self.maintain_tracking_info(prod)
                if product_tracking_mapping_id != -1:
                    request.session.update(
                        {'product_tracking_mapping_id': product_tracking_mapping_id})

                if tracking_id and prod.id and product_tracking_mapping_id:
                    make_logging_request.delay(
                        prod.id, product_tracking_mapping_id, tracking_id, 'product_page', position, trigger_point, u_id,
                        utm_campaign, 2)

            elif self.request.session.get('candidate_id') and \
                    request.session.get('tracking_product_id') and \
                    request.session.get('tracking_id') and \
                    kwargs.get('pk') == request.session.get('tracking_product_id'):
                position = request.session.get('position', 1)
                utm_campaign = request.session.get('utm_campaign', '')
                trigger_point = request.session.get('trigger_point', '')
                u_id = request.session.get('u_id', '')
                r_p = request.session.get('referal_product', '')
                r_sp = request.session.get('referal_subproduct', '')
                popup_based_product = request.session.get('popup_based_product', '')
                make_logging_sk_request.delay(
                    request.session.get('tracking_product_id'), request.session.get('product_tracking_mapping_id'),
                    request.session.get('tracking_id'), 'product_page', position, trigger_point, u_id, utm_campaign, 2, r_p,
                    r_sp, popup_based_product)
            elif self.request.session.get('candidate_id') and \
                    request.session.get('tracking_id') and \
                    not request.session.get('tracking_product_id'):
                if not kwargs.get('pk', ''):
                    return
                prod = Product.objects.filter(id=kwargs.get('pk')).first()
                if not prod:
                    return
                request.session.update({'tracking_product_id': prod.id})
                product_tracking_mapping_id = self.maintain_tracking_info(
                    prod)
                if product_tracking_mapping_id != -1:
                    request.session.update(
                        {'product_tracking_mapping_id': product_tracking_mapping_id})

                tracking_id = request.session.get('tracking_id', '')
                trigger_point = request.session.get('trigger_point', '')
                u_id = request.session.get('u_id', '')
                position = self.request.session.get('position', 1)
                utm_campaign = self.request.session.get('utm_campaign', '')
                r_p = request.session.get('referal_product', '')
                r_sp = request.session.get('referal_subproduct', '')
                popup_based_product = request.session.get('popup_based_product', '')
                if tracking_id and prod.id and product_tracking_mapping_id:
                    make_logging_sk_request.delay(
                        prod.id, product_tracking_mapping_id, tracking_id, 'product_page', position, trigger_point, u_id,
                        utm_campaign, 2, r_p, r_sp, popup_based_product)

            elif self.request.session.get('candidate_id') and \
                    request.session.get('tracking_id') and \
                    request.session.get('product_tracking_mapping_id') == 10:
                if not kwargs.get('pk', ''):
                    return
                request.session.update({
                    'referal_product': request.session.get('product_tracking_mapping_id', ''),
                    'referal_subproduct': request.session.get('tracking_product_id', '')
                })
                prod = Product.objects.filter(id=kwargs.get('pk')).first()
                if not prod:
                    return
                request.session.update({'tracking_product_id': prod.id})
                product_tracking_mapping_id = self.maintain_tracking_info(
                    prod)
                if product_tracking_mapping_id != -1:
                    request.session.update(
                        {'product_tracking_mapping_id': product_tracking_mapping_id})

                tracking_id = request.session.get('tracking_id', '')
                trigger_point = request.session.get('trigger_point', '')
                u_id = request.session.get('u_id', '')
                position = self.request.session.get('position', 1)
                utm_campaign = self.request.session.get('utm_campaign', '')
                r_p = request.session.get('referal_product', '')
                r_sp = request.session.get('referal_subproduct', '')
                if tracking_id and prod.id and product_tracking_mapping_id:
                    make_logging_sk_request.delay(
                        prod.id, product_tracking_mapping_id, tracking_id, 'product_page', position, trigger_point, u_id,
                        utm_campaign, 2, r_p, r_sp)

            self.prd_key = 'detail_db_product_' + pid
            self.prd_solr_key = 'detail_solr_product_' + pid
            cache_dbprd_maping = cache.get(self.prd_key, "")
            if cache_dbprd_maping:
                self.product_obj = cache_dbprd_maping
            else:
                self.product_obj = Product.browsable.filter(pk=pid).first()
                cache.set(self.prd_key, self.product_obj, 60 * 60 * 4)
                if not self.product_obj:
                    return APIResponse(message='Product Not Found', error=True, status=status.HTTP_404_NOT_FOUND)

            cache_slrprd_maping = cache.get(self.prd_solr_key, "")

            if cache_slrprd_maping:
                self.sqs = cache_slrprd_maping
            else:
                sqs = SearchQuerySet().filter(id=pid)
                if sqs:
                    self.sqs = sqs[0]
                    cache.set(self.prd_solr_key, self.sqs, 60 * 60 * 4)
                else:
                    return APIResponse(message='Product Not Found', error=True, status=status.HTTP_404_NOT_FOUND)

            # if (self.sqs.pPc == 'writing' or self.sqs.pPc == 'service' or self.sqs.pPc == 'other') and self.sqs.pTP not in [2, 4] and self.sqs.pTF not in [16, 2]:
            #     pass
            #     # redirect to resume shine (need to handle)
            #     # resume_shine_redirection = self.redirect_for_resume_shine(path_info)
            #     # return resume_shine_redirection
            #
            # if self.sqs.id in settings.LINKEDIN_RESUME_PRODUCTS:
            #     linkedin_cid = settings.LINKEDIN_DICT.get('CLIENT_ID', None)
            #     token = request.GET.get('token', '')
            #     login_url = reverse('login') + '?next=' + \
            #                 request.get_full_path() + '&linkedin=true'
            #     if token and request.session.get('email'):
            #         validate = LinkedinSeriviceMixin().validate_encrypted_key(
            #             token=token,
            #             email=request.session.get('email'),
            #             prd=self.sqs.id)
            #     if validate and linkedin_cid == request.session.get('linkedin_client_id', ''):
            #         services = OrderItem.objects.filter(
            #             order__status__in=[1, 3],
            #             order__candidate_id=request.session.get(
            #                 'candidate_id'),
            #             product__id__in=settings.LINKEDIN_RESUME_PRODUCTS)
            #         if services.exists():
            #             return APIResponse(message='Redirect to dashboard')
            #     elif not validate and linkedin_cid == request.session.get('linkedin_client_id', ''):
            #         request.session['linkedin_modal'] = 1
            #         return APIResponse(message='Redirect to homepage')
            #     elif validate and linkedin_cid != request.session.get('linkedin_client_id', ''):
            #         request.session.flush()
            #         return APIResponse(message='Redirect', data=login_url)
            #     elif not validate:
            #         request.session.flush()
            #         return APIResponse(message='Redirect', data=login_url)
            #
            #     elif token:
            #         request.session.flush()
            #         return APIResponse(message='Redirect', data=login_url)
            #     else:
            #         request.session['linkedin_modal'] = 1
            #         return APIResponse(message='Redirect', data='/')

            if not self.skill and self.product_obj.type_flow == 2:
                self.skill = self.product_obj.productskills.filter(skill__active=True).values_list('skill__name',
                                                                                                   flat=True)[:10]
            self.skill == ",".join(self.skill)

            product_data = self.get_product_detail_context(
                self.product_obj, self.sqs,
                self.product_obj, self.sqs
            )

            context.update({
                'product_detail': product_data,
                'skill': self.skill,
                "ggn_contact_full": settings.GGN_CONTACT_FULL,
                "ggn_contact": settings.GGN_CONTACT,
                'shine_api_url': settings.SHINE_API_URL,
                'tracking_product_id': self.request.session.get('tracking_product_id', ''),
                'product_tracking_mapping_id': self.request.session.get('product_tracking_mapping_id', ''),
                'tracking_id': self.request.session.get('tracking_id', ''),
                'trigger_point': self.request.session.get('trigger_point', ''),
                'u_id': self.request.session.get('u_id', ''),
                'position': self.request.session.get('position', 1),
                'utm_campaign': self.request.session.get('utm_campaign', ''),
                'product_id': self.product_obj and self.product_obj.id,
                'referal_product': self.request.session.get('referal_product', ''),
                'referal_subproduct': self.request.session.get('referal_subproduct'),
                'popup_based_product': self.request.session.get('popup_based_product', '')
            })
            return APIResponse(message='Product fetched successfully', data=context)
        except Exception as e:
            logging.getLogger('error_log').error('Product fetch error with id {} and error is {}'.format(pid, str(e)))
            return APIResponse(message='Something went wrong', error=True, status=status.HTTP_400_BAD_REQUEST)


class ProductReviewAPI(ProductInformationAPIMixin, APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        """
        API to return the all reviews related to product
        """
        pid = self.request.GET.get('pid')
        page = self.request.GET.get('page')
        context = {}

        if not pid:
            return APIResponse(message='Product id data is required', status=status.HTTP_400_BAD_REQUEST)

        try:
            prd_key = 'detail_db_product' + pid
            cache_dbprd_maping = cache.get(prd_key, "")
            if cache_dbprd_maping:
                product_obj = cache_dbprd_maping
            else:
                product_obj = Product.browsable.filter(pk=pid).first()
                cache.set(prd_key, product_obj, 60 * 60 * 4)
                if not product_obj:
                    return APIResponse(message='Product Not found', error=True, status=status.HTTP_404_NOT_FOUND)

            context.update({'prd_reviews': self.get_reviews(product_obj, page)})

            return APIResponse(data=context, message='Review fetched successfully', status=status.HTTP_200_OK)
        except Exception as e:
            logging.getLogger('error_log').error('Product fetch error with id {} and error is {}'.format(pid, str(e)))
            return APIResponse(message='Something went wrong', error=True, status=status.HTTP_400_BAD_REQUEST)
