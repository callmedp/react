# built-in imports
import re
import uuid

# django imports
from django.shortcuts import render, HttpResponsePermanentRedirect
from django.views.generic import ListView, TemplateView
from django.http import QueryDict, Http404
from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse_lazy, resolve, reverse
from django.http import HttpResponseRedirect
from django.conf import settings

# third party imports
# from haystack.views import SearchView
from haystack.query import EmptySearchQuerySet

# local imports
from .forms import SearchForm
from .classes import SimpleSearch, SimpleParams
from .choices import AREA_WITH_LABEL, SKILL_WITH_LABEL

RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)


class SearchBaseView(TemplateView):
    template_name = 'search/search.html'
    ajax_template_name = 'search/ajax/search_listing.html'
    allow_empty_query = False
    clean_query = True
    extra_context = {}
    query_param_name = "q"

    # Conditional Form Validation required variables
    query = ''
    results = EmptySearchQuerySet()
    request = None
    form = None
    results_per_page = RESULTS_PER_PAGE
    search_class = None
    params_class = None
    session_key = "searchquery"
    search_type = ""
    none_query = False

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
        self.params_class_obj = self.params_class()
        self.params_class_obj.set_args(self.args, self.kwargs)

        setattr(self.params_class_obj, "request", self.request)
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
        self.results[start_offset:start_offset + self.results_per_page]

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
            'skills': 'skills',
            'farea': 'farea'
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
    """
    Simple text search
    """
    form = SearchForm
    __name__ = 'SimpleSearch'
    search_type = "keyword"
    extra_context = {'type': 'search'}
    track_query_dict = QueryDict('').copy()
    search_class = SimpleSearch
    params_class = SimpleParams

    def get_fields(self):
        return ["id", "pURL", "pHdx", "pCDate", "pSg", "pIc", "pImA",
                "pAb", "pAR", "pFA", "pCtg", "pPChs", "pCert", "pStM",
                "pCL", "pStar", "pRC", "pNJ", "pCmbs", "pPv"]

    def prepare_response(self):
        self.keywords = self.args
        current_url = resolve(self.request.path_info).url_name
        if current_url == 'search_listing' and not self.request.GET:
            return HttpResponsePermanentRedirect(reverse('search:recommended_listing',
                                                         kwargs={'f_area':'it-software',
                                                                 'skill':'development'}))
        return super(SearchListView, self).prepare_response()

    def pre_processor(self):
        """
        Called before any other processing
        """

        if self.search_params.get("none_query"):
            self.none_query = True

        # Analytics Relevance Tracking
        if hasattr(self, 'request'):
            if not self.request.is_ajax():
                self.search_sid = uuid.uuid4().hex
            else:
                self.search_sid = self.search_params.get('sid')

    def get_extra_context(self):

        request_get = self.search_params.copy()
        request_get.update(self.request.GET)
        request_get.update(self.request.POST)
        self.request_get = request_get
        context = super(SearchListView, self).get_extra_context()

        context['track_query_dict'] = self.track_query_dict.urlencode()
        context.update({"search_type": "simple"})
        return context

    def prepare_track(self, page):
        self.track_query_dict = QueryDict(self.search_params.urlencode()).copy()

        self.track_query_dict['template'] = 'psrp_impressions'

    def build_page(self):
        (paginator, page) = super(SearchListView, self).build_page()
        self.prepare_track(page)
        return paginator, page


