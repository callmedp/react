import json
import logging

from collections import OrderedDict

from django.views.generic import (
    View, FormView, TemplateView, ListView, DetailView)
from django.http import (Http404,
    HttpResponseForbidden, HttpResponse,
    HttpResponseRedirect, HttpResponseBadRequest)
from django.core import exceptions
from django.conf import settings
from django.forms.models import inlineformset_factory
from django.template.response import TemplateResponse
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from .decorators import (
    Decorate, check_permission, check_group,
    stop_browser_cache, has_group)
from django.core.paginator import Paginator
from django.db.models import Q
from shop.choices import PRODUCT_VENDOR_CHOICES, APPLICATION_PROCESS, SUB_FLOWS
from blog.mixins import PaginationMixin
from shop.models import (
    Product, ProductScreen, ScreenChapter,
    Skill, ScreenProductSkill,
    UniversityCoursePaymentScreen)
from faq.models import (
    ScreenFAQ, FAQuestion)
from shop.utils import ProductModeration
from .vendor_form import (
    AddScreenProductForm,
    ChangeScreenProductForm,
    AddScreenProductVariantForm,
    AddScreenFaqForm,
    ChangeScreenFaqForm,
    ScreenProductCountryForm,
    ScreenProductPriceForm,
    ScreenProductAttributeForm,
    ScreenProductFAQForm,
    ScreenFAQInlineFormSet,
    ScreenProductChapterForm,
    ScreenChapterInlineFormSet,
    ScreenProductVariationForm,
    ScreenVariationInlineFormSet,
    ScreenProductSkillForm,
    ScreenSkillInlineFormSet,
    ScreenUniversityCourseForm,
    ScreenUniversityCoursePaymentForm,
    ScreenUniversityCoursesPaymentInlineFormset)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.VENDOR_GROUP_LIST, settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('faq.console_change_faq'))
class ChangeScreenFaqView(DetailView):
    template_name = 'console/vendor/change_screenfaq.html'
    model = ScreenFAQ

    def dispatch(self, request, *args, **kwargs):
        return super(ChangeScreenFaqView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        faq = self.get_object()
        if not faq:
            raise Http404
        if has_group(user=self.request.user, grp_list=settings.PRODUCT_GROUP_LIST):
            pass
        else:
            user_vendor = self.request.user.get_vendor()
            if not user_vendor:
                return HttpResponseForbidden()
            if user_vendor != faq.vendor:
                return HttpResponseForbidden() 
        
        return super(ChangeScreenFaqView, self).get(request, args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(ChangeScreenFaqView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(ChangeScreenFaqView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        main_change_form = ChangeScreenFaqForm(
            instance=self.get_object())
        context.update({
            'messages': alert,
            'form': main_change_form})
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST:
            try:
                obj = int(self.kwargs.get('pk', None))
                faq = int(request.POST.get('faq'))
                if obj == faq:
                    obj = self.object = self.get_object()
                    if has_group(user=self.request.user, grp_list=settings.PRODUCT_GROUP_LIST):
                        pass
                    else:
                        user_vendor = self.request.user.get_vendor()
                        if not user_vendor:
                            messages.error(
                            self.request,
                            "You are not associated to any vendor")
                            return HttpResponseRedirect(reverse('console:screenfaq-list',))
                        if user_vendor != obj.vendor:
                            messages.error(
                            self.request,
                            "FAQ not associated to your vendor")
                            return HttpResponseRedirect(reverse('console:screenfaq-list',))
                        
                    form = None
                    form = ChangeScreenFaqForm(
                        request.POST, instance=obj)
                    if form.is_valid():
                        form.save()
                        messages.success(
                            self.request,
                            "FAQ Changed Successfully")
                        return HttpResponseRedirect(reverse('console:screenfaq-list',))
                    else:
                        context = self.get_context_data()
                        if form:
                            context.update({'form': form})
                        messages.error(
                            self.request,
                            "FAQ Object Change Failed, Changes not Saved")
                        return TemplateResponse(
                            request, [
                                "console/vendor/change_screenfaq.html"
                            ], context)
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:screenfaq-change', kwargs={'pk': faq}))
            except Exception as e:
                messages.error(request, (
                    ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
                logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})

                return HttpResponseRedirect(
                    reverse('console:screenfaq-change', kwargs={'pk': faq}))
        return HttpResponseBadRequest()


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.VENDOR_GROUP_LIST, settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('faq.console_add_faq'))
class AddScreenFaqView(FormView):
    form_class = AddScreenFaqForm
    template_name = 'console/vendor/add_screenfaq.html'
    http_method_names = ['get', 'post']
    success_url = reverse_lazy('console:screenfaquestion-add')

    def get(self, request, *args, **kwargs):
        return super(AddScreenFaqView, self).get(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AddScreenFaqView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        return context

    def form_valid(self, form):
        user = self.request.user
        if user.has_perm('faq.console_add_faq'):
            vendor = user.get_vendor()
            if not vendor:
                messages.error(
                    self.request,
                    "You are not associated to any vendor.")
                return super(AddScreenFaqView, self).form_invalid(form)
            faq = form.save()
            faq.vendor = vendor
            faq.save()
            faq.create_faq()
            
            messages.success(
                self.request,
                "You have successfully added a faq"
            )    
            self.success_url = reverse_lazy('console:screenfaq-list')
            return super(AddScreenFaqView, self).form_valid(form)
        else:
            messages.error(
                self.request,
                "You don't have permission to add faq.")          
            return super(AddScreenFaqView, self).form_invalid(form)
        
    def form_invalid(self, form):
        messages.error(
            self.request,
            "Your submission has not been saved. Try again."
        )
        return super(AddScreenFaqView, self).form_invalid(form)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.VENDOR_GROUP_LIST, settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('faq.console_change_faq'))
class ListScreenFaqView(ListView, PaginationMixin):
    model = ScreenFAQ
    context_object_name = 'screenfaq_list'
    template_name = 'console/vendor/list_faq_screen.html'
    http_method_names = [u'get', ]

    def dispatch(self, request, *args, **kwargs):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        return super(
            ListScreenFaqView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(ListScreenFaqView, self).get(request, args, **kwargs)

    def get_queryset(self):
        queryset = super(ListScreenFaqView, self).get_queryset()
        queryset = queryset.exclude(status=2)
        
        if has_group(user=self.request.user, grp_list=settings.PRODUCT_GROUP_LIST):
            pass
        else:
            vendor = self.request.user.get_vendor()
            if not vendor:
                queryset = queryset.none()
            else:
                queryset = queryset.filter(vendor=vendor)
        try:
            if self.query:
                queryset = queryset.filter(Q(text__icontains=self.query))
        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset %s'%str(e))
            pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListScreenFaqView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        paginator = Paginator(context['screenfaq_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "query": self.query,
            "messages": alert,
        })
        return context


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('faq.console_change_faq'))
class ListModerationScreenFaqView(ListView, PaginationMixin):
    model = ScreenFAQ
    context_object_name = 'screenfaq_list'
    template_name = 'console/vendor/list_faq_screen.html'
    http_method_names = [u'get', ]

    def dispatch(self, request, *args, **kwargs):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        return super(
            ListModerationScreenFaqView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        return super(ListModerationScreenFaqView, self).get(request, args, **kwargs)

    def get_queryset(self):
        queryset = super(ListModerationScreenFaqView, self).get_queryset()
        queryset = queryset.filter(status=2)
        try:
            if self.query:
                queryset = queryset.filter(Q(text__icontains=self.query))
        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset%s'%str(e))
            pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListModerationScreenFaqView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        paginator = Paginator(context['screenfaq_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "query": self.query,
            "messages": alert,
            "moderation": True
        })
        return context

@Decorate(stop_browser_cache())
@Decorate(check_group([settings.VENDOR_GROUP_LIST, settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_change_product'))
class ListScreenProductView(ListView, PaginationMixin):
    model = ProductScreen
    context_object_name = 'productscreen_list'
    template_name = 'console/vendor/list_product_screen.html'
    http_method_names = [u'get', ]

    def dispatch(self, request, *args, **kwargs):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        return super(
            ListScreenProductView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(
            ListScreenProductView, self).get(request, args, **kwargs)

    def get_queryset(self):
        queryset = super(ListScreenProductView, self).get_queryset()
        queryset = queryset.exclude(type_product=2)
        queryset = queryset.exclude(status=2)
        
        if has_group(user=self.request.user, grp_list=settings.PRODUCT_GROUP_LIST):
            pass
        else:
            vendor = self.request.user.get_vendor()
            if not vendor:
                queryset = queryset.none()
            else:
                queryset = queryset.filter(vendor=vendor, type_product__in=[0, 1])
        try:
            if self.query:
                queryset = queryset.filter(Q(name__icontains=self.query))
        except Exception as e:
            logging.getLogger('error_log').error('unable to get query set %s'%str(e))

            pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            ListScreenProductView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        paginator = Paginator(
            context['productscreen_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "query": self.query,
            "messages": alert,
        })
        return context


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_change_product'))
class ListModerationScreenProductView(ListView, PaginationMixin):
    model = ProductScreen
    context_object_name = 'productscreen_list'
    template_name = 'console/vendor/list_product_screen.html'
    http_method_names = [u'get', ]

    def dispatch(self, request, *args, **kwargs):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        return super(
            ListModerationScreenProductView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(
            ListModerationScreenProductView, self).get(request, args, **kwargs)

    def get_queryset(self):
        queryset = super(ListModerationScreenProductView, self).get_queryset()
        queryset = queryset.exclude(type_product=2)
        queryset = queryset.filter(status=2)
        try:
            if self.query:
                queryset = queryset.filter(Q(name__icontains=self.query))
        except Exception as e:
            logging.getLogger('error_log').error('unable to get queryset %s'%str(e))
            pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            ListModerationScreenProductView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        paginator = Paginator(
            context['productscreen_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "query": self.query,
            "messages": alert,
            "moderation": True
        })
        return context


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.VENDOR_GROUP_LIST, settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_add_product'))
class AddScreenProductView(FormView):
    form_class = AddScreenProductForm
    template_name = 'console/vendor/add_screenproduct.html'
    http_method_names = ['get', 'post']
    success_url = reverse_lazy('console:screenproduct-add')

    def get_form_kwargs(self):
        kwargs = super(
            AddScreenProductView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get(self, request, *args, **kwargs):
        return super(AddScreenProductView, self).get(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(
            AddScreenProductView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert,
            'sub_type_flow_choices': json.dumps(SUB_FLOWS)})
        return context

    def form_valid(self, form):
        user = self.request.user
        if user.has_perm('shop.console_add_product'):
            vendor = user.get_vendor()
            if not vendor:
                messages.error(
                    self.request,
                    "You are not associated to any vendor.")
                return super(
                    AddScreenProductView, self).form_invalid(form)
            productscreen = form.save()
            productscreen.vendor = vendor
            productscreen.save()
            productscreen.create_product()
            messages.success(
                self.request,
                "You have successfully added a product"
            )    
            self.success_url = reverse_lazy('console:screenproduct-list')
            return super(
                AddScreenProductView, self).form_valid(form)
        else:
            messages.error(
                self.request,
                "You don't have permission to add product.")          
            return super(
                AddScreenProductView, self).form_invalid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Your submission has not been saved. Try again."
        )
        return super(
            AddScreenProductView, self).form_invalid(form)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.VENDOR_GROUP_LIST, settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_change_product'))
class ChangeScreenProductView(DetailView):
    template_name = 'console/vendor/change_screenproduct.html'
    model = ProductScreen

    def dispatch(self, request, *args, **kwargs):
        return super(
            ChangeScreenProductView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        if not product:
            raise Http404
        
        if has_group(user=self.request.user, grp_list=settings.PRODUCT_GROUP_LIST):
            if product.type_product == 2:
                raise Http404
        else:
            user_vendor = self.request.user.get_vendor()
            if not user_vendor:
                return HttpResponseForbidden()
            if user_vendor != product.vendor:
                return HttpResponseForbidden()
            if not product.type_product in [0, 1]:
                raise Http404
        
        return super(
            ChangeScreenProductView, self).get(request, args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(
                ChangeScreenProductView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(
            ChangeScreenProductView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        main_change_form = ChangeScreenProductForm(
            instance=self.get_object(),
            user=self.request.user)
        price_form = ScreenProductPriceForm(instance=self.get_object())
        country_form = ScreenProductCountryForm(instance=self.get_object())
        obj = self.get_object()
        attribute_form = ScreenProductAttributeForm(
            instance=self.get_object(),)
        if has_group(user=self.request.user, grp_list=settings.PRODUCT_GROUP_LIST):
            vendor = self.get_object().vendor
        else:
            vendor = self.request.user.get_vendor()
        
        ScreenProductFAQFormSet = inlineformset_factory(
            ProductScreen, ProductScreen.faqs.through, fk_name='product',
            form=ScreenProductFAQForm,
            can_delete=False,
            formset=ScreenFAQInlineFormSet, extra=1,
            max_num=50, validate_max=True)
        if self.object:
            prdfaq_formset = ScreenProductFAQFormSet(
                instance=self.get_object(),
                form_kwargs={'object': self.get_object(),
                    'vendor': vendor},)
            context.update({'prdfaq_formset': prdfaq_formset})

        ScreenProductSkillFormSet = inlineformset_factory(
            ProductScreen, ScreenProductSkill,
            fk_name='product',
            form=ScreenProductSkillForm,
            can_delete=True,
            formset=ScreenSkillInlineFormSet, extra=1,
            max_num=15, validate_max=True)

        if self.object:
            prdskill_formset = ScreenProductSkillFormSet(
                instance=self.get_object(),
                form_kwargs={'object': self.get_object()})
            context.update({'prdskill_formset': prdskill_formset})

        ScreenProductChapterFormSet = inlineformset_factory(
            ProductScreen, ScreenChapter, fk_name='product',
            form=ScreenProductChapterForm,
            can_delete=False,
            formset=ScreenChapterInlineFormSet, extra=1,
            max_num=50, validate_max=True)
        if self.object:
            prdchapter_formset = ScreenProductChapterFormSet(
                instance=self.get_object(),
                form_kwargs={'object': self.get_object()},)
            context.update({'prdchapter_formset': prdchapter_formset})
        
        if self.object.type_product == 1:
            ScreenProductVariationFormSet = inlineformset_factory(
                ProductScreen, ProductScreen.variation.through, fk_name='main',
                form=ScreenProductVariationForm,
                can_delete=True,
                formset=ScreenVariationInlineFormSet, extra=0,
                max_num=50, validate_max=True)
            if self.object:
                prdvar_formset = ScreenProductVariationFormSet(
                    instance=self.get_object(),
                    form_kwargs={'object': self.get_object()})
                context.update({'prdvars_formset': prdvar_formset})
        if self.object.type_flow == 14:
            context.update({'prd_university_form': ScreenUniversityCourseForm(
                instance=self.object.screen_university_course_detail)})

            UniversityCoursesPaymentFormset = inlineformset_factory(
                ProductScreen, UniversityCoursePaymentScreen,
                fk_name='productscreen',
                form=ScreenUniversityCoursePaymentForm,
                can_delete=True,
                formset=ScreenUniversityCoursesPaymentInlineFormset, extra=1,
                max_num=15, validate_max=True
            )
 
            university_payment_formset = UniversityCoursesPaymentFormset(instance=self.object)
            context.update({'prd_university_payment_formset': university_payment_formset })

        context.update({
            'messages': alert,
            'form': main_change_form,
            'country_form': country_form,
            'price_form': price_form,
            'attribute_form': attribute_form,
            })
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST or self.request.FILES:
            try:
                obj = int(self.kwargs.get('pk', None))
                prd = int(request.POST.get('product'))
                if obj == prd:
                    obj = self.object = self.get_object()
                    slug = request.POST.get('slug', None)
                    if obj.type_product == 2:
                        messages.error(
                        self.request,
                        "Product is a child variation")
                        return HttpResponseRedirect(reverse('console:screenproduct-change',kwargs={'pk': obj.pk}))
                    
                    if has_group(user=self.request.user, grp_list=settings.PRODUCT_GROUP_LIST):
                        pass
                    else:
                        user_vendor = self.request.user.get_vendor()
                        if not user_vendor:
                            messages.error(
                            self.request,
                            "You are not associated to any vendor")
                            return HttpResponseRedirect(reverse('console:screenproduct-change',kwargs={'pk': obj.pk}))
                        if user_vendor != obj.vendor:
                            messages.error(
                            self.request,
                            "Product not associated to your vendor")
                            return HttpResponseRedirect(reverse('console:screenproduct-change',kwargs={'pk': obj.pk}))
                        
                    form = None
                    if slug == 'main':
                        form = ChangeScreenProductForm(
                            request.POST, instance=obj, user=self.request.user)
                        if form.is_valid():
                            productscreen = form.save()
                            if not productscreen.status == 2:    
                                productscreen.status = 1
                                productscreen.save()        
                            messages.success(
                                self.request,
                                "Product Changed Successfully")
                            return HttpResponseRedirect(reverse('console:screenproduct-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'form': form})
                            messages.error(
                                self.request,
                                "Product Object Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/vendor/change_screenproduct.html"
                                ], context)
                    elif slug == 'country':
                        form = ScreenProductCountryForm(request.POST, instance=obj)
                        if form.is_valid():
                            productscreen = form.save()
                            if not productscreen.status == 2:    
                                productscreen.status = 1
                                productscreen.save()        
                            
                            messages.success(
                                self.request,
                                "Product Countries Visible changed Successfully")
                            return HttpResponseRedirect(reverse('console:screenproduct-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'country_form': form})
                            messages.error(
                                self.request,
                                "Product Country Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/vendor/change_screenproduct.html"
                                ], context)
                    elif slug == 'price':
                        form = ScreenProductPriceForm(request.POST, instance=obj)
                        if form.is_valid():
                            productscreen = form.save()
                            if not productscreen.status == 2:    
                                productscreen.status = 1
                                productscreen.save()        
                            messages.success(
                                self.request,
                                "Product Prices changed Successfully")
                            return HttpResponseRedirect(reverse('console:screenproduct-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'price_form': form})
                            messages.error(
                                self.request,
                                "Product Prices Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/vendor/change_screenproduct.html"
                                ], context)
                    elif slug == 'attribute':
                        form = ScreenProductAttributeForm(
                                request.POST,
                                request.FILES,
                                instance=obj)
                        if form.is_valid():
                            productscreen = form.save()
                            if not productscreen.status == 2:    
                                productscreen.status = 1
                            productscreen.save()        
                            messages.success(
                                self.request,
                                "Product Attributes changed Successfully")
                            return HttpResponseRedirect(reverse('console:screenproduct-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'attribute_form': form})
                            messages.error(
                                self.request,
                                "Product Attributes Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/vendor/change_screenproduct.html"
                                ], context)
                    elif slug == 'faqs':
                        if has_group(user=self.request.user, grp_list=settings.PRODUCT_GROUP_LIST):
                            vendor = self.get_object().vendor
                        else:
                            vendor  = self.request.user.get_vendor()
                        
                        ScreenProductFAQFormSet = inlineformset_factory(
                            ProductScreen, ProductScreen.faqs.through, fk_name='product',
                            form=ScreenProductFAQForm,
                            can_delete=False,
                            formset=ScreenFAQInlineFormSet, extra=0,
                            max_num=50, validate_max=True)
                        formset = ScreenProductFAQFormSet(
                            request.POST, instance=obj,
                            form_kwargs={'object': obj,
                                'vendor':vendor },)
                        from django.db import transaction
                        if formset.is_valid():
                            with transaction.atomic():
                                formset.save(commit=False)
                                saved_formset = formset.save(commit=False)
                                for ins in formset.deleted_objects:
                                    ins.delete()

                                for form in saved_formset:
                                    form.save()
                                formset.save_m2m()
                                if not obj.status == 2:    
                                    obj.status = 1
                                    obj.save()        
                                
                            messages.success(
                                self.request,
                                "Product FAQ changed Successfully")
                            return HttpResponseRedirect(reverse('console:screenproduct-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if formset:
                                context.update({'prdfaq_formset': formset})
                            messages.error(
                                self.request,
                                "Product FAQ Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/vendor/change_screenproduct.html"
                                ], context)
                    elif slug == 'vars':
                        ScreenProductVariationFormSet = inlineformset_factory(
                            ProductScreen, ProductScreen.variation.through, fk_name='main',
                            form=ScreenProductVariationForm,
                            can_delete=False,
                            formset=ScreenVariationInlineFormSet, extra=1,
                            max_num=50, validate_max=True)
                        formset = ScreenProductVariationFormSet(
                            request.POST, instance=obj,
                            form_kwargs={'object': obj},)
                        from django.db import transaction
                        if formset.is_valid():
                            with transaction.atomic():
                                formset.save(commit=False)
                                saved_formset = formset.save(commit=False)
                                for ins in formset.deleted_objects:
                                    ins.delete()

                                for form in saved_formset:
                                    form.save()
                                formset.save_m2m()
                                if not obj.status == 2:    
                                    obj.status = 1
                                    obj.save()        
                                
                            messages.success(
                                self.request,
                                "Product Variation changed Successfully")
                            return HttpResponseRedirect(reverse('console:screenproduct-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if formset:
                                context.update({'prdvars_formset': formset})
                            messages.error(
                                self.request,
                                "Product Variation Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/vendor/change_screenproduct.html"
                                ], context)
                    elif slug == 'chapter':
                        ScreenProductChapterFormSet = inlineformset_factory(
                            ProductScreen, ScreenChapter, fk_name='product',
                            form=ScreenProductChapterForm,
                            can_delete=False,
                            formset=ScreenChapterInlineFormSet, extra=1,
                            max_num=50, validate_max=True)
                        formset = ScreenProductChapterFormSet(
                            request.POST, instance=obj,
                            form_kwargs={'object': obj},)
                        from django.db import transaction
                        if formset.is_valid():
                            with transaction.atomic():
                                formset.save(commit=False)
                                saved_formset = formset.save(commit=False)
                                for ins in formset.deleted_objects:
                                    ins.delete()

                                for form in saved_formset:
                                    form.save()
                                formset.save_m2m()
                                if not obj.status == 2:    
                                    obj.status = 1
                                    obj.save()        
                                
                            messages.success(
                                self.request,
                                "Product Chapter changed Successfully")
                            return HttpResponseRedirect(reverse('console:screenproduct-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if formset:
                                context.update({'prdchapter_formset': formset})
                            messages.error(
                                self.request,
                                "Product Chapter Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/vendor/change_screenproduct.html"
                                ], context)

                    elif slug == 'skill':
                        ScreenProductSkillFormSet = inlineformset_factory(
                            ProductScreen, ScreenProductSkill, fk_name='product',
                            form=ScreenProductSkillForm,
                            can_delete=True,
                            formset=ScreenSkillInlineFormSet, extra=0,
                            max_num=15, validate_max=True)
                        formset = ScreenProductSkillFormSet(
                            request.POST, instance=obj,
                            form_kwargs={'object': obj},)
                        from django.db import transaction
                        if formset.is_valid():
                            with transaction.atomic():
                                formset.save(commit=False)
                                saved_formset = formset.save(commit=False)
                                for ins in formset.deleted_objects:
                                    ins.delete()

                                for form in saved_formset:
                                    form.save()
                                formset.save_m2m()
                            messages.success(
                                self.request,
                                "Product Skill Changed Successfully")
                            return HttpResponseRedirect(
                                reverse(
                                    'console:screenproduct-change',
                                    kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if formset:
                                context.update({'prdskill_formset': formset})
                            messages.error(
                                self.request,
                                "Product Skill Change Failed, \
                                Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/vendor/change_screenproduct.html"
                                ], context)
                    elif slug == 'university':
                        form = ScreenUniversityCourseForm(request.POST, request.FILES, instance=obj.screen_university_course_detail)
                        application_process_priority = [k for k in form.data['application_process_priority'].split(',') if k]

                        if application_process_priority:
                            form.data['application_process'] = str(application_process_priority)

                        benefits_priority = [k for k in form.data['benefits_priority'].split(',') if k]
                        form.data['benefits'] = str(benefits_priority) if benefits_priority else ''
                        headings = [key for key in form.data.keys() if key.startswith('heading')]
                        attendees_criteria = []

                        for heading in sorted(headings):
                            if form.data[heading] or form.data['sub' + heading]:
                                attendees_criteria.append((form.data[heading], form.data['sub'+heading]))

                        form.data['attendees_criteria'] = str(attendees_criteria)
                        if form.is_valid():
                            form.save()
                            if not obj.status == 2:
                                obj.status = 1
                                obj.save()
                            messages.success(
                                self.request,
                                "University course details changed Successfully")
                            return HttpResponseRedirect(reverse('console:screenproduct-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'prd_university_form': form})
                            messages.error(
                                self.request,
                                "University course details Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/vendor/change_screenproduct.html"
                                ], context)

                    elif slug == 'university_payment':
                        UniversityCoursesPaymentFormset = inlineformset_factory(
                            ProductScreen, UniversityCoursePaymentScreen,
                            form=ScreenUniversityCoursePaymentForm,
                            can_delete=True,
                            extra=2,
                            max_num=15, validate_max=True
                        )
                        formset = UniversityCoursesPaymentFormset(
                            request.POST, instance=obj)
                        from django.db import transaction
                        if formset.is_valid():
                            with transaction.atomic():
                                formset.save(commit=False)
                                saved_formset = formset.save(commit=False)
                                for ins in formset.deleted_objects:
                                    ins.delete()

                                for form in saved_formset:
                                    form.save()
                                if not obj.status == 2:
                                    obj.status = 1
                                    obj.save()
                            messages.success(
                                self.request,
                                "University course Changed Successfully")
                            return HttpResponseRedirect(
                                reverse(
                                    'console:screenproduct-change',
                                    kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if formset:
                                context.update({'prd_university_payment_formset': formset})
                            messages.error(
                                self.request,
                                "University Course Change Failed, \
                                Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/vendor/change_screenproduct.html"
                                ], context)
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:screenproduct-change', kwargs={'pk': prd}))
            except Exception as e:
                messages.error(request, (
                    ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
                logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})

                return HttpResponseRedirect(
                    reverse('console:screenproduct-change', kwargs={'pk': prd}))
        return HttpResponseBadRequest()


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.VENDOR_GROUP_LIST, settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_change_product'))
class AddScreenProductVariantView(DetailView):
    template_name = 'console/vendor/add_screenvariant.html'
    model = ProductScreen

    def dispatch(self, request, *args, **kwargs):
        return super(
            AddScreenProductVariantView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        if not product:
            raise Http404
        if not product.type_product == 1:
            raise Http404
        if has_group(user=self.request.user, grp_list=settings.PRODUCT_GROUP_LIST):
            pass
        else:
            user_vendor = self.request.user.get_vendor()
            if not user_vendor:
                return HttpResponseForbidden()
            if user_vendor != product.vendor:
                return HttpResponseForbidden() 
        
        return super(
            AddScreenProductVariantView, self).get(request, args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(
                AddScreenProductVariantView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(
            AddScreenProductVariantView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        main_change_form = AddScreenProductVariantForm(parent=self.get_object(),
            user=self.request.user)
        context.update({
            'messages': alert,
            'form': main_change_form,
            })
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST or self.request.FILES:
            try:
                obj = int(self.kwargs.get('pk', None))
                prd = int(request.POST.get('product'))
                if obj == prd:
                    obj = self.object = self.get_object()
                    slug = request.POST.get('slug', None)
                    if not obj.type_product == 1:
                        messages.error(
                        self.request,
                        "Product is not parent variation")
                        return HttpResponseRedirect(reverse('console:screenproduct-change',kwargs={'pk': obj.pk}))
                        
                    if has_group(user=self.request.user, grp_list=settings.PRODUCT_GROUP_LIST):
                        pass
                    else:
                        user_vendor = self.request.user.get_vendor()
                        if not user_vendor:
                            messages.error(
                            self.request,
                            "You are not associated to any vendor")
                            return HttpResponseRedirect(reverse('console:screenproduct-change',kwargs={'pk': obj.pk}))
                        if user_vendor != obj.vendor:
                            messages.error(
                            self.request,
                            "Product not associated to your vendor")
                            return HttpResponseRedirect(reverse('console:screenproduct-change',kwargs={'pk': obj.pk}))
                    
                    form = None
                    if slug == 'variant':
                        form = AddScreenProductVariantForm(
                                request.POST, request.FILES,
                                parent=obj,
                                user=self.request.user)
                        if form.is_valid():
                            prods = form.save()
                            prods.type_product = 2
                            prods.product_class = obj.product_class
                            prods.type_flow = obj.type_flow
                            prods.vendor = obj.vendor
                            prods.save()
                            prods.create_product()
                            obj.add_variant(prods)
                            if not obj.status == 2:    
                                obj.status = 1
                                obj.save()        
                                
                            messages.success(
                                self.request,
                                "Product Changed Successfully")
                            return HttpResponseRedirect(reverse('console:screenproduct-change',kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'form': form})
                            messages.error(
                                self.request,
                                "Product Variant Add Failed, Saved")
                            return TemplateResponse(
                                request, [
                                    "console/vendor/add_screenvariant.html"
                                ], context)
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:screenproductvariant-add', kwargs={'pk': prd}))
            except Exception as e:
                messages.error(request, (
                    ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
                logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})

                return HttpResponseRedirect(
                    reverse('console:screenproductvariant-add', kwargs={'pk': prd}))
        return HttpResponseBadRequest()


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.VENDOR_GROUP_LIST, settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_change_product'))
class ChangeScreenProductVariantView(DetailView):
    template_name = 'console/vendor/change_screenvariant.html'
    model = ProductScreen

    def dispatch(self, request, *args, **kwargs):
        return super(
            ChangeScreenProductVariantView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        if not product:
            raise Http404
        if not product.type_product == 2:
            raise Http404
        if has_group(user=self.request.user, grp_list=settings.PRODUCT_GROUP_LIST):
            pass
        else:
            user_vendor = self.request.user.get_vendor()
            if not user_vendor:
                return HttpResponseForbidden()
            if user_vendor != product.vendor:
                return HttpResponseForbidden() 
        return super(
            ChangeScreenProductVariantView, self).get(request, args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(
                ChangeScreenProductVariantView, self).get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super(
            ChangeScreenProductVariantView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        pk_parent = kwargs.get('parent',None)
        parent = self.get_object().get_parent()
        
        main_change_form = AddScreenProductVariantForm(parent=parent,
            user=self.request.user, instance=self.get_object())
        context.update({
            'messages': alert,
            'form': main_change_form,
            'parent': parent.pk if parent else None
            })
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST or self.request.FILES:
            try:
                obj = int(self.kwargs.get('pk', None))
                parent = int(self.kwargs.get('parent', None))
                prd = int(request.POST.get('product'))
                if obj == prd:
                    obj = self.object = self.get_object()
                    slug = request.POST.get('slug', None)
                    form = None
                    if not obj.type_product == 2:
                        messages.error(
                        self.request,
                        "Product is not child variation")
                        return HttpResponseRedirect(
                            reverse('console:screenproductvariant-change', kwargs={'pk': prd, 'parent': parent}))
                    if has_group(user=self.request.user, grp_list=settings.PRODUCT_GROUP_LIST):
                        pass
                    else:
                        user_vendor = self.request.user.get_vendor()
                        if not user_vendor:
                            messages.error(
                            self.request,
                            "You are not associated to any vendor")
                            return HttpResponseRedirect(
                                reverse('console:screenproductvariant-change', kwargs={'pk': prd, 'parent': parent}))
                        if user_vendor != obj.vendor:
                            messages.error(
                            self.request,
                            "Product not associated to your vendor")
                            return HttpResponseRedirect(
                                reverse('console:screenproductvariant-change', kwargs={'pk': prd, 'parent': parent}))
                    if slug == 'variant':
                        parent = self.get_object().get_parent()
                        form = AddScreenProductVariantForm(
                            request.POST, request.FILES,
                            parent=parent,
                            user=self.request.user,
                            instance=obj)

                        if form.is_valid():
                            productscreen = form.save()
                            productscreen.status = 1
                            productscreen.save()        
                            if not parent.status == 2:    
                                parent.status = 1
                                parent.save()

                            messages.success(
                                self.request,
                                "Product Changed Successfully")
                            return HttpResponseRedirect(
                                reverse('console:screenproductvariant-change',
                                    kwargs={'pk': obj.pk, 'parent': parent.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'form': form})
                            messages.error(
                                self.request,
                                "Product Variant Add Failed, Saved")
                            return TemplateResponse(
                                request, [
                                    "console/vendor/change_screenvariant.html"
                                ], context)
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:screenproductvariant-change', kwargs={'pk': prd, 'parent': parent}))
            except Exception as e:
                messages.error(request, (
                    ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))

                logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})

                return HttpResponseRedirect(
                    reverse('console:screenproductvariant-change', kwargs={'pk': prd, 'parent': parent}))
        return HttpResponseBadRequest()


@Decorate(check_group([settings.VENDOR_GROUP_LIST, settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_change_product'))
class ActionScreenFaqView(View):

    def post(self, request, *args, **kwargs):
        try:
            form_data = self.request.POST
            action = form_data.get('action', None)
            pk_obj = form_data.get('screenfaq', None)
            allowed_action = []
            if has_group(user=self.request.user, grp_list=settings.PRODUCT_GROUP_LIST):
                allowed_action = ['approval', 'live', 'revert', 'reject']
            elif has_group(user=self.request.user, grp_list=settings.VENDOR_GROUP_LIST):
                allowed_action = ['approval']

            if action and action in allowed_action:
                try:
                    screenfaq = ScreenFAQ.objects.get(pk=pk_obj)
                    faq = screenfaq.faq
                    if not faq:
                        faq = screenfaq.create_faq()
                    if action == "approval":
                        screenfaq.status = 2
                        screenfaq.save()
                        messages.success(
                            self.request,
                                "FAQ is assigned to product for moderation!") 
                        data = {'success': 'True', 'next_url': reverse('console:screenfaq-list') }
                    elif action == "live":
                        faq.text = screenfaq.text
                        faq.answer = screenfaq.answer
                        faq.vendor = screenfaq.vendor
                        faq.sort_order = screenfaq.sort_order
                        screenfaq.status = 3
                        screenfaq.save()
                        faq.status = 2
                        faq.save()
                        messages.success(
                            self.request,
                                "FAQ is copied to live!") 
                        data = {'success': 'True', 'next_url': reverse('console:screenfaq-moderationlist') }
                    elif action == "reject":
                        screenfaq.status = 5
                        screenfaq.save()
                        messages.success(
                            self.request,
                                "FAQ changes is rejected!") 
                        data = {'success': 'True', 'next_url': reverse('console:screenfaq-moderationlist') }
                    elif action == "revert":
                        screenfaq.text = faq.text
                        screenfaq.answer = faq.answer
                        screenfaq.vendor = faq.vendor
                        screenfaq.sort_order = screenfaq.sort_order
                        screenfaq.status = 6
                        screenfaq.save()
                        messages.success(
                            self.request,
                                "FAQ changes is reverted!") 
                        data = {'success': 'True', 'next_url': reverse('console:screenfaq-moderationlist') }
                except Exception as e:
                    logging.getLogger('error_log').error(str(e))
                    data = {'error': 'True'}
                    messages.error(
                        self.request,
                        "Object Do not Exists!")    
            else:
                data = {'error': 'True'}
                messages.error(
                    self.request,
                    "Invalid Action, Do not have permission!")
            return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception as e:
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
            logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})

        data = {'error': 'True'}
        return HttpResponse(json.dumps(data), content_type="application/json")


@Decorate(check_group([settings.VENDOR_GROUP_LIST, settings.PRODUCT_GROUP_LIST]))
@Decorate(check_permission('shop.console_change_product'))
class ActionScreenProductView(View, ProductModeration):

    def post(self, request, *args, **kwargs):
        try:
            form_data = self.request.POST
            
            action = form_data.get('action', None)
            pk_obj = form_data.get('screenproduct', None)
            allowed_action = []
            groups = self.request.user.groups.all().values_list('name', flat=True)
            if has_group(user=self.request.user, grp_list=settings.PRODUCT_GROUP_LIST):
                allowed_action = ['approval', 'live', 'revert', 'reject']
            elif has_group(user=self.request.user, grp_list=settings.VENDOR_GROUP_LIST):
                allowed_action = ['approval']

            if action and action in allowed_action:
                try:
                    productscreen = ProductScreen.objects.get(pk=pk_obj)
                    product = productscreen.product
                    if not product:
                        product = productscreen.create_product()
                    if action == "approval":
                        if self.validate_screenproduct(request=self.request,productscreen=productscreen): 
                            productscreen.status = 2
                            productscreen.save()
                            messages.success(
                                self.request,
                                    "Product is assigned for moderation!") 
                            data = {'success': 'True',
                                'next_url': reverse('console:screenproduct-list') }
                        else:
                            data = {'error': 'True'}
                    elif action == "reject":
                        productscreen.status = 5
                        productscreen.save()
                        messages.success(
                            self.request,
                                "Product changes is rejected!") 
                        data = {'success': 'True',
                            'next_url': reverse('console:screenproduct-moderationlist') }
                    elif action == "live":
                        if self.validate_screenproduct(request=self.request,productscreen=productscreen): 
                            product, productscreen, copied = self.copy_to_product(
                                request=self.request,
                                product=product,
                                screen=productscreen)
                            if copied:
                                productscreen.status = 3
                                productscreen.save()
                                product.is_indexable = False
                                product.save()
                                if product.type_product == 1:
                                    childs = product.mainproduct.all()
                                    for child in childs:
                                        sibling = child.sibling
                                        sibling.is_indexable = False
                                        sibling.save()
                                messages.success(
                                    self.request,
                                        "Product Screen is copied to live! Please validate fields in live product") 
                                data = {'success': 'True',
                                    'next_url': reverse('console:product-change', kwargs={'pk': product.pk}) }
                            else:
                                messages.error(
                                    self.request,
                                        "Product Screen copy Failed!") 
                                data = {'error': True,}
                        else:
                            messages.error(
                                    self.request,
                                        "Product Screen copy Failed!") 
                            data = {'error': 'True'}
                    elif action == "revert":
                        product, productscreen, copied = self.copy_to_screen(
                            request=self.request,
                            product=product,
                            screen=productscreen)
                        if copied:
                            productscreen.status = 6
                            productscreen.save()
                            messages.success(
                                self.request,
                                    "Product Screen is changes is reverted!") 
                            data = {'success': 'True', 'next_url': reverse('console:screenproduct-moderationlist') }
                        else:
                            messages.error(
                                self.request,
                                    "Product Screen revert Failed!") 
                            data = {'error': True,}
                except Exception as e:
                    logging.getLogger('error_log').error(str(e))
                    data = {'error': 'True'}
                    messages.error(
                        self.request,
                        "Object Do not Exists!")    
            else:
                data = {'error': 'True'}
                messages.error(
                    self.request,
                    "Invalid Action, Do not have permission!")
            return HttpResponse(json.dumps(data), content_type="application/json")
        except Exception as e:
            messages.error(request, (
                ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
            logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})

        data = {'error': 'True'}
        return HttpResponse(json.dumps(data), content_type="application/json")


