from collections import OrderedDict

from django.views.generic import (
    FormView, TemplateView, ListView, DetailView)
from django.http import (
    HttpResponseRedirect, HttpResponseForbidden, HttpResponseBadRequest)
from django.core import exceptions

from django.forms.models import inlineformset_factory
from django.template.response import TemplateResponse
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from .decorators import Decorate, check_permission, check_group
from django.core.paginator import Paginator
from django.db.models import Q
from shop.choices import PRODUCT_VENDOR_CHOICES
from blog.mixins import PaginationMixin
from shop.models import (
    Product, ProductScreen)
from faq.models import ScreenFAQ, ScreenChapter
from .vendor_form import (
    AddScreenProductForm,
    ChangeScreenProductForm,
    ScreenProductCountryForm,
    ScreenProductPriceForm,
    ScreenProductAttributeForm)


@Decorate(check_group(['Vendor']))
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
        vendor = self.request.user.get_vendor()
        if not vendor:
            queryset = queryset.none()
        else:
            queryset = queryset.filter(vendor=vendor)
        try:
            if self.query:
                queryset = queryset.filter(Q(text__icontains=self.query))
        except:
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


@Decorate(check_group(['Vendor']))
@Decorate(check_permission('faq.console_change_chapter'))
class ListScreenChapterView(ListView, PaginationMixin):
    model = ScreenChapter
    context_object_name = 'screenchapter_list'
    template_name = 'console/vendor/list_chapter_screen.html'
    http_method_names = [u'get', ]

    def dispatch(self, request, *args, **kwargs):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        return super(
            ListScreenChapterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(
            ListScreenChapterView, self).get(request, args, **kwargs)

    def get_queryset(self):
        queryset = super(ListScreenChapterView, self).get_queryset()
        queryset = queryset.filter(parent__isnull=True)
        vendor = self.request.user.get_vendor()
        if not vendor:
            queryset = queryset.none()
        else:
            queryset = queryset.filter(vendor=vendor)
        try:
            if self.query:
                queryset = queryset.filter(Q(heading__icontains=self.query))
        except:
            pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListScreenChapterView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        paginator = Paginator(context['screenchapter_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "query": self.query,
            "messages": alert,
        })
        return context


@Decorate(check_group(['Vendor']))
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
        vendor = self.request.user.get_vendor()
        if not vendor:
            queryset = queryset.none()
        else:
            queryset = queryset.filter(vendor=vendor, type_product__in=dict(PRODUCT_VENDOR_CHOICES).keys())
        try:
            if self.query:
                queryset = queryset.filter(Q(name__icontains=self.query))
        except:
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


@Decorate(check_group(['Vendor']))
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
        context.update({'messages': alert})
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


@Decorate(check_group(['Vendor']))
@Decorate(check_permission('shop.console_change_product'))
class ChangeScreenProductView(DetailView):
    template_name = 'console/vendor/change_screenproduct.html'
    model = ProductScreen

    def dispatch(self, request, *args, **kwargs):
        return super(
            ChangeScreenProductView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
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
        country_form = ScreenProductCountryForm(instance=self.get_object())
        price_form = ScreenProductPriceForm(instance=self.get_object())
        attribute_form = ScreenProductAttributeForm(
            instance=self.get_object(),)

        context.update({
            'messages': alert,
            'form': main_change_form,
            'country_form': country_form,
            'price_form': price_form,
            'attribute_form': attribute_form
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
                    form = None
                    if slug == 'main':
                        form = ChangeScreenProductForm(
                            request.POST, instance=obj, user=self.request.user)
                        if form.is_valid():
                            form.save()
                            messages.success(
                                self.request,
                                "Product Changed Successfully")
                            return HttpResponseRedirect(reverse('console:screenproduct-list',))
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
                            product = form.save(commit=True)
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
                            product = form.save(commit=True)
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
                            product = form.save(commit=True)
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
                                "Product Prices Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/vendor/change_screenproduct.html"
                                ], context)
                    messages.error(
                        self.request,
                        "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:screenproduct-change', kwargs={'pk': prd}))
            except:
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:screenproduct-change', kwargs={'pk': prd}))
        return HttpResponseBadRequest()
