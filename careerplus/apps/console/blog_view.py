import logging
from django.db.models import F

from django.views.generic import FormView, ListView, UpdateView
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.conf import settings
from blog.models import Tag, Category, Blog, Comment, Author
from blog.mixins import PaginationMixin

from .decorators import (
    has_group,
    Decorate, check_permission,
    check_group, stop_browser_cache)

from .blog_form import (
    TagAddForm,
    TagChangeForm,
    CategoryAddForm,
    CategoryChangeForm,
    ArticleFilterForm,
    ArticleAddForm,
    ArticleChangeForm,
    CommentUpdateForm,
    CommentActionForm,
    AuthorAddForm,
    AuthorChangeForm)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.BLOGGER_GROUP_LIST]))
class CommentModerateView(UpdateView):
    model = Comment
    template_name = 'console/blog/comment-moderation-update.html'
    success_url = "/console/blog/comment/comment-to-moderate/"
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
                if obj.is_published:
                    blog = obj.blog
                    blog.comment_moderated += 1
                    blog.save()
                if request.user.is_authenticated:
                    obj.last_modified_by = request.user
                valid_form = self.form_valid(form)
                messages.add_message(request, messages.SUCCESS,
                    'Comment %s Updated Successfully.' % (self.object.id))
                return valid_form
            except Exception as e:
                messages.add_message(request, messages.ERROR, 'Comment %s Not Updated. due to %s' % (self.object.id, str(e)))
                return self.form_invalid(form)
        return self.form_invalid(form)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.BLOGGER_GROUP_LIST]))
class CommentModerateListView(ListView, PaginationMixin):

    context_object_name = 'comment_list'
    template_name = 'console/blog/comment-moderation-list.html'
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
        alert = messages.get_messages(self.request)
        context.update({
            "query": self.query,
            "action_form": CommentActionForm(),
            "messages": alert,
        })
        return context

    def post(self, request, *args, **kwargs):
        try:
            comment_list = request.POST.getlist('table_records', [])
            action_type = int(request.POST.get('action_type', '0'))
            comment_objs = Comment.objects.filter(id__in=comment_list)

            blg_list=list(comment_objs.values_list('blog__id',flat=True))




            if action_type == 0:
                messages.add_message(request, messages.ERROR, 'Please select valid action first')
            elif action_type == 1:
                comment_objs.update(is_published=True)
                Blog.objects.filter(id__in=blg_list).update(comment_moderated=F('comment_moderated') + 1)

                messages.add_message(request, messages.SUCCESS, str(len(comment_list)) + ' Comments are published.')
            elif action_type == 2:
                comment_objs.update(is_removed=True)
                messages.add_message(request, messages.SUCCESS, str(len(comment_list)) + ' Comments removed.')
        except Exception as e:
            messages.add_message(request, messages.ERROR, str(e))

        return HttpResponseRedirect(reverse('console:blog-comment-to-moderate'))

    def get_queryset(self):
        queryset = super(self.__class__, self).get_queryset()
        queryset = queryset.filter(is_published=False, is_removed=False, )
        
        try:
            if self.query:
                queryset = queryset.filter(Q(message__icontains=self.query))
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e)) 
        return queryset


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.BLOGGER_GROUP_LIST]))
class ArticleUpdateView(UpdateView):
    model = Blog
    template_name = 'console/blog/article-change.html'
    success_url = "/console/blog/article/"
    http_method_names = [u'get', u'post']
    form_class = ArticleChangeForm

    def get_form_kwargs(self):
        kwargs = super(ArticleUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

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
                if request.user.is_authenticated:
                    obj.last_modified_by = request.user

                valid_form = self.form_valid(form)
                form.save_m2m()
                messages.add_message(request, messages.SUCCESS,
                    'Blog %s Updated Successfully.' % (self.object.id))
                return valid_form
            except Exception as e:
                messages.add_message(request, messages.ERROR, 'Blog %s Not Updated. Due to %s' % (self.object.id, str(e)))
                return self.form_invalid(form)
        return self.form_invalid(form)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.BLOGGER_GROUP_LIST]))
class ArticleAddView(FormView):
    template_name = "console/blog/article-add.html"
    success_url = "/console/blog/article/"
    http_method_names = [u'get', u'post']
    form_class = ArticleAddForm

    def get_form_kwargs(self):
        kwargs = super(ArticleAddView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

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
                blog = form.save(commit=False)
                if request.user.is_authenticated:
                    blog.created_by = request.user
                    blog.last_modified_by = request.user
                    blog.save()
                valid_form = self.form_valid(form)
                form.save_m2m()
                messages.add_message(request, messages.SUCCESS, 'Blog Created Successfully.')
                return valid_form
            except Exception as e:
                messages.add_message(request, messages.ERROR, 'Blog Not Created. Due to %s' % (str(e)))
                return self.form_invalid(form)
        return self.form_invalid(form)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.BLOGGER_GROUP_LIST]))
class ArticleListView(ListView, PaginationMixin):

    context_object_name = 'article_list'
    template_name = 'console/blog/article-list.html'
    model = Blog
    http_method_names = [u'get', u'post']

    def __init__(self):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        self.sel_status, self.sel_p_cat, self.sel_writer = '-1', '', ''

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '').strip()
        self.sel_status = int(request.GET.get('status', '-1'))
        self.sel_p_cat = request.GET.get('p_cat', '')
        self.sel_writer = request.GET.get('author', '')
        self.visibility = int(request.GET.get('visibility', '-1'))
        self.sortdate = int(request.GET.get('sortdate', '1'))
        return super(self.__class__, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        paginator = Paginator(context['article_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        initial_filter_data = {
            "author": self.sel_writer,
            "p_cat": self.sel_p_cat,
            "status": self.sel_status,
            "visibility":self.visibility,
        }
        filter_form = ArticleFilterForm(initial=initial_filter_data,request=self.request)
        context.update({
            "query": self.query,
            "filter_form": filter_form,
            "sel_status": self.sel_status,
            "sel_p_cat": self.sel_p_cat,
            "sel_writer": self.sel_writer,
            "visibility": self.visibility,
            "sortdate": 0 if self.sortdate == 1 else 1
        })
        return context

    def get_queryset(self):
        queryset = super(self.__class__, self).get_queryset()
        visibility = []
        if has_group(user=self.request.user, grp_list=[settings.LEARNING_BLOGGER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(1)
        if has_group(user=self.request.user, grp_list=[settings.TALENT_BLOGGER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(2)

        if has_group(user=self.request.user, grp_list=[settings.HR_INSIDER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(3)
            visibility.append(4)
            visibility.append(5)


        queryset = queryset.filter(visibility__in=visibility)

        try:
            if self.query:
                queryset = queryset.filter(Q(name__icontains=self.query) |
                    Q(slug__icontains=self.query))
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if self.sel_status != -1:
                queryset = queryset.filter(status=self.sel_status)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if self.sel_p_cat:
                queryset = queryset.filter(p_cat__pk=self.sel_p_cat)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if self.sel_writer:
                queryset = queryset.filter(author__pk=self.sel_writer)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        try:
            if self.visibility and self.visibility != -1:
                queryset = queryset.filter(visibility=self.visibility)
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass

        sort_query = "publish_date" if self.sortdate == 1 else "-publish_date"

        return queryset.select_related('p_cat', 'user', 'created_by',
                                       'last_modified_by').order_by(sort_query)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.BLOGGER_GROUP_LIST]))
class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'console/blog/category-change.html'
    success_url = "/console/blog/category/"
    http_method_names = [u'get', u'post']
    form_class = CategoryChangeForm

    def get_form_kwargs(self):
        kwargs = super(CategoryUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

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
                if request.user.is_authenticated:
                    obj.last_modified_by = request.user

                valid_form = self.form_valid(form)
                messages.add_message(request, messages.SUCCESS,
                    'Category %s Updated Successfully.' % (self.object.id))
                return valid_form
            except Exception as e:
                messages.add_message(request, messages.ERROR, 'Category %s Not Updated. Due to %s' % (self.object.id, str(e)))
                return self.form_invalid(form)
        return self.form_invalid(form)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.BLOGGER_GROUP_LIST]))
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
        visibility = []
        if has_group(user=self.request.user, grp_list=[settings.LEARNING_BLOGGER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(1)
        if has_group(user=self.request.user, grp_list=[settings.TALENT_BLOGGER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(2)
        if has_group(user=self.request.user, grp_list=[settings.HR_INSIDER, settings.PRODUCT_GROUP_LIST]):
            visibility.append(3)
            visibility.append(4)
            visibility.append(5)

        queryset = queryset.filter(visibility__in=visibility)
        
        try:
            if self.query:
                queryset = queryset.filter(Q(name__icontains=self.query))
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass
        return queryset.order_by('-last_modified_on')


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.BLOGGER_GROUP_LIST]))
class CategoryAddView(FormView):
    template_name = "console/blog/category-add.html"
    success_url = "/console/blog/category/"
    http_method_names = [u'get', u'post']
    form_class = CategoryAddForm

    def get_form_kwargs(self):
        kwargs = super(CategoryAddView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

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
                if request.user.is_authenticated:
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


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.BLOGGER_GROUP_LIST]))
class TagUpdateView(UpdateView):
    model = Tag
    template_name = 'console/blog/tag-change.html'
    success_url = "/console/blog/tag/"
    http_method_names = [u'get', u'post']
    form_class = TagChangeForm

    def get_form_kwargs(self):
        kwargs = super(TagUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

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
                if request.user.is_authenticated:
                    obj.last_modified_by = request.user
                valid_form = self.form_valid(form)
                messages.add_message(request, messages.SUCCESS,
                    'Tag Updated Successfully.')
                return valid_form
            except Exception as e:
                messages.add_message(request, messages.ERROR, 'Tag %s Not Updated. Due to %s' % (self.object.id, str(e)))
                return self.form_invalid(form)
        return self.form_invalid(form)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.BLOGGER_GROUP_LIST]))
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
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass
        return queryset.order_by('-last_modified_on')


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.BLOGGER_GROUP_LIST]))
class TagAddView(FormView):
    template_name = "console/blog/tag-add.html"
    success_url = "/console/blog/tag/"
    http_method_names = [u'get', u'post']
    form_class = TagAddForm

    def get_form_kwargs(self):
        kwargs = super(TagAddView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

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
                if request.user.is_authenticated:
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


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.BLOGGER_GROUP_LIST]))
class AuthorAddView(FormView):
    template_name = "console/blog/author-add.html"
    success_url = "/console/blog/author/"
    http_method_names = [u'get', u'post']
    form_class = AuthorAddForm

    def get_form_kwargs(self):
        kwargs = super(AuthorAddView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

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
                author = form.save(commit=False)
                if request.user.is_authenticated:
                    author.created_by = request.user
                    author.last_modified_by = request.user
                    author.save()
                valid_form = self.form_valid(form)
                form.save_m2m()
                messages.add_message(request, messages.SUCCESS, 'Author Created Successfully.')
                return valid_form
            except Exception as e:
                messages.add_message(request, messages.ERROR, 'Author Not Created. Due to %s' % (str(e)))
                return self.form_invalid(form)
        return self.form_invalid(form)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.BLOGGER_GROUP_LIST]))
class AuthorUpdateView(UpdateView):
    model = Author
    template_name = 'console/blog/author-change.html'
    success_url = "/console/blog/author/"
    http_method_names = [u'get', u'post']
    form_class = AuthorChangeForm

    def get_form_kwargs(self):
        kwargs = super(AuthorUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

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
                if request.user.is_authenticated:
                    obj.last_modified_by = request.user

                valid_form = self.form_valid(form)
                form.save_m2m()
                messages.add_message(request, messages.SUCCESS,
                    'Author %s Updated Successfully.' % (self.object.id))
                return valid_form
            except Exception as e:
                messages.add_message(request, messages.ERROR, 'Author %s Not Updated. Due to %s' % (self.object.id, str(e)))
                return self.form_invalid(form)
        return self.form_invalid(form)


@Decorate(stop_browser_cache())
@Decorate(check_group([settings.BLOGGER_GROUP_LIST]))
class AuthorListView(ListView, PaginationMixin):

    context_object_name = 'author_list'
    template_name = 'console/blog/author-list.html'
    model = Author
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
        paginator = Paginator(context['author_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        context.update({
            "query": self.query,
        })
        return context

    def get_queryset(self):
        queryset = super(self.__class__, self).get_queryset()
        # visibility = []
        # if has_group(user=self.request.user, grp_list=[settings.LEARNING_BLOGGER, settings.PRODUCT_GROUP_LIST]):
        #     visibility.append(1)
        # if has_group(user=self.request.user, grp_list=[settings.TALENT_BLOGGER, settings.PRODUCT_GROUP_LIST]):
        #     visibility.append(2)

        # if has_group(user=self.request.user, grp_list=[settings.HR_INSIDER, settings.PRODUCT_GROUP_LIST]):
        #     visibility += [3, 4, 5]

        # queryset = queryset.filter(visibility__in=visibility)
        
        try:
            if self.query:
                queryset = queryset.filter(Q(name__icontains=self.query))
        except Exception as e:
            logging.getLogger('error_log').error("%s " % str(e))
            pass
        return queryset.order_by('-last_modified_on')
