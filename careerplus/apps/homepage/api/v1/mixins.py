# Python Core Import
import logging
import json
# Django Import
from django.utils import timezone
from django.conf import settings
from django.db.models import Count, F

# RestFramework Import

# Model Import
from shop.models import Category, Product, ProductSkill
from haystack.query import SearchQuerySet


from shop.choices import PRODUCT_CHOICES,PRODUCT_TAG_CHOICES, STUDY_MODE, COURSE_TYPE_DICT, COURSE_LEVEL_DICT
from shop.templatetags.shop_tags import get_faq_list, format_features, format_extra_features
class PopularProductMixin(object):

    def popular_courses_algorithm(self, class_category=settings.COURSE_SLUG, quantity=2, category=None):
        """
        According to the new algorithm of Trending courses
        1. Conversion ratio - (total sales generated by that product)[:3]
        2. Revenue per mile - (total amount of sales generated by that product * 1000 / Total views for that product) [:3]
        """
        try:

            if category is not None:
                product_obj = Category.objects.get(id=int(category), is_skill=True).categoryproducts.all()
            else:
                product_obj = Product.objects.filter(product_class__slug__in=class_category,
                                                     active=True,
                                                     is_indexed=True)

            product_conversion_ratio = product_obj.order_by('-buy_count')[
                                       :quantity].values_list('id', flat=True)

            product_revenue_per_mile = product_obj.annotate(
                revenue=(F('buy_count') * F('inr_price')) * 1000 / F('cp_page_view')) \
                                           .exclude(id__in=list(product_conversion_ratio)).order_by('-revenue')[
                                       :quantity].values_list('id', flat=True)

            return product_obj, product_conversion_ratio, product_revenue_per_mile

        except Exception as e:
            logging.getLogger('error_log').error("%s" % str(e))
            return False, '', ''

    def get_popular_courses(self,category,quantity=3):
        parent_categories = Category.objects.filter(id=category)
        children_categories = [c.get_childrens().values_list('id',flat=True) for c in parent_categories]
        products = Product.objects.filter(category__id__in=children_categories,
                                                    active=True,
                                                   is_indexed=True).order_by('-buy_count')[:quantity].\
                                                    values_list('id', flat=True)
        return products   

    def get_products_json(self,product_ids):
        products = SearchQuerySet().filter(id__in=product_ids, pTP__in=[0, 1, 3]).exclude(
            id__in=settings.EXCLUDE_SEARCH_PRODUCTS
        )
        popularProducts = ProductMixin().get_course_json(products)
        return popularProducts 
    
    def popular_certifications(self):
        try:
            product_obj = Product.objects.filter(type_flow=16,
                                                     active=True,
                                                     is_indexed=True)

            product_conversion_ratio = product_obj.order_by('-buy_count').values_list('id', flat=True)
            products = SearchQuerySet().filter(id__in=product_conversion_ratio, pTP__in=[0, 1, 3]).exclude(
            id__in=settings.EXCLUDE_SEARCH_PRODUCTS
            )[:20]
            popular_certification = ProductMixin().get_course_json(products)

            return popular_certification

        except Exception as e:
            logging.getLogger('error_log').error("%s" % str(e))
            return False, '', ''

class ProductMixin(object):

    def get_course_json(self, courses=[]):
        course_data = []
        mode_choices = dict(STUDY_MODE)
        type_dict = dict(COURSE_TYPE_DICT)
        level_type = dict(COURSE_LEVEL_DICT)
        for course in courses:
            d = json.loads(course.pVrs).get('var_list')
            data = {
                'id':course.id,
                'name':course.pNm,
                'about':course.pAb,
                'url':course.pURL,
                'imgUrl':course.pImg,
                'imgAlt':course.pImA,
                'title':course.pTt,
                'slug':course.pSg,
                'jobsAvailable':course.pNJ,
                'skillList': course.pSkilln,
                'rating': float(course.pARx),
                'stars': course.pStar,
                'mode': mode_choices.get(course.pStM[0], course.pStM[0]) if course.pStM else None,
                'providerName':course.pPvn,
                'price':float(course.pPin),
                'tags': PRODUCT_TAG_CHOICES[course.pTg][0],
                'highlights':format_extra_features(course.pBS) if course.pBS else None,
                'brochure':json.loads(course.pUncdl[0]).get('brochure') if course.pUncdl else None,
                'u_courses_benefits':json.loads(course.pUncdl[0]).get('highlighted_benefits').split(';') if course.pUncdl else None,
                'u_desc': course.pDsc,
                }
            if len(d)!=0:
                data.update({
                    'duration':d[0].get('dur_days'), 
                    'type':type_dict.get(d[0].get('type'), d[0].get('type')),  
                    'label':d[0].get('label'), 
                    'level':level_type.get(d[0].get('level'), d[0].get('level')), 
                })
            course_data.append(data)

        return course_data

    def get_assessments_json(self, assessments=[]):
        assessments_data = []
        mode_choices = dict(STUDY_MODE)
        for assessment in assessments:
            assessment_data = {
                'id':assessment.id,
                'name':assessment.pNm,
                'about':assessment.pAb,
                'url':assessment.pURL,
                'imgUrl':assessment.pImg,
                'rating':assessment.pARx,
                'stars': assessment.pStar,
                'jobsAvailable':assessment.pNJ,
                'skillList': assessment.pSkilln,
                'mode': mode_choices.get(assessment.pStM[0], assessment.pStM[0]) if assessment.pStM else None,
                'providerName':assessment.pPvn if assessment.pPvn else None,
                'price':float(assessment.pPin),
                'tags':PRODUCT_TAG_CHOICES[assessment.pTg][1],
                'brochure':json.loads(assessment.pUncdl[0]).get('brochure') if assessment.pUncdl else None,
                'test_duration':json.loads(assessment.pAsft[0]).get('test_duration') if assessment.pAsft else None,
                'number_of_questions':json.loads(assessment.pAsft[0]).get('number_of_questions') if assessment.pAsft else None,
            }
            assessments_data.append(assessment_data)

        return assessments_data
