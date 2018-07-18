from django.views.generic import ListView, UpdateView
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
import logging

from blog.mixins import PaginationMixin

from .models import Country
from .forms import CountryUpdateForm

from console.decorators import (
    Decorate,
    check_group, stop_browser_cache
)

@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
class CountryUpdateView(UpdateView):
	model = Country
	template_name = 'geoadmin/country-update.html'
	success_url = "/console/geolocation/country/"
	http_method_names = [u'get', u'post']
	form_class = CountryUpdateForm

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
				valid_form = self.form_valid(form)
				messages.add_message(request, messages.SUCCESS,
					'Country %s Updated Successfully.' % (self.object.id))
				return valid_form
			except Exception as e:
				messages.add_message(request, messages.ERROR, 'Country %s Not Updated. due to %s' % (self.object.id, str(e)))
				return self.form_invalid(form)
		return self.form_invalid(form)

@Decorate(stop_browser_cache())
@Decorate(check_group([settings.PRODUCT_GROUP_LIST]))
class CountryListView(ListView, PaginationMixin):

	context_object_name = 'country_list'
	template_name = 'geoadmin/country-list.html'
	model = Country
	http_method_names = [u'get', ]

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
		paginator = Paginator(context['country_list'], self.paginated_by)
		context.update(self.pagination(paginator, self.page))
		alert = messages.get_messages(self.request)
		context.update({
			"query": self.query,
			"messages": alert,
		})
		return context

	def get_queryset(self):
		queryset = super(self.__class__, self).get_queryset()
		try:
			if self.query:
				queryset = queryset.filter(Q(name__icontains=self.query) | Q(code2__icontains=self.query) | Q(code3__icontains=self.query) | Q(phone__icontains=self.query))
		except Exception as e:
			logging.getLogger('error_log').error('unable to get queryset%s' % str(e))
			pass
		return queryset