
from collections import OrderedDict
from django.core.paginator import Paginator
from django.http import Http404, HttpResponsePermanentRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.utils.http import urlquote
from django.views.generic import DetailView, ListView
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from .models import Product, Category, Attribute
from review.models import Review


class ProductInformationMixin(object):

    def get_breadcrumbs(self, product, category_slug):
        breadcrumbs = []
        breadcrumbs.append(
            OrderedDict({
                'label': 'Home',
                'url': '/',
                'active': True}))
        try:
            prod_cat = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            prod_cat = product.categories.filter(
                productcategories__is_main=True,
                productcategories__active=True)
            if prod_cat:
                prod_cat = prod_cat[0]
            else:
                prod_cat = None
        if prod_cat:
            main_cat = prod_cat.related_to.filter(
                to_category__relation=0, to_category__related_from=prod_cat,
                to_category__is_main_parent=True)

            if main_cat:
                breadcrumbs.append(
                    OrderedDict({
                        'label': main_cat[0].name,
                        'url': main_cat[0].get_absolute_url(),
                        'active': True}))
                breadcrumbs.append(
                    OrderedDict({
                        'label': prod_cat.name,
                        'url': prod_cat.get_absolute_url(),
                        'active': True}))
                breadcrumbs.append(
                    OrderedDict({
                        'label': product.name,
                        'active': None}))
        return {
            'breadcrumbs': breadcrumbs
        }

    def get_sibling_package(self, product):
        other_siblings = OrderedDict()
        siblings = {
            'product_type': 'course',
            'otherprovide': other_siblings
        }
        return siblings

    def get_info(self, product):
        info = {}
        info['prd_img'] = product.image.url
        info['prd_img_alt'] = product.image_alt
        info['prd_H1'] = product.heading if product.heading else product.name
        info['prd_about'] = product.about
        info['prd_desc'] = product.description
        info['prd_uget'] = product.buy_shine
        info['prd_rating'] = round(product.avg_rating, 1)
        info['prd_num_rating'] = product.no_review
        info['prd_num_bought'] = product.buy_count
        info['prd_num_jobs'] = product.num_jobs
        info['prd_rating_star'] = product.get_ratings()
        return info

    def get_program_structure(self, product):
        structure = {
            'prd_program_struct': False
        }
        topic = product.structure
        topic_chapter_list = topic.chapters.filter(
            topicchapters__active=True).order_by('topicchapters__sort_order')
        if topic_chapter_list:
            structure.update({
                'prd_program_struct': True,
                'topic_chap_list': topic_chapter_list
            })
        return structure

    def get_faq(self, product):
        structure = {
            'prd_faq': False
        }
        faqs = product.faqs.filter(
            productfaqs__active=True).order_by('productfaqs__question_order')
        if faqs:
            structure.update({
                'prd_faq': True,
                'faq_list': faqs
            })
        return structure

    def get_recommendation(self, product):
        recommendation = {
            'prd_recommend': True,
        }
        recommended_list = product.related.filter(
            secondaryproduct__active=True,
            secondaryproduct__type_relation=2)
        if recommendation:
            recommendation.update({
                'prd_recommend': True,
                'recommended_list': recommended_list
            })
        return recommendation

    def get_combos(self, product):
        combos = []
        combo_list = product.childs.all()
        for combo in combo_list:
            combos.append(
                OrderedDict({
                    'label': combo.name,
                    'url': '/'}))
        return {'combos': combos}

    def get_childs(self, product):
        childs = []
        child_list = product.childs.all()
        from shop.choices import MODE_CHOICES, COURSE_TYPE_CHOICES
        for child in child_list:
            childs.append(
                OrderedDict({
                    'label': child.name,
                    'mode': dict(MODE_CHOICES).get(child.study_mode),
                    'duration': child.duration_months,
                    'type': dict(COURSE_TYPE_CHOICES).get(child.course_type),
                    'certify': child.certification,
                    'url': '/'}))
        return {'childs': childs}

    def get_variation(self, product):
        variation = []
        var_list = product.variation.all()
        from shop.choices import EXP_CHOICES
        EXP_DICT = dict(EXP_CHOICES)
        for var in var_list:
            variation.append(
                OrderedDict({
                    'label': EXP_DICT.get(var.experience),
                    'url': '/'}))
        return {
            'variations': variation,
            'prd_variation': EXP_DICT.get(product.experience)
        }

    def get_countries(self, product):
        attr_country = []
        country_id = Attribute.objects.get(pk='1')
        attr_country_list = product.productattributes.filter(
            attribute=country_id)
        for con in attr_country_list:
            attr_country.append(
                OrderedDict({
                    'id': con.value_option.id,
                    'name': con.value_option.option}))
        return {
            'countries': attr_country}

    def get_reviews(self, product, page):
        product_type = ContentType.objects.get(
            app_label='shop', model='product')
        try:
            review_list = Review.objects.filter(
                content_type__id=product_type.id,
                object_id=product.pk)
            rv_total = len(review_list)
            per_page = 5
            rv_paginator = Paginator(review_list, per_page)
            rv_page = int(page if page else 1)
            try:
                review_list = rv_paginator.page(rv_page)
            except:
                review_list = []
            return {
                'prd_rv_total': rv_total,
                'prd_review_list': review_list,
                'prd_rv_page': rv_page}
        except:
            return {
                'prd_rv_total': 0,
                'prd_review_list': [],
                'prd_rv_page': page
            }


class ProductDetailView(DetailView, ProductInformationMixin):
    context_object_name = 'product'
    http_method_names = ['get', 'post']

    model = Product
    _view_signal = None
    # # Whether to redirect to the URL with the right path
    _enforce_paths = True
    # # Whether to redirect child products to their parent's URL
    # __enforce_parent__ = True

    def __init__(self, *args, **kwargs):
        # _view_signal = product_viewed

        super(ProductDetailView, self).__init__(*args, **kwargs)

    def get_template_names(self):
        return ['product/detail.html']

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(ProductDetailView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        ctx = super(ProductDetailView, self).get_context_data(**kwargs)
        product = self.object
        cat_slug = kwargs.get('cat_slug', None)
        ctx.update(self.get_breadcrumbs(product, cat_slug))
        ctx.update(self.get_info(self.object))
        ctx.update(self.get_variation(product))
        # ctx.update(self.get_program_structure(product))
        ctx.update(self.get_faq(product))
        ctx.update(self.get_recommendation(product))
        ctx.update(self.get_combos(product))
        ctx.update(self.get_childs(product))
        # ctx.update(self.get_countries(product))
        ctx.update(self.get_reviews(product, 1))
        return ctx

    # def send_signal(self, request, response, product):
    #     self.view_signal.send(
    #         sender=self, product=product, user=request.user, request=request,
    #         response=response)

    def redirect_if_necessary(self, current_path, product):
        # if self.enforce_parent and product.is_child:
        #     return HttpResponsePermanentRedirect(
        #         product.parent.get_absolute_url())

        if self._enforce_paths:
            expected_path = product.get_absolute_url()
            if expected_path != urlquote(current_path):
                return HttpResponsePermanentRedirect(expected_path)

    def get(self, request, **kwargs):
        self.object = product = self.get_object()
        redirect = self.redirect_if_necessary(request.path, product)
        if redirect is not None:
            return redirect

        response = super(ProductDetailView, self).get(request, **kwargs)
        # self.send_signal(request, response, product)
        return response


class ProductReviewListView(ListView, ProductInformationMixin):
    template_name = 'product/partials/reviews.html'
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
            self._page_kwarg = self.request.GET.get('pg', 1)
            try:
                self._product = Product.objects.get(
                    pk=self.kwargs['product_pk'])
            except:
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
