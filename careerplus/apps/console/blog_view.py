from django.views.generic import FormView, ListView, UpdateView
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from blog.models import Tag, Category
from blog.mixins import PaginationMixin


from .blog_form import (
	TagAddForm,
	TagChangeForm,
	CategoryAddForm,
	CategoryChangeForm)


class CategoryUpdateView(UpdateView):
	model = Category
	template_name = 'console/blog/category-change.html'
	success_url = "/console/blog/category/"
	http_method_names = [u'get', u'post']
	form_class = CategoryChangeForm

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super(self.__class__, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(self.__class__, self).get_context_data(**kwargs)
		alert = messages.get_messages(self.request)
		context.update({
			'messages': alert})
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			try:
				# form.save()
				obj = form.save(commit=False)
				if request.user.is_authenticated():
					obj.last_modified_by = request.user

				valid_form = self.form_valid(form)
				messages.add_message(request, messages.SUCCESS,
					'Category %s Updated Successfully.' % (self.object.id))
				return valid_form
			except Exception as e:
				messages.add_message(request, messages.ERROR, 'Category %s Not Updated. Due to %s' % (self.object.id, str(e)))
				return self.form_invalid(form)
		return self.form_invalid(form)


class CategoryListView(ListView, PaginationMixin):

	context_object_name = 'category_list'
	template_name = 'console/blog/category-list.html'
	model = Category
	http_method_names = [u'get', u'post']

	def __init__(self):
		self.page = 1
		self.paginated_by = 50
		self.query = ''

	def get(self, request, *args, **kwargs):
		self.page = request.GET.get('page', 1)
		self.query = request.GET.get('query', '')
		return super(self.__class__, self).get(request, args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(self.__class__, self).get_context_data(**kwargs)
		paginator = Paginator(context['category_list'], self.paginated_by)
		context.update(self.pagination(paginator, self.page))
		context.update({
			"query": self.query,
		})
		return context

	def get_queryset(self):
		queryset = super(self.__class__, self).get_queryset()
		try:
			if self.query:
				queryset = queryset.filter(Q(name__icontains=self.query))
		except:
			pass
		return queryset


class CategoryAddView(FormView):
	template_name = "console/blog/category-add.html"
	success_url = "/console/blog/category/"
	http_method_names = [u'get', u'post']
	form_class = CategoryAddForm

	def get(self, request, *args, **kwargs):
		return super(self.__class__, self).get(request, args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(self.__class__, self).get_context_data(**kwargs)
		alert = messages.get_messages(self.request)
		context.update({
			'messages': alert})
		return context

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			try:
				category = form.save(commit=False)
				if request.user.is_authenticated():
					category.created_by = request.user
					category.last_modified_by = request.user
					category.save()
				valid_form = self.form_valid(form)
				messages.add_message(request, messages.SUCCESS, 'Category Created Successfully.')
				return valid_form
			except Exception as e:
				messages.add_message(request, messages.ERROR, 'Category Not Created. Due to %s' % (str(e)))
				return self.form_invalid(form)
		return self.form_invalid(form)


class TagUpdateView(UpdateView):
	model = Tag
	template_name = 'console/blog/tag-change.html'
	success_url = "/console/blog/tag/"
	http_method_names = [u'get', u'post']
	form_class = TagChangeForm

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super(self.__class__, self).get(request, args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(self.__class__, self).get_context_data(**kwargs)
		alert = messages.get_messages(self.request)
		context.update({
			'messages': alert})
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			try:
				obj = form.save(commit=False)
				if request.user.is_authenticated():
					obj.last_modified_by = request.user
				valid_form = self.form_valid(form)
				messages.add_message(request, messages.SUCCESS,
					'Tag Updated Successfully.')
				return valid_form
			except Exception as e:
				messages.add_message(request, messages.ERROR, 'Tag %s Not Updated. Due to %s' % (self.object.id, str(e)))
				return self.form_invalid(form)
		return self.form_invalid(form)


class TagListView(ListView, PaginationMixin):

	context_object_name = 'tag_list'
	template_name = 'console/blog/tag-list.html'
	model = Tag
	http_method_names = [u'get', u'post']

	def __init__(self):
		self.page = 1
		self.paginated_by = 50
		self.query = ''

	def get(self, request, *args, **kwargs):
		self.page = request.GET.get('page', 1)
		self.query = request.GET.get('query', '')
		return super(self.__class__, self).get(request, args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(self.__class__, self).get_context_data(**kwargs)
		paginator = Paginator(context['tag_list'], self.paginated_by)
		context.update(self.pagination(paginator, self.page))
		context.update({
			"query": self.query,
		})
		return context

	def get_queryset(self):
		queryset = super(self.__class__, self).get_queryset()
		try:
			if self.query:
				queryset = queryset.filter(Q(name__icontains=self.query))
		except:
			pass
		return queryset


class TagAddView(FormView):
	template_name = "console/blog/tag-add.html"
	success_url = "/console/blog/tag/"
	http_method_names = [u'get', u'post']
	form_class = TagAddForm

	def get(self, request, *args, **kwargs):
		return super(self.__class__, self).get(request, args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(self.__class__, self).get_context_data(**kwargs)
		alert = messages.get_messages(self.request)
		context.update({
			'messages': alert})
		return context

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			try:
				tag = form.save(commit=False)
				if request.user.is_authenticated():
					tag.created_by = request.user
					tag.last_modified_by = request.user
					tag.save()
				valid_form = self.form_valid(form)
				messages.add_message(request, messages.SUCCESS, 'Tag Created Successfully.')
				return valid_form
			except Exception as e:
				messages.add_message(request, messages.ERROR, 'Tag Not Created. Due to %s' % (str(e)))
				return self.form_invalid(form)
		return self.form_invalid(form)