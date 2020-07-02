# built-in imports
import re
import uuid
from collections import OrderedDict
import json
import logging

# django imports
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponsePermanentRedirect
from django.template.loader import render_to_string
from django.views.generic import TemplateView, FormView
from django.http import QueryDict, Http404
from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy, resolve, reverse
from django.http import HttpResponse, Http404
from django.conf import settings
from django.utils.http import urlencode, urlquote_plus
from django.db.models import Q

# local imports
from .templatetags.search_tags import get_choice_display
from .forms import SearchForm, SearchRecommendedForm
from .classes import SimpleSearch, SimpleParams, FuncAreaSearch, FuncAreaParams, RecommendedSearch, RecommendedParams
from .choices import FA_ID_TO_CAT_ID_MAPPING

#inter app imports
from partner.models import Vendor
from geolocation.models import Country
from shop.models import FunctionalArea, Skill, Category

# third party imports
from haystack.query import EmptySearchQuerySet
from core.library.haystack.query import SQS
from django_redis import get_redis_connection

#Global Constants
RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)
# RESULTS_PER_PAGE = 4
error_log = logging.getLogger('error_log')
redis_conn = get_redis_connection("search_lookup")


class SearchBaseView(TemplateView):
    # template_name = 'search/search.html'
    ajax_template_name = 'search/ajax/search_listing.html'
    allow_empty_query = False
    extra_context = {}

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

    facet_key_model_mapping = {"pVid":Vendor}
    facet_model_extra_key_mapping = {}
    facet_choice_map = {"pFA":"FA_FACETS",
                    "pCL":"CL_FACETS",
                    "pDM":"DURATION_DICT",
                    "pCert":"CERT_FACETS",
                    "pStM":"STUDY_MODE",
                    "pPinr":"PRICE_FACETS"}

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

    def get_template_names(self):
        if not self.request.amp:
            return ["search/search.html"]
        return ["search/search-amp.html"]

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

        if self.search_params.get("none_query"):
            self.none_query = True

        # Analytics Relevance Tracking
        if hasattr(self, 'request'):
            if not self.request.is_ajax():
                self.search_sid = uuid.uuid4().hex
            else:
                self.search_sid = self.search_params.get('sid')

    def empty_query_handler(self):
        """
        Prevent further processing if empty query.
        Render response directly. No relaxing/redirects required.
        """
        if (not self.query and not self.allow_empty_query) or self.none_query:
            self.results = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).only('pTt pURL pHd pAR pNJ pImA pImg pNm').order_by('-pBC')[:20]
            return self.create_response()

    def get_results(self):
        """
        This gets the results from search_class.
        Instantiates the search_class, sets params and gets results.
        """
        search_class_obj = self.search_class()
        search_class_obj.set_params(self.search_params)
        search_class_obj.user = self.request.user
        search_class_obj.query = self.query
        self.results, self.found = search_class_obj.get_results()

    def post_processor(self):
        """
        Called just before building response and after results are generated
        """
        filter_mapping = {
            'fprice': 'inrp',
            'fmode': 'mode',
            'fduration': 'duration',
            'fclevel': 'level',
            'fcert': 'certify',
            'fvid': 'vid'
        }

        # Following code is for generating starting from price according to variation filtered TODO: move to ajax later on
        requested_filters = [x for x in ['fprice', 'fmode', 'fduration', 'fclevel', 'fcert', 'fvid'] if x in self.request.GET]
        # if filters are not applied, skip
        if len(requested_filters):
            for result in self.results:
                variations = json.loads(result.pVrs)
                # if no variations, skip
                if variations['variation']:
                    selected_price = result.pPinb if result.pPc == 'writing' or result.pPc == 'service' else result.pPin
                    selected_fprice = result.pPfinb if result.pPc == 'writing' or result.pPc == 'service' else result.pPfin
                    # add variation price to parent price
                    for var in variations['var_list']:
                        continue_flag = 0
                        for att in requested_filters:
                            if not (self.request.GET[att].lower() == str(var.get(filter_mapping[att], '')).lower()):
                                continue_flag = 1
                                break
                        if continue_flag:
                            continue
                        if var['inr_price'] < selected_price:
                            selected_price = var['inr_price']
                            selected_fprice = var['fake_inr_price']
                    if result.pPc == 'writing' or result.pPc == 'service':
                        selected_price += selected_price
                        selected_fprice += selected_fprice
                    result.pPin = selected_price
                    result.pPfin = selected_fprice

        # calculate discount on the fly
        for result in self.results:
            if float(result.pPfin):
                result.discount = round((float(result.pPfin) - float(result.pPin)) * 100 / float(result.pPfin), 2)

    def get_facets_dict(self):
        results_facets = self.results.facet_counts()
        facet_fields_data = results_facets.get('fields',{})
        facet_dict = {}
        bool_string_mapping = {"true":True,"false":False}
        
        for key in facet_fields_data.keys():
            facet_dict[key] = []
            others_dict = {}
            
            for value in facet_fields_data[key]:
                val = int(value[0]) if value[0].isdigit() else value[0]
                val = bool_string_mapping.get(val,val)

                if val == True : val = 1
                facet_data = {"id":val,"count":value[1]}
                
                if self.facet_choice_map.get(key):
                    facet_data.update({"label":get_choice_display(value[0],self.facet_choice_map[key])})

                if facet_data.get('label') == "Others":
                    
                    if str(val) in others_dict.get('id',''):
                        continue

                    others_dict['id'] = "{} {}".format(others_dict['id'],val) if others_dict.get('id') else str(val)
                    others_dict['count'] = others_dict.get('count',0) + value[1]
                    continue

                facet_dict[key].append(facet_data)

            if others_dict:
                other_ids = others_dict.get('id','').split()
                sorted_other_ids = map(str,sorted([int(x) for x in other_ids]))
                facet_dict[key].append({"label":"Others","id":" ".join(sorted_other_ids),
                                        "count":others_dict['count']
                                        })

        for key,model in self.facet_key_model_mapping.items():
            data = facet_dict.get(key)
            
            if not data:
                continue

            ids = [x.get('id') for x in data]
            objects = model.objects.filter(id__in=ids)
            id_to_object_mapping = {str(x.id):x for x in objects}

            for x in data:
                obj = id_to_object_mapping.get(str(x.get("id","")))
                if not obj:
                    x.update({"label":"","slug":""})
                else:
                    x.update({"label":getattr(obj,"name",""),"slug":getattr(obj,"slug","")})
                
                if self.facet_model_extra_key_mapping.get(model.__name__):
                    extra_fields_required = self.facet_model_extra_key_mapping[model.__name__]
                    x.update({key:getattr(obj,key) if obj else None for key in extra_fields_required})

        return facet_dict

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
        if self.form:
            context['form'] = self.form(self.search_params)
        context['search_params'] = self.search_params
        context['QUERY_STRING'] = self.request.get_full_path()
        if self.found:
            context['facets'] = self.get_facets_dict()

        context['search_params_string'] = self.search_params.urlencode()
        context = self.set_form_attributes_in_context(context)
        context['search_type'] = self.search_type
        context['fshift'] = self.search_params.getlist('fshift', [])
        context['fcid'] = self.search_params.getlist('fcid', [])

        context['CLICK_TRACKING'] = settings.CLICK_TRACKING
        context['tracking_source'] = self.request.META['PATH_INFO']
        context['tracking_drive'] = 'logo_tracking'
        if self.request.flavour == 'mobile':
            context['tracking_medium'] = 'msite'
        else:
            context['tracking_medium'] = 'web'
        context['prod_type'] = self.search_params.getlist('prod_type', [])
        
        facet_context_param_mapping = {'fclevel':'clevel',
                                    'fcert':'cert',
                                    'frating':'rating',
                                    'farea':'areaf',
                                    'fduration':'duration',
                                    'fmode':'mode',
                                    'fprice':'price',
                                    'fvid': 'vid'
                                    }

        for facet,context_param in facet_context_param_mapping.items():
            context[context_param] = self.request.GET.getlist(facet)
        context['breadcrumbs'] = self.get_breadcrumbs()
        context['products_found'] = self.found
        context['show_chat'] = True
        func_area = self.request.session.get('recomm_fa')
        if not func_area:
            return context
        # popping the recomm fun
        try:
            self.request.session.pop('recomm_fa')
        except:
            pass
        facets = context.get('facets',{})
        facets_ids = [str(id.get('id')) for id in facets.get('pFA',[]) if id \
                                                                          and
                      isinstance(id.get('id'),int)]
        func_area = FA_ID_TO_CAT_ID_MAPPING.get(str(func_area))
        if not func_area or not facets_ids:
            return context
        if func_area in facets_ids:
            context.update({'areaf':func_area})
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

        paginator = Paginator(self.results, self.results_per_page)

        try:
            if page_no > paginator.num_pages:
                page_no = paginator.num_pages
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
            context['search_params'].update({'prod_count': len(self.results)})
        except Exception as e:
            logging.getLogger('error_log').error(str(e))
            context['search_params'].update({'prod_count': 0})
        if self.request.is_ajax():

            return HttpResponse(json.dumps({
                'response': render_to_string(self.ajax_template_name, context, self.request),
                'num_pages': paginator.num_pages,
                'has_next': page.has_next()
            }), content_type='application/json')
        else:
            return render(self.request, self.get_template_names(), context)

    def set_form_attributes_in_context(self, context):
        """
        Pass the form-attributes back into context.
        Used to fill the form after search is performed.
        """
        param_context_mapping = {
            'skills': 'skills',
            'area': 'area'
        }

        for param, value in param_context_mapping.items():
            if self.search_params.getlist(param):
                context[value] = self.search_params.getlist(param)
        return context

    def get_breadcrumbs(self):
        breadcrumbs = []
        breadcrumbs.append(
            OrderedDict({
                'label': 'Home',
                'url': '/',
                'active': True}))
        return breadcrumbs

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
        # empty_query = self.empty_query_handler()
        # if empty_query:
            # return response
        # if not empty_query:
        self.get_results()
        response = self.post_processor()  # Handle relaxation.
        if response:
            return response
        return self.create_response()

    def get(self, request, *args, **kwargs):
        return self.prepare_response()

    def post(self, request, *args, **kwargs):
        return self.prepare_response()


class SearchListView(SearchBaseView):
    """
    Simple text search
    """
    form = SearchForm
    __name__ = 'SimpleSearch'
    search_type = "simple"
    extra_context = {'type': 'search'}
    track_query_dict = QueryDict('').copy()
    search_class = SimpleSearch
    params_class = SimpleParams

    def prepare_response(self):
        self.keywords = self.args
        current_url = resolve(self.request.path_info).url_name
        return super(SearchListView, self).prepare_response()

    def get_breadcrumbs(self):
        breadcrumbs = super(SearchListView, self).get_breadcrumbs()
        breadcrumbs.append(
            OrderedDict({
                'label': 'Search',
                'active': None
            }))
        return breadcrumbs

    def get_extra_context(self):
        request_get = self.search_params.copy()
        request_get.update(self.request.GET)
        request_get.update(self.request.POST)
        self.request_get = request_get
        context = super(SearchListView, self).get_extra_context()
        context['track_query_dict'] = self.track_query_dict.urlencode()
        context.update({"search_type": "simple"})
        vendor_id = self.request.GET.getlist('fvid',[])

        if len(vendor_id) != 1:
            return context
        if not vendor_id[0].isdigit():
            return context
        if self.request.flavour.lower() == 'mobile':
            banner = 'mobile_banner_image'
        else:
            banner = 'banner_image'

        vendor = Vendor.objects.only('banner_image',
                    'mobile_banner_image','banner_visibility').filter(
            id__in=vendor_id).first()
        if not vendor or not vendor.banner_visibility or not getattr(vendor,\
                banner,None):
            return context

        context.update({'vendor_banner':getattr(vendor,banner).url})
        return context

    def prepare_track(self, page):
        self.track_query_dict = QueryDict(self.search_params.urlencode()).copy()
        self.track_query_dict['template'] = 'psrp_impressions'

    def build_page(self):
        (paginator, page) = super(SearchListView, self).build_page()
        self.prepare_track(page)
        return paginator, page


class RecommendedSearchView(SearchBaseView, FormView):
    """
    Simple text search
    """
    form = SearchRecommendedForm
    __name__ = 'RecommendedSearch'
    search_type = "recommended"
    extra_context = {'type': 'search'}
    track_query_dict = QueryDict('').copy()
    search_class = RecommendedSearch
    params_class = RecommendedParams
    allow_empty_query = True

    def empty_query_handler(self):
        """
        Override for allowing no query search
        """
        pass  # Do nothing

    def get_initial(self):
        super(RecommendedSearchView, self).get_initial()
        if self.request.session.get('candidate_id'):
            func_area = self.request.session.get('func_area')
            func_area = FunctionalArea.objects.filter(pk=func_area)
            func_area = func_area[0].name if func_area else ''
            skills = self.request.session.get('mid_skills').split(",")
            skills_found = Skill.objects.filter(pk__in=skills).values_list('name', flat=True)
        else:
            func_area = ''
            skills_found = []
        return {'area': func_area, 'skills': ",".join(skills_found)}

    def get_breadcrumbs(self):
        breadcrumbs = super(RecommendedSearchView, self).get_breadcrumbs()
        breadcrumbs.append(
            OrderedDict({
                'label': 'Recommendation',
                'active': None
            }))
        return breadcrumbs

    def get_extra_context(self):
        request_get = self.search_params.copy()
        request_get.update(self.request.GET)
        request_get.update(self.request.POST)
        self.request_get = request_get
        context = super(RecommendedSearchView, self).get_extra_context()
        func_areas_set = [f.decode() for f in redis_conn.smembers('func_area_set')]
        skills_set = [s.decode() for s in redis_conn.smembers('skills_set')]
        context.update({'func_area_set': func_areas_set, 'skills_set': skills_set})
        context['track_query_dict'] = self.track_query_dict.urlencode()
        context.update({"search_type": "recommended"})
        func_area = self.request.session.get('func_area')
        if func_area:
            func_area = FunctionalArea.objects.filter(pk=func_area)
            func_area = func_area[0].name if func_area else ''
        context.update({'recmnd_func_area': func_area})
        skills = self.request.session.get('mid_skills')
        skills_found = Skill.objects.filter(pk__in=skills).values_list('name', flat=True)
        context.update({'recmnd_skills': ','.join(skills_found)})
        
        return context

    def prepare_track(self, page):
        self.track_query_dict = QueryDict(self.search_params.urlencode()).copy()
        self.track_query_dict['template'] = 'psrp_impressions'

    def build_page(self):
        (paginator, page) = super(RecommendedSearchView, self).build_page()
        self.prepare_track(page)
        return paginator, page


class FuncAreaPageView(SearchBaseView):
    """
    Functional Area Page
    """
    form = None
    __name__ = 'FuncAreaSearch'
    search_type = "func_area"
    extra_context = {'type': 'func_area'}
    track_query_dict = QueryDict('').copy()
    search_class = FuncAreaSearch
    params_class = FuncAreaParams
    allow_empty_query = True

    def get(self,request,*args,**kwargs):
        path_info = kwargs
        root=request.GET.get('root')
        mobile=request.GET.get('mobile')
        campaign = request.GET.get('utm_campaign')
        if root == 'interested_mail':
            logging.getLogger('info_log').info('interested user clicked product having fa_slug "{}" id-{}, mobile number is "{}", under campaign "{}"'.format(path_info.get('fa_slug'),path_info.get("pk", ""), mobile, campaign))
        paths_to_redirect = {"/services/resume-services/537/":"/services/resume-writing/63/",
                "/services/linkedin-profile-writing/65/":"/services/linkedin-profile/180/"}

        if request.path in paths_to_redirect.keys():
            return HttpResponsePermanentRedirect(paths_to_redirect.get(request.path))

        return super(FuncAreaPageView,self).get(request,*args,**kwargs)

    def empty_query_handler(self):
        """
        Override for allowing no query search
        """
        pass    # Do nothing

    def get_breadcrumbs(self):
        breadcrumbs = super(FuncAreaPageView, self).get_breadcrumbs()

        if self.func_area:
            breadcrumbs.append(
                OrderedDict({
                    'label': self.func_area[0].name,
                    'active': None}))
        return breadcrumbs

    def get_countries(self):
        country_choices = [(m.phone, m.name) for m in
                           Country.objects.exclude(Q(phone__isnull=True) | Q(phone__exact=''))]
        initial_country = Country.objects.filter(phone='91')[0].phone
        return country_choices, initial_country

    def get_extra_context(self):
        request_get = self.search_params.copy()
        request_get.update(self.request.GET)
        request_get.update(self.request.POST)
        self.request_get = request_get
        self.func_area = Category.objects.filter(
            id=self.kwargs['pk'], type_level__in=[2, 3])
        context = super(FuncAreaPageView, self).get_extra_context()

        country_choices, initial_country = self.get_countries()
        context.update({'country_choices': country_choices, 'initial_country': initial_country, })
        if self.func_area.exists():
            meta_desc = "Online {} services. Get expert advice & tips for {} at Shine Learning".format(
                self.func_area[0].name, self.func_area[0].name)
            meta_title = "{} Courses – Online Certifications @ Shine Learning".format(
                self.func_area[0].name)
            context['func_area_name'] = self.func_area[0].heading
            context['func_area_title'] = self.func_area[0].title
            context['meta'] = self.func_area[0].as_meta(self.request)
            meta_dict = context['meta'].__dict__
            meta_dict['description'] = meta_desc
            meta_dict['title'] = meta_title
            context['canonical_url'] = self.func_area[0].get_canonical_url()
        else:
            raise Http404
        context['track_query_dict'] = self.track_query_dict.urlencode()
        context.update({"search_type": "func_area"})

        return context

    def prepare_track(self, page):
        self.track_query_dict = QueryDict(self.search_params.urlencode()).copy()
        self.track_query_dict['template'] = 'psrp_impressions'

    def build_page(self):
        (paginator, page) = super(FuncAreaPageView, self).build_page()
        self.prepare_track(page)
        return paginator, page


class RedirectToRecommendationsView(FormView):
    form_class = SearchRecommendedForm
    template_name = 'search/search.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RedirectToRecommendationsView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        form_data = self.get_form().data
        func_area = form_data['area']
        func_area_obj = None
        try:
            func_area_obj = FunctionalArea.objects.get(name__iexact=func_area)
            self.request.session.update({'func_area': func_area_obj.id})
        except Exception as e:
            error_log.error('Func Area not found in DB:', func_area)
        skills = form_data['skills'].split(",")
        skills = Skill.objects.filter(name__in=skills)
        self.request.session.update({'skills': [skill.id for skill in skills]})
        func_area_slug = func_area_obj.name if func_area_obj else func_area
        rx = '[' + re.escape(''.join(settings.CHARS_TO_REMOVE)) + ']'
        func_area_slug = urlquote_plus(re.sub(rx, '', func_area_slug))
        skills_slug = '-'.join([skill.name for skill in skills])
        skills_slug = urlquote_plus(re.sub(rx, '', skills_slug))
        self.success_url = reverse_lazy('search:recommended_listing',
            kwargs={
            'area_slug': func_area_slug,
            'area': func_area_obj.id if func_area_obj else 0,
            'skills_slug': skills_slug,
            'skills': '-'.join([str(skill.id) for skill in skills])})
        return self.success_url
