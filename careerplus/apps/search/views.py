# built-in imports
import re

# django imports
from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.http import QueryDict, Http404
from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.conf import settings

# third party imports
# from haystack.views import SearchView
from haystack.query import EmptySearchQuerySet

# local imports
# from shinecp.gosf.forms import GosfFilterForm
# from shinecp.gosf.views import ProductVariationListView, CommonContext
# from shinecp.theme.utils import is_mobile_browser
from .forms import SearchForm
from .classes import SimpleSearch, SimpleParams

RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)

class SearchQueryView(ListView):

    template_name = 'search/search.html'
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


# class SearchListView():
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

    # def render_to_response(self, context, **response_kwargs):
    #     response = super(SearchListView, self).render_to_response(
    #         context, **response_kwargs)
    #     return response

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

    # def post(self, request, form=None):
    #     return self.get(self).get(request)
    #
    # def form_valid(self, form):
    #     self.form = form
    #     return self.render_to_response(self.get_context_data(form=form))
    #
    # def form_invalid(self, form):
    #     raise Http404
    #
    # def get_queryset(self):
    #     return self.get_results()

    # def list(self, request, *args, **kwargs):
    #     sqs = self.get_results()
    #     data = self.paginator.paginate_queryset(sqs, request)
    #     serializer = self.get_serializer(data, many=True)
    #     return self.paginator.get_paginated_response(serializer.data)


class SearchBaseView(TemplateView):
    template = 'search/search.html'
    ajax_template_name = 'search/ajax/search_listing.html'
    allow_empty_query = True
    clean_query = True
    extra_context = {}
    query_param_name = "q"
    query = ''
    results = EmptySearchQuerySet()
    request = None
    form = None
    results_per_page = RESULTS_PER_PAGE
    search_class = None
    params_class = None
    session_key = "searchquery"
    search_type = ""

    def prepare_response(self):
        """
        Handle both GET and POST requests in the same way.
        """
        if not self.search_class:
            self.search_class = self.get_search_class()
        self.get_search_params()
        response = self.pre_processor()
        if response:
            return response
        self.get_search_query()
        self.empty_query_handler()
        self.get_results()
        response = self.post_processor()    # Handle relaxation.
        if response:
            return response

        return self.create_response()

    def get_search_class(self):
        """
        Search class must be defined for all the extending views.
        The search class performs all the computations.
        Raise an exception if the search class is not defined.
        """
        if not hasattr(self, 'search_class'):
            raise ImproperlyConfigured("'%s' must define search_class" % self.__class__.__name__)

        return self.search_class

    def get_params_class(self):

        if not hasattr(self, 'params_class'):
            raise ImproperlyConfigured("'%s' must define params_class" % self.__class__.__name__)

        return self.params_class

    def get_search_params(self):
        self.params_class_obj = self.params_class(self.args, self.kwargs, self.request)
        self.search_params = self.params_class_obj.get_search_params()

    def get_search_query(self):
        self.query = self.params_class_obj.get_search_query()

    def pre_processor(self):
        """
        Called before any other processing
        """
        pass

    def empty_query_handler(self):
        """
        Prevent further processing if empty query.
        Render response directly. No relaxing/redirects required.
        """
        if (not self.query and not self.allow_empty_query) or self.none_query:
            self.results = EmptySearchQuerySet()
            return self.create_response()

    def get_fields(self):
        """
        List here all the fields needed.
        If not mentioned, all the fields will be returned.
        """
        return []

    def get_results(self):
        """
        This gets the results from search_class.
        Instantiates the search_class, sets params and gets results.
        """
        search_class_obj = self.search_class()
        search_class_obj.set_params(self.search_params)
        search_class_obj.user = self.request.user
        search_class_obj.query = self.query
        self.results = search_class_obj.get_results()

    def post_processor(self):
        """
        Called just before building response and after results are generated
        """
        pass

    def get_extra_context(self):
        """
        Returns extra context to be passed to the template. List is maintained in
        'extra_context' dictionary

        In case you want to override and have a completely new mapping, just define
        the dictionary in your extended class.

        In case you want to append more facets to existing dictionary then you are
        suppose to override this method and return updated dictionary
        """
        context = self.extra_context.copy()
        context['searchquery'] = self.request.get_full_path()
        context['form'] = self.form(self.search_params)
        context['search_params'] = self.search_params
        context['QUERY_STRING'] = self.request.get_full_path()

        context['facets'] = self.results.facet_counts()
        context['search_params_string'] = self.search_params.urlencode()
        context = self.set_form_attributes_in_context(context)
        context['search_type'] = self.search_type
        context['fshift'] = self.search_params.getlist('fshift',[])
        context['fcid'] = self.search_params.getlist('fcid',[])

        context['CLICK_TRACKING'] = settings.CLICK_TRACKING
        context['tracking_source'] = self.request.META['PATH_INFO']
        context['tracking_drive'] = 'logo_tracking'
        if self.request.flavour == 'mobile':
            context['tracking_medium'] = 'msite'
        else:
            context['tracking_medium'] = 'web'
        context['prod_type'] = self.search_params.getlist('prod_type', [])

        return context

    def build_page(self):
        """
        The results are returned from the search_class.
        They need to be paginated inside the view.
        Get the paginator and page from this method.
        """

        try:
            page_no = int(self.search_params.get('page', 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 1:
            raise Http404("Pages should be 1 or greater.")

        start_offset = (page_no - 1) * self.results_per_page
        self.results = self.results[start_offset:start_offset + self.results_per_page]

        paginator = Paginator(self.results, self.results_per_page)

        try:
            if page_no > paginator.num_pages:
                page_no=paginator.num_pages
            page = paginator.page(page_no)
        except InvalidPage:
            raise Http404("No such page!")
        return paginator, page

    def create_response(self):
        """
        Creates the final response. Executes a series of functionality:
        1> If limits are enabled then check for limits and if exhausted then
            render limits exhausted template
        2> Calls the page builder
        3> Builds base template context and updates with any extra context passed
        4> Finally renders the mentioned search template
        """

        paginator, page = self.build_page()

        context = {
            'query': self.query,
            'page': page,
            'paginator': paginator,
        }
        context.update(self.get_extra_context())
        try:
            context['search_params'].update({'prod_count': self.results.count()})
        except:
            context['search_params'].update({'prod_count': 0})
        if self.request.is_ajax():
            return render(self.request, self.ajax_template_name, context)
        else:
            return render(self.request, self.template_name, context)

    def set_form_attributes_in_context(self,context):
        """
        Pass the form-attributes back into context.
        Used to fill the form after search is performed.
        """
        param_context_mapping = {
            'fskill': 'skill',
            'farea': 'area'
        }

        for param, value in param_context_mapping.items():
            if self.search_params.getlist(param):
                context[value] = self.search_params.getlist(param)
        return context

    def get(self,request,*args,**kwargs):
        return self.prepare_response()

    def post(self,request,*args,**kwargs):
        return self.prepare_response()


class SearchListView(SearchBaseView):
    form = SearchForm
    __name__ = 'SimpleSearch'
    search_type = "keyword"
    extra_context = {'type': 'search'}
    track_query_dict = QueryDict('').copy()
    search_class = SimpleSearch
    params_class = SimpleParams
    pass
