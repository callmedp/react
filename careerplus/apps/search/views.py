# built-in imports
import re

# django imports
from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.http import Http404
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect

# third party imports

# local imports
# from shinecp.gosf.forms import GosfFilterForm
# from shinecp.gosf.views import ProductVariationListView, CommonContext
# from shinecp.theme.utils import is_mobile_browser


class SearchQueryView(ListView):

    template_name = 'search/listing.html'
    initial = {'price_from': 0, 'price_to': 0}
    search_type = ""

    # def get_initial(self):
    #     if hasattr(self, '_initial'):
    #         return self._initial
    #     initial = self.initial.copy()
    #     variation = self.request.session.get('variation')
    #     keyword = self.request.POST.get('keyword')
    #
    #     if not is_mobile_browser(self.request):
    #         mobile_browser = False
    #     else:
    #         mobile_browser = True
    #
    #     initial.update(
    #         {'search': 1, 'keyword': keyword,
    #          'mobile_browser': mobile_browser})
    #
    #     if 'price_to' not in initial or initial['price_to'] == 0:
    #         initial.update({
    #             'price_to': CommonContext.get_price_slider_max_price()
    #             })
    #     self._initial = initial
    #     return initial

    def render_to_response(self, context, **response_kwargs):
        response = super(SearchQueryView, self).render_to_response(
            context, **response_kwargs)
        return response

    # def get_context_data(self, **kwargs):
    #
    #     context = super(self.__class__, self).get_context_data(**kwargs)
    #     pv_list_response = ProductVariationListView.as_view()(
    #         request=self.request, **context)
    #     context.update({'search': 1})
    #     context.update(pv_list_response.context_data)
    #     context.update(self.get_common_context_data())
    #     return context

    # def get(self, request, *args, **kwargs):
    #     request.method = 'POST'
    #     request.POST = request.GET.copy()
    #
    #     q_search=request.GET.get('q', '').strip().replace('-', ' ')
    #     if q_search:
    #
    #         q_search = re.sub(r'[^\d\w\s\?%-()*]', '',q_search[:50] )
    #
    #         request.POST.update(
    #             {'keyword':q_search})
    #
    #         [request.POST.update(
    #             {key: value}) for key, value in self.get_initial().iteritems() if
    #             key not in request.POST]
    #         mobile_browser = request.POST['mobile_browser']
    #         if mobile_browser:
    #             self.template_name = 'mobile/listing.html'
    #         form = GosfFilterForm(request.GET or request.POST)
    #         self.kwargs.update({'form': form})
    #         self.form = form
    #
    #         if form.is_valid():
    #             self.keyword = form.cleaned_data['keyword']
    #             self.location = form.cleaned_data['location']
    #
    #         return super(self.__class__, self).post(self, request, *args, **kwargs)
    #     else:
    #         return HttpResponseRedirect(reverse_lazy('gosf:gosf_home'))

    def post(self, request, form=None):
        return self.get(self).get(request)

    def form_valid(self, form):
        self.form = form
        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        raise Http404


class SearchListView(ListView):
    # form_class = GosfFilterForm
    # template_name = 'listing/search_v3.html'#'gosf/search.html'
    # initial = {'price_from': 0, 'price_to': 0}

    # def get_initial(self):
    #     if hasattr(self, '_initial'):
    #         return self._initial
    #     initial = self.initial.copy()
    #     variation = self.request.session.get('variation')
    #     keyword = self.request.POST.get('keyword')
    #     location = self.request.POST.get('location')
    #
    #     if not is_mobile_browser(self.request):
    #         mobile_browser = False
    #     else:
    #         mobile_browser = True
    #
    #     initial.update(
    #         {'search': 1, 'keyword': keyword,
    #          'location': location,
    #          'mobile_browser': mobile_browser})
    #
    #     if 'price_to' not in initial or initial['price_to'] == 0:
    #         initial.update({
    #             'price_to': CommonContext.get_price_slider_max_price()
    #             })
    #     self._initial = initial
    #     return initial

    def render_to_response(self, context, **response_kwargs):
        response = super(SearchListView, self).render_to_response(
            context, **response_kwargs)
        return response

    # def get_context_data(self, **kwargs):
    #
    #     context = super(self.__class__, self).get_context_data(**kwargs)
    #     pv_list_response = ProductVariationListView.as_view()(
    #         request=self.request, **context)
    #     context.update({'search': 1})
    #     context.update(pv_list_response.context_data)
    #     context.update(self.get_common_context_data())
    #     return context

    # def get(self, request, *args, **kwargs):
    #     request.method = 'POST'
    #     request.POST = request.GET.copy()
    #
    #     if 'keyword_in_url' in kwargs:
    #         request.POST.update(
    #             {'keyword': kwargs['keyword_in_url'].replace('-', ' ')})
    #
    #     if 'location' in kwargs:
    #         request.POST.update(
    #             {'location': kwargs['location'].replace('-', ' ')})
    #
    #     [request.POST.update(
    #         {key: value}) for key, value in self.get_initial().iteritems() if key not in request.POST]
    #     mobile_browser = request.POST['mobile_browser']
    #     if mobile_browser:
    #         self.template_name = 'mobile/listing.html'
    #     form = GosfFilterForm(request.GET or request.POST)
    #     self.kwargs.update({'form': form})
    #     self.form = form
    #
    #     if form.is_valid():
    #         self.keyword = form.cleaned_data['keyword']
    #         self.location = form.cleaned_data['location']
    #
    #     return super(self.__class__, self).post(self, request, *args, **kwargs)

    def post(self, request, form=None):
        return self.get(self).get(request)

    def form_valid(self, form):
        self.form = form
        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        raise Http404


class TestListingView(TemplateView):
    template_name = 'search/listing.html'