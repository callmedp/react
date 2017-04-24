from django.views.generic import FormView, ListView, UpdateView
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import TagAddForm, CategoryAddForm, BlogAddForm, ArticleFilterForm,\
    CommentUpdateForm
from .models import Tag, Category, Blog, Comment
from .mixins import PaginationMixin


class CommentUpdateView(UpdateView):
	model = Comment
	template_name = 'blogadmin/comment-update.html'
	success_url = "/article/admin/comment-to-moderate/"
	http_method_names = [u'get', u'post']
	form_class = CommentUpdateForm

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
				# form.save()
				obj = form.save(commit=False)
				if request.user.is_authenticated():
					obj.last_modified_by = request.user
				messages.add_message(request, messages.SUCCESS,
					'Comment %s Updated Successfully.' % (self.object.id))
				return self.form_valid(form)
			except:
				messages.add_message(request, messages.ERROR, 'Comment %s Not Updated.' % (self.object.id))
				return self.form_invalid(form)
		return self.form_invalid(form)


class CommentListView(ListView, PaginationMixin):

	context_object_name = 'comment_list'
	template_name = 'blogadmin/comment-list.html'
	model = Comment
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
		paginator = Paginator(context['comment_list'], self.paginated_by)
		context.update(self.pagination(paginator, self.page))
		context.update({
			"query": self.query,
		})
		return context

	def get_queryset(self):
		queryset = super(self.__class__, self).get_queryset()
		queryset = queryset.filter(is_published=False, is_removed=False)
		try:
			if self.query:
				queryset = queryset.filter(Q(message__icontains=self.query))
		except:
			pass
		return queryset


class BlogUpdateView(UpdateView):
	model = Blog
	template_name = 'blogadmin/article-update.html'
	success_url = "/article/admin/articles/"
	http_method_names = [u'get', u'post']
	form_class = BlogAddForm

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		context = super(self.__class__, self).get(request, *args, **kwargs)
		return context

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
				messages.add_message(request, messages.SUCCESS,
					'Blog %s Updated Successfully.' % (self.object.id))
				return self.form_valid(form)
			except:
				messages.add_message(request, messages.ERROR, 'Blog %s Not Updated.' % (self.object.id))
				return self.form_invalid(form)
		return self.form_invalid(form)


class BlogListView(ListView, PaginationMixin):

	context_object_name = 'article_list'
	template_name = 'blogadmin/article-list.html'
	model = Blog
	http_method_names = [u'get', u'post']

	def __init__(self):
		self.page = 1
		self.paginated_by = 50
		self.query = ''
		self.sel_status, self.sel_p_cat, self.sel_writer = '-1', '', ''

	def get(self, request, *args, **kwargs):
		self.page = request.GET.get('page', 1)
		self.query = request.GET.get('query', '')
		self.sel_status = int(request.GET.get('status', '-1'))
		self.sel_p_cat = request.GET.get('p_cat', '')
		self.sel_writer = request.GET.get('user', '')
		return super(self.__class__, self).get(request, args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(self.__class__, self).get_context_data(**kwargs)
		paginator = Paginator(context['article_list'], self.paginated_by)
		context.update(self.pagination(paginator, self.page))
		initial_filter_data = {
			"user": self.sel_writer,
			"p_cat": self.sel_p_cat,
			"status": self.sel_status
		}
		filter_form = ArticleFilterForm(initial=initial_filter_data)
		context.update({
			"query": self.query,
			"filter_form": filter_form,
			"sel_status": self.sel_status,
			"sel_p_cat": self.sel_p_cat,
			"sel_writer": self.sel_writer
		})
		return context

	def get_queryset(self):
		queryset = super(self.__class__, self).get_queryset()
		try:
			if self.query:
				queryset = queryset.filter(Q(name__icontains=self.query)|
					Q(slug__icontains=self.query))
		except:
			pass

		try:
			if self.sel_status != -1:
				queryset = queryset.filter(status=self.sel_status)
		except:
			pass

		try:
			if self.sel_p_cat:
				queryset = queryset.filter(p_cat__pk=self.sel_p_cat)
		except:
			pass

		try:
			if self.sel_writer:
				queryset = queryset.filter(user__pk=self.sel_writer)
		except:
			pass

		return queryset


class CategoryUpdateView(UpdateView):
	model = Category
	template_name = 'blogadmin/category-update.html'
	success_url = "/article/admin/categories/"
	http_method_names = [u'get', u'post']
	form_class = CategoryAddForm

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
				messages.add_message(request, messages.SUCCESS,
					'Category %s Updated Successfully.' % (self.object.id))
				return self.form_valid(form)
			except:
				messages.add_message(request, messages.ERROR, 'Category Not Updated.')
				return self.form_invalid(form)
		return self.form_invalid(form)


class CategoryListView(ListView, PaginationMixin):

	context_object_name = 'category_list'
	template_name = 'blogadmin/category-list.html'
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


class TagUpdateView(UpdateView):
	model = Tag
	template_name = 'blogadmin/tag-update.html'
	success_url = "/article/admin/tags/"
	http_method_names = [u'get', u'post']
	form_class = TagAddForm

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
				messages.add_message(request, messages.SUCCESS,
					'Tag Updated Successfully.')
				return self.form_valid(form)
			except:
				messages.add_message(request, messages.ERROR, 'Tag Not Updated.')
				return self.form_invalid(form)
		return self.form_invalid(form)


class TagListView(ListView, PaginationMixin):

	context_object_name = 'tag_list'
	template_name = 'blogadmin/tag-list.html'
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


class BlogAddFormView(FormView):
	template_name = "blogadmin/article-add.html"
	success_url = "/article/admin/article-add/"
	http_method_names = [u'get', u'post']
	form_class = BlogAddForm

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
				blog = form.save()
				if request.user.is_authenticated():
					blog.created_by = request.user
					blog.last_modified_by = request.user
					blog.save()
				messages.add_message(request, messages.SUCCESS, 'Blog Created Successfully.')
				return self.form_valid(form)
			except:
				messages.add_message(request, messages.ERROR, 'Blog Not Created.')
				return self.form_invalid(form)
		return self.form_invalid(form)


class TagAddFormView(FormView):
	template_name = "blogadmin/tag-add.html"
	success_url = "/article/admin/tag-add/"
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
				tag = form.save()
				if request.user.is_authenticated():
					tag.created_by = request.user
					tag.last_modified_by = request.user
					tag.save()
				messages.add_message(request, messages.SUCCESS, 'Tag Created Successfully.')
				return self.form_valid(form)
			except:
				messages.add_message(request, messages.ERROR, 'Tag Not Created.')
				return self.form_invalid(form)
		return self.form_invalid(form)


class CategoryAddFormView(FormView):
	template_name = "blogadmin/category-add.html"
	success_url = "/article/admin/category-add/"
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
				category = form.save()
				if request.user.is_authenticated():
					category.created_by = request.user
					category.last_modified_by = request.user
					category.save()
				messages.add_message(request, messages.SUCCESS, 'Category Created Successfully.')
				return self.form_valid(form)
			except:
				messages.add_message(request, messages.ERROR, 'Category Not Created.')
				return self.form_invalid(form)
		return self.form_invalid(form)