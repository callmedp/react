# python imports


# Django imports
from django.views.generic import (
    FormView, ListView, UpdateView)
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse_lazy, reverse
# third party imports

# local imports
from blog.mixins import PaginationMixin
from shop.models import (
    Faculty)
from .shop_form import (
    AddFacultyForm, ChangeFacultyForm)


class FacultyChangeView(UpdateView):
    model = Faculty
    template_name = 'console/university/change_faculty.html'
    success_url = reverse_lazy('console:faculty-list')
    http_method_names = [u'get', u'post']
    form_class = ChangeFacultyForm

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Your change has not been saved. Try again."
        )
        return super(FacultyChangeView, self).form_invalid(form)

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "You have successfully changed Faculty"
        )
        return super(FacultyChangeView, self).form_valid(form)


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