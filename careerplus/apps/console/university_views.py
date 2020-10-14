# python imports
import logging

# Django imports
from django.views.generic import (
    FormView, ListView, DetailView)
from django.contrib import messages
from django.db.models import Q
from django.http import (
    HttpResponseForbidden,
    HttpResponseRedirect, HttpResponseBadRequest)
from django.core.paginator import Paginator
from django.template.response import TemplateResponse
from django.forms.models import inlineformset_factory
from django.urls import reverse_lazy, reverse
# third party imports

# local imports
from blog.mixins import PaginationMixin
from .decorators import (
    Decorate,
    check_permission, stop_browser_cache)
from shop.models import (
    Faculty)
from .shop_form import (
    AddFacultyForm, ChangeFacultyForm,
    FacultyCourseForm, FacultyCourseInlineFormSet)


@Decorate(stop_browser_cache())
@Decorate(check_permission('shop.console_change_faculty'))
class FacultyChangeView(DetailView):
    model = Faculty
    template_name = 'console/university/change_faculty.html'

    def dispatch(self, request, *args, **kwargs):
        return super(FacultyChangeView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self, 'object'):
            return self.object
        else:
            return super(FacultyChangeView, self).get_object(queryset)

    def get(self, request, *args, **kwargs):
        return super(FacultyChangeView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FacultyChangeView, self).get_context_data(**kwargs)
        FacultyCourseFormSet = inlineformset_factory(
            Faculty, Faculty.products.through, fk_name='faculty',
            form=FacultyCourseForm,
            can_delete=False,
            formset=FacultyCourseInlineFormSet, extra=1,
            max_num=20, validate_max=True)

        alert = messages.get_messages(self.request)
        main_change_form = ChangeFacultyForm(
            instance=self.get_object())

        course_formset = FacultyCourseFormSet(
            instance=self.get_object(),
            form_kwargs={'object': self.get_object()})
        context.update({'course_formset': course_formset})

        context.update({
            'messages': alert,
            'form': main_change_form, })
        return context

    def post(self, request, *args, **kwargs):
        if self.request.POST or self.request.FILES:
            try:
                obj = int(self.kwargs.get('pk', None))
                faculty = int(request.POST.get('faculty'))
                if obj == faculty:
                    obj = self.object = self.get_object()
                    slug = request.POST.get('slug', None)
                    form = None
                    if slug == 'main':
                        form = ChangeFacultyForm(
                            request.POST, request.FILES, instance=obj)
                        if form.is_valid():
                            form.save()
                            url = obj.get_full_url()
                            Faculty.objects.filter(pk=obj.pk).update(url=url)
                            messages.success(
                                self.request,
                                "Faculty Changed Successfully")
                            return HttpResponseRedirect(
                                reverse(
                                    'console:faculty-change',
                                    kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if form:
                                context.update({'form': form})
                            messages.error(
                                self.request,
                                "Faculty Object Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/university/change_faculty.html"
                                ], context)

                    elif slug == 'course':
                        FacultyCourseFormSet = inlineformset_factory(
                            Faculty, Faculty.products.through,
                            fk_name='faculty',
                            form=FacultyCourseForm,
                            can_delete=False,
                            formset=FacultyCourseInlineFormSet, extra=1,
                            max_num=20, validate_max=True)

                        formset = FacultyCourseFormSet(
                            request.POST, instance=obj,
                            form_kwargs={'object': obj})
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
                                "Faculty Course changed Successfully")
                            return HttpResponseRedirect(
                                reverse('console:faculty-change', kwargs={'pk': obj.pk}))
                        else:
                            context = self.get_context_data()
                            if formset:
                                context.update({'course_formset': formset})
                            messages.error(
                                self.request,
                                "Faculty Course Change Failed, Changes not Saved")
                            return TemplateResponse(
                                request, [
                                    "console/university/change_faculty.html"
                                ], context)
                messages.error(
                    self.request,
                    "Object Does Not Exists")
                return HttpResponseRedirect(
                    reverse('console:faculty-change',
                        kwargs={'pk': faculty}))
            except Exception as e:
                logging.getLogger('error_log').error("%(msg)s : %(err)s" % {'msg': 'Contact Tech ERROR', 'err': e})
                messages.error(request, (
                    ("%(msg)s : %(err)s") % {'msg': 'Contact Tech ERROR', 'err': e}))
            return HttpResponseRedirect(
                reverse('console:faculty-change', kwargs={'pk': faculty}))
        return HttpResponseBadRequest()


@Decorate(stop_browser_cache())
@Decorate(check_permission('shop.console_add_faculty'))
class FacultyAddView(FormView):
    form_class = AddFacultyForm
    template_name = 'console/university/add_faculty.html'
    http_method_names = ['get', 'post']
    success_url = reverse_lazy('console:faculty-list')

    def get(self, request, *args, **kwargs):
        return super(FacultyAddView, self).get(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FacultyAddView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        return context

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "You have successfully added a Faculty"
        )
        return super(FacultyAddView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Your addition has not been saved. Try again."
        )
        return super(FacultyAddView, self).form_invalid(form)


@Decorate(stop_browser_cache())
@Decorate(check_permission('shop.console_view_faculty'))
class FacultyListView(ListView, PaginationMixin):
    model = Faculty
    context_object_name = 'faculty_list'
    template_name = 'console/university/list_faculty.html'
    http_method_names = [u'get', ]

    def dispatch(self, request, *args, **kwargs):
        self.page = 1
        self.paginated_by = 50
        self.query = ''
        return super(FacultyListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.page = request.GET.get('page', 1)
        self.query = request.GET.get('query', '')
        return super(FacultyListView, self).get(request, args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FacultyListView, self).get_context_data(**kwargs)
        alert = messages.get_messages(self.request)
        context.update({'messages': alert})
        paginator = Paginator(context['faculty_list'], self.paginated_by)
        context.update(self.pagination(paginator, self.page))
        alert = messages.get_messages(self.request)
        context.update({
            "query": self.query,
            "messages": alert,
        })
        return context

    def get_queryset(self):
        queryset = super(FacultyListView, self).get_queryset()

        if self.query:
            queryset = queryset.filter(Q(name__icontains=self.query))

        return queryset.order_by('-modified')