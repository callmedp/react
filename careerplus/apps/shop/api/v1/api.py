# Python Core Import
import logging
import json
from datetime import datetime
from django.utils import timezone
from decimal import Decimal
from collections import OrderedDict

# Django-Core Import
from django.core.cache import cache
from django.db.models import Count, Avg, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.conf import settings
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

# Inter-App Import
from .tasks import create_product_review_task
from core.library.haystack.query import SQS
from shop.models import Category, SubHeaderCategory
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
from shop.choices import APPLICATION_PROCESS, BENEFITS, NEO_LEVEL_OG_IMAGES, SMS_URL_LIST, PRODUCT_TAG_CHOICES, \
                        STUDY_MODE, COURSE_TYPE_DICT, COURSE_LEVEL_DICT, DURATION_DICT


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

    def get_solar_fakeprice(self, inr_price, fake_inr_price):
        if inr_price is not None:
            inr_price = inr_price
            fake_inr_price = fake_inr_price
            if fake_inr_price > Decimal('0.00'):
                diff = float(fake_inr_price) - float(inr_price)
                percent_diff = round((diff / float(fake_inr_price)) * 100, 0)
                return (round(fake_inr_price, 0), percent_diff)
        return None

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
        info['pTF'] = product.pTF
        info['pTg'] = dict(PRODUCT_TAG_CHOICES).get(product.pTg)
        info['prd_vendor_img'] = product.pVi
        # info['prd_vendor_img_alt'] = product.vendor.image_alt
        info['pPv'] = product.pPv
        info['prd_rating_star'] = product.pStar
        info['prd_video'] = product.pvurl
        info['start_price'] = product.pPinb
        info['pPinb'] = product.pPinb
        info['pPfinb'] = product.pPfinb
        info['pUPC'] = product.pUPC

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
        combo = {'combo': False}
        combos = json.loads(product.pCmbs)
        if combos['combo']:
            combo.update({ 'combo': True, 'combo_list': combos['combo_list'] })
            return combo
        return combo

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

    def get_delivery_flow(self, pTF):
        """
        Return data of how it works
        """
        context = {}
        if pTF == 1 or pTF == 12 or pTF == 13:
            context.update({
                'main_heading': 'How to begin',
                'articles': [
                    {
                        'heading': 'Upload Resume',
                        'article': 'Place order and upload your initial resume'
                    },
                    {
                        'heading': 'We Contact',
                        'article': 'Our resume expert will contact you for discussion'
                    },
                    {
                        'heading': 'Receive Draft',
                        'article': 'Receive 1st draft and give feedback to the expert'
                    },
                    {
                        'heading': 'Download Final Resume',
                        'article': 'Download your finalized professional resume'
                    }
                ]
            })
        if pTF == 2:
            # Courses
            context.update({
                'main_heading': 'How to begin',
                'articles': [
                    {
                        'heading': 'Place Order',
                        'article': 'Place your order'
                    },
                    {
                        'heading': 'Get Your Study Material',
                        'article': 'Recieve online access/study material from course provider'
                    },
                    {
                        'heading': 'Start Learning',
                        'article': 'Access the material and start learning'
                    },
                    {
                        'heading': 'Go for Exam',
                        'article': 'Appear for exam - Get Certified'
                    }
                ]
            })
        if pTF == 3:
            # Resume Critique
            context.update({
                'main_heading': 'How to begin',
                'articles': [
                    {
                        'heading': 'Introduce yourself',
                        'article': 'Place order and upload your initial resume'
                    },
                    {
                        'heading': 'We Update',
                        'article': 'Our resume expert will evaluate your resume'
                    },
                    {
                        'heading': 'Get Feedback',
                        'article': 'Receive feedback from resume expert'
                    },
                    {
                        'heading': 'Apply Feedback',
                        'article': 'Apply feedback to develop the best resume yourself'
                    }
                ]
            })
        if pTF == 4:
            # International Profile update
            context.update({
                'main_heading': 'How to begin',
                'articles': [
                    {
                        'heading': 'Introduce yourself',
                        'article': 'Place order and upload your resume'
                    },
                    {
                        'heading': 'We Update',
                        'article': 'Our expert will update your profile'
                    },
                    {
                        'heading': 'Profile Access',
                        'article': 'Start accessing your profile'
                    },
                    {
                        'heading': 'Increase Chances of Jobs',
                        'article': 'Increase your chances of getting relevant job matches'
                    }
                ]
            })
        if pTF == 5:
            # Featured profile
            context.update({
                'main_heading': 'How to begin',
                'articles': [
                    {
                        'heading': 'Introduce yourself',
                        'article': 'Place order and upload your resume'
                    },
                    {
                        'heading': 'We update',
                        'article': 'Our expert will update your profile'
                    },
                    {
                        'heading': 'Featured',
                        'article': 'Get featured on shine'
                    },
                    {
                        'heading': 'View',
                        'article': 'Get 10x recruiter views'
                    }
                ]
            })
        if pTF == 6:
            # IDFY/Assessment reports
            context.update({
                'main_heading': 'How to begin',
                'articles': [
                    {
                        'heading': 'Order',
                        'article': 'Place your order'
                    },
                    {
                        'heading': 'Update Details',
                        'article': 'Update your details on partner site'
                    },
                    {
                        'heading': 'Verify',
                        'article': 'Verification process by the team'
                    },
                    {
                        'heading': 'Download',
                        'article': 'Download Assessment report'
                    }
                ]
            })
        if pTF == 7 or pTF == 15:
            # Resume Booster
            context.update({
                'main_heading': 'How to begin',
                'articles': [
                    {
                        'heading': 'Order',
                        'article': 'Place your order'
                    },
                    {
                        'heading': 'Upload',
                        'article': 'Upload resume'
                    },
                    {
                        'heading': 'Resume Shared',
                        'article': 'Resume shared with 1000+ Recruiters'
                    },
                    {
                        'heading': 'Get Calls',
                        'article': 'Increase chances of getting Interview Calls'
                    }
                ]
            })
        if pTF == 9:
            # RoundOne
            context.update({
                'main_heading': 'How to begin',
                'articles': [
                    {
                        'heading': 'Order',
                        'article': 'Place your order'
                    },
                    {
                        'heading': 'Apply',
                        'article': 'Apply on relation jobs'
                    },
                    {
                        'heading': 'Talk',
                        'article': 'Talk to referrals'
                    },
                    {
                        'heading': 'Get Calls',
                        'article': 'Get an interview call'
                    }
                ]
            })
        if pTF == 10:
            # Courses study Mate
            context.update({
                'main_heading': 'How to begin',
                'articles': [
                    {
                        'heading': 'Order',
                        'article': 'Place your order'
                    },
                    {
                        'heading': 'Assessment',
                        'article': 'Give assessment to start your course'
                    },
                    {
                        'heading': 'Learn',
                        'article': 'Learn from best educators in the industry'
                    },
                    {
                        'heading': 'Certificate',
                        'article': 'Get Certified'
                    }
                ]
            })
        if pTF == 16:
            # Link and SMS Service
            context.update({
                'main_heading': 'How it works',
                'articles': [
                    {
                        'heading': 'Order',
                        'article': 'Place your order'
                    },
                    {
                        'heading': 'Get test link',
                        'article': 'Get the link of the test on mail and sms'
                    },
                    {
                        'heading': 'Test',
                        'article': 'Complete your test'
                    },
                    {
                        'heading': 'Get Report',
                        'article': 'Get the report of the site'
                    },
                    {
                        'heading': 'Get Certificate',
                        'article': 'Certificate gets added to your shine profile'
                    }
                ]
            })
        return context

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
            per_page = 9
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
                    {
                        'title': review.title, 
                        'user_email': review.user_email,
                        'user_name': review.user_name,
                        'average_rating': review.average_rating,
                        'rating': review.get_ratings(),
                        'created': review.created.strftime("%b %d, %Y"),
                        'content': review.content
                    }
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

    def get_who_should_learn(self, category):
        """
        Data for who should learn
        """
        prd_should_learn = {
            'prd_should_lrn': False
        }
        # Heading choice means only take heading with who-should-learn
        subheadercategory = SubHeaderCategory.objects.filter(category=category, heading_choices=2, active=True,
                                                             heading_choices__in=[2, 3, 4])

        if subheadercategory:
            prd_should_learn.update({
                'prd_should_lrn': True,
                'prd_should_lrn_dt': subheadercategory.first().description
            })
        return prd_should_learn

    def get_breadcrumbs(self, product, category):
        """
        Getting the breadcrumb detail
        """
        breadcrumbs = []
        breadcrumbs.append(
            OrderedDict({
                'name': 'Home',
                'url': '/',
                'active': True}))
        if category:
            if category.type_level == 4:
                category = category.get_parent(
                )[0] if category.get_parent() else None
        if category:
            if product.is_course and product.type_flow != 14:
                parent = category.get_parent()
                if parent:
                    breadcrumbs.append(
                        OrderedDict({
                            'name': parent[0].name,
                            'url': parent[0].get_absolute_url(),
                            'active': True}))

            if product.is_service or product.is_writing:
                if category.is_service and category.type_level == 3:
                    breadcrumbs.append(
                        OrderedDict({
                            'name': category.name,
                            'url': category.get_absolute_url(),
                            'active': True}))
                else:
                    parent = category.get_parent()
                    if parent:
                        breadcrumbs.append(
                            OrderedDict({
                                'name': parent[0].name,
                                'url': reverse('func_area_results', kwargs={'fa_slug': parent[0].slug, 'pk': parent[0].id}),
                                'active': True}))
            else:
                breadcrumbs.append(
                    OrderedDict({
                        'name': category.name,
                        'url': category.get_absolute_url(),
                        'active': True}))
        breadcrumbs.append(
            OrderedDict({
                'name': product.name,
                'active': None}))
        return breadcrumbs

    def get_breadcrumb_data(self, category):
        # Not in used
        breadcrumbs = []
        breadcrumbs.append({"url": '', "name": category.name})
        return breadcrumbs

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

        context.update(self.is_combos(sqs))

        context.update(json.loads(sqs.pFBT))
        get_fakeprice = self.get_solar_fakeprice(sqs.pPinb, sqs.pPfinb)
        # update get fake price
        get_fake_price = 00

        context['domain_name'] = '{}//{}'.format(
            settings.SITE_PROTOCOL, settings.SITE_DOMAIN)
        if getattr(product, 'vendor', None):
            context.update({'prd_vendor_slug': product.vendor.slug})
        # context.update({'sqs': sqs})
        context.update({'get_fakeprice': get_fakeprice})
        meta = product.as_meta(self.request)
        setattr(meta, '_keywords', None)
        setattr(meta, '_url', context.get('canonical_url', ''))
        context['meta'] = meta.__dict__
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
        candidate_id = self.request.session.get('candidate_id', None)
        if candidate_id:
            contenttype_obj = ContentType.objects.get_for_model(product)
            review_obj = Review.objects.filter(object_id=product.id, content_type=contenttype_obj,
                                                          user_id=candidate_id).first()
            if review_obj:
                context['review'] = {
                    'title': review_obj.title,
                    'user_email': review_obj.user_email,
                    'user_name:': review_obj.user_name,
                    'average_rating': review_obj.average_rating,
                    'rating': review_obj.get_ratings(),
                    'created': review_obj.created.strftime("%b %d, %Y"),
                    'content': review_obj.content
                }
            else:
                context['review'] = None
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

    def get_duration_mode(self, product):
        type_dict = dict(COURSE_TYPE_DICT)
        level_type = dict(COURSE_LEVEL_DICT)
        access_duratiopn = dict(DURATION_DICT)
        context = {}
        duration_days = json.loads(product.pVrs).get('var_list')
        if len(duration_days) != 0:
            context.update({
                'duration': duration_days[0].get('dur_days'),
                'access_duration': access_duratiopn.get(duration_days[0].get('duration')),
                'type': type_dict.get(duration_days[0].get('type'), duration_days[0].get('type')),
                'label': duration_days[0].get('label'),
                'level': level_type.get(duration_days[0].get('level'), duration_days[0].get('level')),
            })
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
            data.update(self.get_duration_mode(sqs))
            if product:
                data.update({'breadcrumbs': self.get_breadcrumbs(product, product.category_main)})
            data.update({'dlvry_flow': self.get_delivery_flow(sqs.pTF)})
            data.update(self.get_who_should_learn(product.category_main))
            if product.take_free_test:
                data.update({
                    'free_test': True,
                    'shld_take_test_slg': product.take_free_test.get_absolute_url(),
                    'test_title': product.take_free_test.title
                })
            else:
                data.update({'free_test': False})
            main_context.update(self.get_other_detail(product, sqs))
            main_context.update(data)
            if not settings.DEBUG:
                cache.set(key, data, 60 * 60 * 4)

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

    def redirect_for_resume_shine(self, path_info):
        pk = path_info.get("pk", "")
        cat_slug = 'product'
        prd_slug = path_info.get('prd_slug')

        if(path_info.get('cat_slug') == 'linkedin-profile-writing'):
            cat_slug = cat_slug + '/' + path_info.get("cat_slug", "")

        expected_path = "{}/{}/{}/{}".format(
            settings.RESUME_SHINE_MAIN_DOMAIN, cat_slug, prd_slug, pk)
        return expected_path

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
        path_info = kwargs
        context = {}
        pid = self.request.GET.get('pid')
        tracking_id = request.GET.get('t_id', '')
        utm_campaign = request.GET.get('utm_campaign', '')
        trigger_point = request.GET.get('trigger_point', '')
        u_id = request.GET.get('u_id', request.session.get('u_id', ''))
        position = self.request.GET.get('position', -1)
        popup_based_product = self.request.GET.get('popup_based_product', '')
        recommendation_by = request.GET.get('recommendation_by', '')
        cart_addition = request.GET.get('cart_addition', "False")
        self.skill = self.request.session.get('skills_name', [])

        show_popup = self.request.GET.get('spop', False)
        if not show_popup:
            try:
                self.request.session.update({'lead_create_prods': [int(kwargs.get('pk', 0))]})
            except:
                pass

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
                    'utm_campaign': utm_campaign,
                    'recommendation_by': recommendation_by
                })
                product_tracking_mapping_id = self.maintain_tracking_info(prod)
                if product_tracking_mapping_id != -1:
                    request.session.update(
                        {'product_tracking_mapping_id': product_tracking_mapping_id})

                if tracking_id and prod.id and product_tracking_mapping_id:
                    make_logging_request.delay(
                        prod.id, product_tracking_mapping_id, tracking_id, 'product_page', position, trigger_point, u_id,
                        utm_campaign, 2, popup_based_product, recommendation_by, cart_addition)

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
                recommendation_by = request.GET.get('recommendation_by', '')
                cart_addition = request.GET.get('cart_addition', "False")
                make_logging_sk_request.delay(
                    request.session.get('tracking_product_id'), request.session.get('product_tracking_mapping_id'),
                    request.session.get('tracking_id'), 'product_page', position, trigger_point, u_id, utm_campaign, 2, r_p,
                    r_sp, popup_based_product, recommendation_by, cart_addition)
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
                recommendation_by = request.GET.get('recommendation_by', '')
                cart_addition = request.GET.get('cart_addition', "False")
                if tracking_id and prod.id and product_tracking_mapping_id:
                    make_logging_sk_request.delay(
                        prod.id, product_tracking_mapping_id, tracking_id, 'product_page', position, trigger_point, u_id,
                        utm_campaign, 2, r_p, r_sp, popup_based_product, recommendation_by, cart_addition)

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
                popup_based_product = request.session.get('popup_based_product', '')
                recommendation_by = request.GET.get('recommendation_by', '')
                cart_addition = request.GET.get('cart_addition', "False")
                if tracking_id and prod.id and product_tracking_mapping_id:
                    make_logging_sk_request.delay(
                        prod.id, product_tracking_mapping_id, tracking_id, 'product_page', position, trigger_point, u_id,
                        utm_campaign, 2, r_p, r_sp, popup_based_product, recommendation_by, cart_addition)

            self.prd_key = 'detail_db_product_' + pid
            self.prd_solr_key = 'detail_solr_product_' + pid
            cache_dbprd_maping = cache.get(self.prd_key, "")
            if cache_dbprd_maping:
                self.product_obj = cache_dbprd_maping
            else:
                self.product_obj = Product.browsable.filter(pk=pid).first()
                if not settings.DEBUG:
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
                    if not settings.DEBUG:
                        cache.set(self.prd_solr_key, self.sqs, 60 * 60 * 4)
                else:
                    return APIResponse(message='Product Not Found', error=True, status=status.HTTP_404_NOT_FOUND)

            if (self.sqs.pPc == 'writing' or self.sqs.pPc == 'service' or self.sqs.pPc == 'other') and self.sqs.pTP not in [2, 4] and self.sqs.pTF not in [16, 2]:
                path_info = {"pk": self.sqs.pk, 'prd_slug': self.sqs.pSg, "cat_slug": self.sqs.pCat}
                data = {
                    'redirect_url': self.redirect_for_resume_shine(path_info)
                }
                return APIResponse(message='Resume Redirect', data=data)
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
                'product_tracking_mapping_id': self.maintain_tracking_info(self.product_obj),
                'product_id': self.product_obj and self.product_obj.id,
            })
            return APIResponse(message='Product fetched successfully', data=context)
        except Exception as e:
            logging.getLogger('error_log').error('Product fetch error with id {} and error is {}'.format(pid, str(e)))
            return APIResponse(message='Something went wrong', error=True, status=status.HTTP_400_BAD_REQUEST)


class ProductReviewAPIListing(ProductInformationAPIMixin, APIView):
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
                if not settings.DEBUG:
                    cache.set(prd_key, product_obj, 60 * 60 * 4)
                if not product_obj:
                    return APIResponse(message='Product Not found', error=True, status=status.HTTP_404_NOT_FOUND)

            context.update({'prd_reviews': self.get_reviews(product_obj, page)})

            return APIResponse(data=context, message='Review fetched successfully', status=status.HTTP_200_OK)
        except Exception as e:
            logging.getLogger('error_log').error('Product fetch error with id {} and error is {}'.format(pid, str(e)))
            return APIResponse(message='Something went wrong', error=True, status=status.HTTP_400_BAD_REQUEST)


class ProductReviewAPI(APIView):
    permission_classes = (AllowAny,)

    def __init__(self):
        self.oi = None
        self.candidate_id = None
        self.rating = None
        self.select_rat = None

    def post(self, request):
        """
        This method create reviews for individual product.
        """
        self.candidate_id = request.session.get('candidate_id', None)
        # self.candidate_id = request.POST.get('candidate_id', None)
        self.product_pk = request.POST.get('product_id') or request.data.get('product_id')
        self.product = None

        if self.product_pk and self.candidate_id:
            try:
                self.product = Product.objects.only('id').get(pk=self.product_pk)
                contenttype_obj = ContentType.objects.get_for_model(self.product)
                review_obj = Review.objects.filter(
                        object_id=self.product.id,
                        content_type=contenttype_obj,
                        user_id=self.candidate_id
                    )
                if review_obj:
                    return APIResponse(error=False, message='You have already submitted feedback', status=status.HTTP_200_OK)

                review = request.POST.get('review', '').strip() or request.data.get('review', '').strip() 
                rating = int(request.POST.get('rating', 1)) or int(request.data.get('rating', 1))
                title = request.POST.get('title', '') or request.data.get('title', '') 
                email = request.session.get('email', '')
                # email = request.POST.get('email', '')

                if not all(len(i) > 0 for i in [review, title, email]):
                    return APIResponse(error=True, message='Email, Review and Title is required', status=status.HTTP_400_BAD_REQUEST)

                name = ''
                if request.session.get('first_name'):
                    name += request.session.get('first_name')
                if request.session.get('last_name'):
                    name += ' ' + request.session.get('last_name')
                product = self.product
                create_product_review_task.delay(product.id, name, email, self.candidate_id, review, rating, title)
                return APIResponse(error=False, message='Thank you for posting review. It will be displayed after moderation.', status=status.HTTP_200_OK)

            except Exception as e:
                logging.getLogger('error_log').error('Error in creating review log: {}'.format(str(e)))
                return APIResponse(error=True, message='Something went wrong', status=status.HTTP_400_BAD_REQUEST)

        return APIResponse(error=True, message='Product Id and candidate Id required', status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        product_pk = self.request.POST.get('product_id') or self.request.data.get('product_id')
        candidate_id = request.session.get('candidate_id')
        # candidate_id = self.request.POST.get('candidate_id')

        if candidate_id and product_pk:
            review = request.POST.get('review', '').strip() or request.data.get('review', '').strip() 
            rating = int(request.POST.get('rating', 1)) or int(request.data.get('rating', 1))
            title = request.POST.get('title', '').strip() or request.data.get('title', '') 

            if not all(len(i) > 0 for i in [review, title]):
                return APIResponse(error=True, message='Review and Title is required', status=status.HTTP_400_BAD_REQUEST)

            try:
                product_obj = Product.objects.only('id').get(pk=product_pk)
                contenttype_obj = ContentType.objects.get_for_model(
                    product_obj)
                review_obj = Review.objects.filter(object_id=product_obj.id, content_type=contenttype_obj, user_id=candidate_id).first()

                # Setting status back to 0 for adding this review again to moderation list
                if review_obj and review_obj.user_id == candidate_id:
                    review_obj.content = review
                    review_obj.average_rating = rating
                    review_obj.status = 0
                    review_obj.title = title
                    review_obj.created = timezone.now()
                    review_obj.save()
                    return APIResponse(error=False, message='Thank you for posting review. It will be displayed after moderation.', status=status.HTTP_200_OK)
                else:
                    return APIResponse(error=True, message='Something went wrong', status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logging.getLogger('error_log').error('Error in updating review log: {}'.format(str(e)))
                return APIResponse(error=True, message='Something went wrong', status=status.HTTP_400_BAD_REQUEST)
        return APIResponse(error=True, message='Product Id and candidate Id required', status=status.HTTP_400_BAD_REQUEST)