from collections import OrderedDict
from django.core.paginator import Paginator
from django.http import Http404, HttpResponsePermanentRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.utils.http import urlquote
from django.views.generic import DetailView, ListView
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType

from cart.mixins import CartMixin

from .models import Product, Category, Attribute
from review.models import Review


class ProductInformationMixin(object):

    def get_breadcrumbs(self, product, category):
        breadcrumbs = []
        breadcrumbs.append(
            OrderedDict({
                'label': 'Home',
                'url': '/',
                'active': True}))
        if category:
            parent = category.get_parent()
            if parent:
                breadcrumbs.append(
                    OrderedDict({
                        'label': parent[0].name,
                        'url': parent[0].get_absolute_url(),
                        'active': True}))
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

    def get_info(self, product):
        info = {}
        info['prd_img'] = product.image.url
        info['prd_img_alt'] = product.image_alt
        info['prd_img_bg'] = product.get_bg
        info['prd_H1'] = product.heading if product.heading else product.name
        info['prd_about'] = product.about
        info['prd_desc'] = product.description
        info['prd_uget'] = product.buy_shine
        info['prd_rating'] = round(product.avg_rating, 1)
        info['prd_num_rating'] = product.no_review
        info['prd_num_bought'] = product.buy_count
        info['prd_num_jobs'] = product.num_jobs
        info['prd_vendor'] = product.vendor.name
        info['prd_vendor_img'] = product.vendor.image.url
        info['prd_vendor_img_alt'] = product.vendor.image_alt
        info['prd_rating_star'] = product.get_ratings()
        info['prd_video'] = product.video_url
        if product.is_course:
            info['prd_service'] = 'course'
        elif product.is_writing:
            info['prd_service'] = 'resume'
        elif product.is_service:
            info['prd_service'] = 'service'
        else:
            info['prd_service'] = 'other'
        info['prd_product'] = product.type_product
        info['prd_exp'] = product.get_exp
        return info

    def get_program_structure(self, product):
        structure = {
            'prd_program_struct': False
        }
        # chapter_list = product.chapters.filter(
        #     productstructure__active=True).order_by('productstructure__sort_order')
        # if chapter_list:
        #     structure.update({
        #         'prd_program_struct': True,
        #         'chap_list': chapter_list
        #     })
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

    def get_recommendation(self, product):
        recommendation = {
            'prd_recommend': False,
        }
        recommended_list = product.related.filter(
            secondaryproduct__active=True,
            active=True,
            secondaryproduct__type_relation=2)
        if recommended_list:
            recommendation.update({
                'prd_recommend': True,
                'recommended_list': recommended_list
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
                'package_list': categoryproducts})
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
                'provider_list': providers})
        return provider

    def get_combos(self, product):
        combos = product.childs.filter(active=True)
        return {'combos': combos}

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


class ProductDetailView(DetailView, ProductInformationMixin, CartMixin):
    context_object_name = 'product'
    http_method_names = ['get', 'post']

    model = Product
    
    def __init__(self, *args, **kwargs):
        # _view_signal = product_viewed
        self.category = None
        # # Whether to redirect to the URL with the right path
        self._enforce_paths = True
        # # Whether to redirect child products to their parent's URL
        self._enforce_parent = True

        super(ProductDetailView, self).__init__(*args, **kwargs)

    def get_template_names(self):
        return ['product/detail1.html']

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(ProductDetailView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        ctx = super(ProductDetailView, self).get_context_data(**kwargs)
        product = self.object
        category = self.category
        ctx.update(self.get_breadcrumbs(product, category))
        ctx.update(self.get_info(product))
        ctx.update(self.get_program_structure(product))
        ctx.update(self.get_faq(product))
        ctx.update(self.get_recommendation(product))
        ctx.update(self.get_reviews(product, 1))
        if product.type_service == 3:
            ctx.update(self.get_other_provider(product, category))
        else:
            ctx.update(self.get_other_package(product, category))
        if product.type_product == 1:
            ctx.update(self.get_variation(product))
        if product.is_combo:
            ctx.update(self.get_combos(product))
        ctx.update(self.get_frequentlybought(product, category))
        ctx.update(self.getSelectedProduct(product))
        ctx.update(self.getSelectedProductPrice(product))
        return ctx

    # def send_signal(self, request, response, product):
    #     self.view_signal.send(
    #         sender=self, product=product, user=request.user, request=request,
    #         response=response)

    def redirect_if_necessary(self, current_path, product, cat_slug=None):
        if self._enforce_paths:
            expected_path = product.get_absolute_url(cat_slug)
            if expected_path != urlquote(current_path):
                return HttpResponsePermanentRedirect(expected_path)
    
    def return_http404(self, product):
        if not product:
            return True
        if not product.active:
            return True
        if not self.category:
            return True
        if product.var_child:
            return True
        if product.is_virtual:
            return True
        return False
    
    def get(self, request, **kwargs):
        self.object = product = self.get_object()
        if product:
            self.category = category = product.verify_category(kwargs.get('cat_slug', None))

        HTTP404 = self.return_http404(product)
        if HTTP404:
            raise Http404
        redirection = self.redirect_if_necessary(
            request.path, product, category)
        if redirection is not None:
            return redirection

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
