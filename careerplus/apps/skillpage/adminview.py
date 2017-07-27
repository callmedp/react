# from django.views.generic import FormView, ListView, UpdateView
# from django.contrib import messages
# from django.core.paginator import Paginator
# from django.db.models import Q

# from .forms import SkillAddForm
# from shop.models import Category, ProductCategory
# from blog.mixins import PaginationMixin


# class SkillAddFormView(FormView):
#     template_name = "skillpageadmin/skill-add.html"
#     success_url = "/skillpage/admin/skill-add/"
#     http_method_names = [u'get', u'post']
#     form_class = SkillAddForm

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


# class SkillListView(ListView, PaginationMixin):

#     context_object_name = 'category_list'
#     template_name = 'skillpageadmin/skill-list.html'
#     model = Category
#     http_method_names = [u'get', u'post']
#     page = 1
#     paginated_by = 50
#     query = ''

#     def get(self, request, *args, **kwargs):
#         self.page = request.GET.get('page', 1)
#         self.query = request.GET.get('query', '')
#         return super(self.__class__, self).get(request, args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super(self.__class__, self).get_context_data(**kwargs)
#         paginator = Paginator(context['category_list'], self.paginated_by)
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


# class SkillUpdateView(UpdateView):
#     model = Category
#     template_name = 'skillpageadmin/skill-update.html'
#     success_url = "/skillpage/admin/skill-list/"
#     http_method_names = [u'get', u'post']
#     form_class = SkillAddForm

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
#                     'Skill %s Updated Successfully.' % (self.object.id))
#                 return self.form_valid(form)
#             except:
#                 messages.add_message(request, messages.ERROR, 'Skill Not Updated.')
#                 return self.form_invalid(form)
#         return self.form_invalid(form)
