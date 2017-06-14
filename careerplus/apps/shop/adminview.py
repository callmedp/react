# from django.views.generic import FormView, ListView, UpdateView
# from django.contrib import messages
# from django.core.paginator import Paginator
# from django.db.models import Q

# from .forms import ProductAddForm
# from shop.models import Product
# from partner.models import Vendor
# from blog.mixins import PaginationMixin


# class ProductAddFormView(FormView):
#     template_name = "productadmin/product_add.html"
#     success_url = "/shop/admin/product-add/"
#     http_method_names = [u'get', u'post']
#     form_class = ProductAddForm

#     def get(self, request, *args, **kwargs):
#         return super(self.__class__, self).get(request, args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super(self.__class__, self).get_context_data(**kwargs)
#         alert = messages.get_messages(self.request)
        
#         context.update({
#             'messages': alert,
#         })
#         return context

#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         if form.is_valid():
#             try:
#                 form.save()
#                 messages.add_message(request, messages.SUCCESS, 'Skill Page Created Successfully.')
#                 return self.form_valid(form)
#             except:
#                 messages.add_message(request, messages.ERROR, 'Skill Page Not Created.')
#                 return self.form_invalid(form)
#         return self.form_invalid(form)


# class ProductListView(ListView, PaginationMixin):

#     context_object_name = 'product_list'
#     template_name = 'productadmin/product-list.html'
#     model = Product
#     http_method_names = [u'get', u'post']
#     page = 1
#     paginated_by = 5
#     query = ''

#     def get(self, request, *args, **kwargs):
#         self.page = request.GET.get('page', 1)
#         self.query = request.GET.get('query', '')
#         return super(self.__class__, self).get(request, args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super(self.__class__, self).get_context_data(**kwargs)
#         paginator = Paginator(context['product_list'], self.paginated_by)
#         context.update(self.pagination(paginator, self.page))
#         context.update({
#             "query": self.query,
#         })
#         return context

#     def get_queryset(self):
#         queryset = super(self.__class__, self).get_queryset()
#         try:
#             if self.query:
#                 queryset = queryset.filter(Q(name__icontains=self.query))
#         except:
#             pass
#         return queryset


# class ProductUpdateView(UpdateView):
#     model = Product
#     template_name = 'productadmin/product-update.html'
#     success_url = "/shop/admin/product-list/"
#     http_method_names = [u'get', u'post']
#     form_class = ProductAddForm

#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super(self.__class__, self).get(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super(self.__class__, self).get_context_data(**kwargs)
#         alert = messages.get_messages(self.request)
#         context.update({
#             'slug': self.object.slug,
#             'messages': alert})
#         return context

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             try:
#                 form.save()
#                 messages.add_message(request, messages.SUCCESS,
#                     'Product %s Updated Successfully.' % (self.object.id))
#                 return self.form_valid(form)
#             except:
#                 messages.add_message(request, messages.ERROR, 'Product Not Updated.')
#                 return self.form_invalid(form)
#         return self.form_invalid(form)
