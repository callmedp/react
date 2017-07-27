from core.library.search.query import SQS
from . import inputs

from haystack.inputs import Raw
from haystack.query import EmptySearchQuerySet

import ast
import uuid
import logging
import copy

#django imports
from django.views.generic import View
from django.utils.text import slugify
from django.conf import settings
from django.http import QueryDict, Http404
from django.core.urlresolvers import resolve, reverse
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.core.cache import cache
from django.template.response import TemplateResponse as render
from search.decorators import persist_referral_code

#local imports
import inputs
from forms import SearchForm
from decorators import jd_login_url,ajax_candidate_login_required, jd_login_url_job
from base_class_views import SearchView
from mixins import RecentSearchesMixin

from search.classes.simple_search import SimpleSearch
from search.classes.simple_class import SimpleParams
from search.classes.similar_search import SimilarSearch
from search.classes.similar_class import SimilarParams
from search.classes.matching_search import MatchingSearch
from search.classes.matching_class import MatchingClass
from search.classes.job_description import JobDescription
from search.classes.job_description_class import JobDescriptionParams
from search.classes.othermatching_search import OtherMatchedSearch
from search.classes.governmentjobs_class import GovernmentJobsParams
from search.classes.governmentjobs import GovernmentJobs
from helpers import search_clean_fields, remove_quote_in_q,clean_id_fields, \
clean_list_fields, clean_all_fields,get_candidate_data, get_jsrp_keyword, \
get_candidate_preferred_location,get_contextual_redirect_path, \
get_contextual_params_from_query, handle_special_chars, get_cached_job_details,get_canonical_url,\
pop_stop_words, get_app_deeplink_url, get_url_mapping, get_highest_priority_param, get_company_page_results

from search.constants import KEYWORD_RELATED_SKILL_MAPPING,\
LOCATION_RELATED_INDUSTRY_MAPPING, INDUSTRY_FA_CONFLICTING_LIST,\
INDUSTRY_RELATED_SKILL_MAPPING, FA_RELATED_SKILL_MAPPING, COMPANY_RELATED_COMPANY_MAPPING
from search.lookups import FILLERS
from search.choices import BREADCRUMB_MAPPING, SEO_TAGS_MAPPING

#inter app imports
from lookup.data import get_jsrp_lookup
from shine.shared.utils.mobileutility import MOBILE_CALL,err_chk_modify
from candidate.register.forms import CandidateRegisterForm
from candidate.frontend.helpers import get_job_details

from candidate.frontend.choices import FUNCTIONAREA_SEARCH_CHOICES, INDUSTRY_SEARCH_CHOICES_ID
from candidate.cache_func import cache_applied_jobs, cache_all_prefrences, cache_all_jobs
from candidate.shared.constants.backoffice import JSRP_VALUES, JD_VALUES

from candidate.shared.models import CandidateShortlistedJobs

#third party imports
from django_redis import get_redis_connection


logger = logging.getLogger('candidate.views')

class SearchModelMixin(object):

    results = SQS()
    clean_query = True
    query_param_name = "keyword"
    allow_empty_query = True

    fields = ["id","jACnt", "jCID", "jCType", "jPDate", "jRUrl", "jSpt", "jJT",
              "jCName", "jLoc", "jExp", "jExMinId", "jExMaxId", "jSalMinID", "jSalMaxID",
              "jAreaID", "jInd", "jArea", "jCL", "jCTU", "jFR", "jKwd", "jQA", "jCUID",
              "jJD", "jCD", "jSal", "jRN", "jRE", "jRP", "jIRA", "jERA"]

    extra_params = {
        'ersearch': 1,
        'mm': '1',
        'qt': 'dismax',
        'facet': 'on',
        'facet.mincount': '1',
        'qf': 'jCName jJT^12 jLoc^6 jArea^2 jInd^2 jKwd^3 text jCNameB jJTB^15 jKwdb^15 jLocB^25 jCNameBS^25',
        'pf': 'jCName^10 jJT^12 jLoc^6 jArea^2 jInd^2 jKwd^3 jJD^2 jCNameB^15 jJTB^15 jKwdb^15 jLocB^25',
        'pf2': 'jKwdb^10 jCNameB^10 jJTB^24',
        'ps2': 1,
        'tie': 1,
    }

    facet_list = []

    filter_mapping = {
        'jCID': 'job_company_id',
        'jPDate': ('since_posting_date', '*'),
    }

    boost_mapping = {
    }

    needed_params_options = {'q', 'loc', 'minsal', 'minexp', 'ind',
                             'area', 'location', 'fexp', 'fsalary',
                             'farea', 'findustry', 'job_company_id', 'fshift',
                             'rect_uid'}

    sort_mapping = {'sort': {'1': ['-jPDate'], '2': ['-jIRA', '-jPDate']}}

    query_param_name = 'q'

    replacement_char = {'-and-': ' AND ',
                        '-or-': ' OR '}

    mobile = None
   
    def get_filter_mapping(self):
        """
        Returns the filter mappings to be used in add_filter method. List is maintained
        in 'filter_mapping' dictionary and is supposed to be defined at class level.

        Incase you want to override and have a completely new mapping, just define
        the dictionary in your extended class.

        Incase you want to append more facets to existing dictionary then you are
        suppose to override this method and return updated dictionary
        """
        return self.filter_mapping.copy()

    def get_boost_mapping(self):
        """
        Returns the boost mappings to be used in add_boost method. List is maintained
        in 'boost_mapping' dictionary and is supposed to be defined at class level.

        Incase you want to override and have a completely new mapping, just define
        the dictionary in your extended class.

        Incase you want to append more facets to existing dictionary then you are
        suppose to override this method and return updated dictionary
        """
        return self.boost_mapping.copy()

    def get_sort_mapping(self):
        """
        Returns sort mappings to be used in add_sort method. List is maintained
        in 'sort_mapping' dictionary and is supposed to be defined at class level.

        Incase you want to override and have a completely new mapping, just define
        the dictionary in your extended class.

        Incase you want to append more facets to existing dictionary then you are
        suppose to override this method and return updated dictionary
        """
        return self.sort_mapping.copy()

    def get_facet_list(self):
        return self.facet_list
    
    def get_field_list(self):
        return self.fields
    
    def add_facets(self):
        """
        All faceting related logic should go here. Extend the class and override
        this function
        """
        results = self.results
        for facet in self.get_facet_list():
            results = results.facet(facet)
        return results

    def query_builder(self):
        return self.search_params.get(self.query_param_name, "")

    def query_cleaner(self):
        """
        Any query processing goes here. If clean_query is True only then this
        method is invoked. Should return the final query after processing
        """
        return self.query

    def add_search_form_filters(self, results):
        """
        Filter search results on the basis of form params sent by candidate.
        Search filter mapping used for filtering.
        """
        for field, param in self.get_filter_mapping().items():
            if type(param) == tuple:
                if self.search_params.get(param[0]) or self.search_params.get(param[1]):
                    p1 = self.search_params.get(param[0], '*')
                    p1 = '*' if not p1 else p1
                    p2 = self.search_params.get(param[1], '*')
                    p2 = '*' if not p2 else p2
                    results = results.narrow('%s:[%s TO %s]' % (field, p1, p2))
            elif type(param) == list:
                for p in param:
                    if self.search_params.get(p):
                        results = results.narrow('%s:(%s)' % (field, ' '.join(self.search_params.getlist(p))))
            else:
                if self.search_params.get(param):
                    fields = field.split(',')
                    if len(fields) > 1:
                        filters = []
                        for key in fields:
                            filters.append('%s:(%s)' % (key, ' '.join(self.search_params.getlist(param))))
                        results = results.narrow(' '.join(filters))
                    else:
                        results = results.narrow('%s:(%s)' % (field, ' '.join(self.search_params.getlist(param))))

        return results

    def add_sws_filters(self, results):
        """
        Implement Search Within Search filtering.
        """
        self.swsh = {'valid': [], 'exclude': []}

        if self.search_params.get('swsv'):
            self.swsh['valid'] = []
            sws_list = self.search_params.get('swsv').split('||')
            for sws in sws_list:
                if sws.lower() != "search within results":
                    self.swsh['valid'].append(sws)

        if self.search_params.get('swse'):
            self.swsh['exclude'] = self.search_params.get('swse').split('||')

        if self.search_params.get('sws') and str(self.search_params.get('sws')).lower() != "search within results":
            self.swsh['valid'].append(self.search_params.get('sws'))

        for sws in self.swsh['valid']:
            results = results.narrow('text:(%s)' % inputs.Cleaned().prepare(sws))

        return results

    def add_filters(self):
        """
        All Generic Filters applicable to all scenarios and requiring computation go here
        """
        results = self.results
        results = self.add_search_form_filters(results)
        
        # Job Freshness Filter
        if self.search_params.get('active') and self.search_params.get('active').isdigit():
            results = results.narrow('jPDate:[NOW/DAY-%sDAYS TO *]' % self.search_params.get('active'))

        # SWS Handling
        results = self.add_sws_filters(results)

        if self.search_params.get("rect") and self.search_params.get("rect"):
            results = results.narrow('jAC:(%s)' % 'False')

        return results

    def add_boost(self):
        """
        All boosting related logic should go here. Override as one key can have range of boosts.
        So technicanlly implemented by enabling one tuple to have multiple tuples or lists and
        iterating over these tupes
        """
        results = self.results
        for field, params in self.get_boost_mapping().items():
            for param in params:
                if type(param[0]) == list:
                    if self.search_params.get(param[0][0]) or self.search_params.get(param[0][1]):
                        p1 = self.search_params.get(param[0][0], '*')
                        p1 = '*' if not p1 else p1
                        p2 = self.search_params.get(param[0][1], '*')
                        p2 = '*' if not p2 else p2
                        results = results.boost('%s:[%s TO %s]' % (field, p1, p2), param[1])
                else:
                    if self.search_params.get(param[0]):
                        results = results.boost('%s:(%s)' % (field, ' '.join(self.search_params.getlist(param[0]))), param[1])

        # Compute Salary Boosting
        if str(self.search_params.get('Salary')).isdigit():
            sal1 = int(self.search_params.get('Salary')) + 1
            sal2 = int(self.search_params.get('Salary')) + 2
            results = results.boost('jSalMinID:(%s)' % sal1, 1)
            results = results.boost('jSalMinID:[%s TO *]' % sal2, 2)

        # Company Jobs Boosting vs Consultant Jobs
        results = results.boost('jCType:0', 4)

        # boost paid jobs
        results = results.boost('jPaid:1', 50)

        # boost jobs where the company is not anonymous
        results = results.boost('jAC:0', 2)

        return results

    def add_sort(self):
        """
        All sorting related logic should go here. Extend the class and override
        this function
        """
        results = self.results
        for field, param in self.get_sort_mapping().items():
            if self.search_params.get(field):
                if param.get(self.search_params.get(field)):
                    results = results.order_by(*param[self.search_params.get(field)])
        return results

    def get_extra_params(self):
        """
        Returns extra parameters to be included in solr query. Mapping is maintained
        in 'extra_params' dictionary and is supposed to be defined at class level.

        Incase you want to override and have a completely new mapping, just define
        the dictionary in your extended class.

        Incase you want to append more facets to existing dictionary then you are
        supposed to override this method and return updated dictionary
        """

        params = self.extra_params.copy()
        return params
    
    def get_results(self):
        """
        Computes the entire query by calling various necessary functions for
        faceting, boosting, extra params and fires the final solr query.

        Note: This does not make the actual solr call as its lazy. The actual
        query is fired in solr when the result is accessed/iterated
        """
        
        self.results = SQS()
        
        if self.needed_params_options and not self.needed_params_options.intersection(self.search_params.keys()):
            return EmptySearchQuerySet()
        
        self.query = self.query_builder()
        
        self.query = self.query_cleaner()
        
        self.results = self.add_filters()
        
        if self.search_params.get("sort") != "1":
            self.results = self.add_boost()
        
        self.results = self.add_sort()
        
        self.results = self.results.extra(self.get_extra_params())
        
        self.results = self.results.filter(content=Raw(self.query))
        
        self.results = self.add_facets()
        
        if hasattr(self, 'get_fields') and self.get_fields():
            self.results = self.results.only(*self.get_fields())
        
        return self.results


class SearchMixin(SearchView):
    """
    Candidate base search view.
    """
    session_key = "searchquery"
    template = 'search/search.html'
    ajax_template = 'search/partials/searchlist.html'
    search_type = ""
    allow_empty_query = True
    form = SearchForm

    similar_fields = []

    query_param_name = 'q'

    replacement_char = {'-and-': ' AND ',
                        '-or-': ' OR '}

    mobile = None
    keywords = None

    def prepare_response(self):
        self.mobile = 'is_mobile' in dir(self.request) and self.request.is_mobile
        self.keywords = self.args
        return super(SearchMixin, self).prepare_response()

    def set_form_attributes_in_context(self,context):
        """
        Pass the form-attributes back into context.
        Used to fill the form after search is performed.
        """
        param_context_mapping = {'location':'location',
                                'fexp':'experience',
                                'fsalary':'salary',
                                'farea':'area',
                                'findustry':'industry',
                                }

        for param,value in param_context_mapping.items():
            if self.search_params.getlist(param):
                context[value] = self.search_params.getlist(param)
        return context

    def set_seo_tags_in_context_post(self,context):
        params = self.search_params.copy()
        job_count_dict = {'job_count':str(self.results.count())}
        params.update(job_count_dict)
        search_parameters = ['q','loc','job_count']
        priority_1 = ['q']
        priority_2 = ['loc']
        params_mapping = []
        for search_param in search_parameters:
            if params.get(search_param,'')!='':
                params_mapping.append(search_param)
        url_key = get_highest_priority_param(params_mapping,priority_1)
        try:
            params_mapping.remove(url_key)
        except:
            pass
        url_key += ' ' + get_highest_priority_param(params_mapping,priority_2)
        url_key = slugify(url_key)
        if not url_key:
            return context
        meta_seo_tags = SEO_TAGS_MAPPING.get(url_key)
        seo_tags = copy.deepcopy(meta_seo_tags)
        for meta_tag in seo_tags:
            context_tag_key = meta_tag + '_tag'
            for param in search_parameters:
                seo_tags[meta_tag] = seo_tags[meta_tag].replace('<'+param+'>' ,handle_special_chars(params.get(param,''),False,True).title())

            context[context_tag_key] = seo_tags[meta_tag]
        return context

    def set_seo_tags_in_context(self,context):
        prod_count_dict = {'prod_count': str(self.results.count())}

        search_params = self.search_params.copy()
        search_params.update(prod_count_dict)

        search_parameters = ['skill', 'job_title','company','loc','ind','area','minexp','walkin','job_count']

        url_key = get_url_mapping(search_params)
        meta_seo_tags = SEO_TAGS_MAPPING.get(url_key)
        seo_tags = copy.deepcopy(meta_seo_tags)
        if not seo_tags:
            return context
        for tag in seo_tags:
            context_tag_key = str(tag) + '_tag'
            if context.has_key(context_tag_key):
                continue
            for search_param in search_parameters:
                if not search_params.has_key(search_param):
                    continue
                if (isinstance(search_params.get(search_param), list)):
                    search_params[search_param] = ' '.join(search_params.get(search_param))
                if search_param == 'ind':
                    search_params['ind'] = dict(INDUSTRY_SEARCH_CHOICES_ID).get(int(self.search_params['ind']),'')
                    if slugify(search_params['ind']) in INDUSTRY_FA_CONFLICTING_LIST:
                        ind = search_params['ind'] + ' Industry'
                        search_params['ind'] = ind
                if search_param == 'area':
                    search_params['area'] = dict(FUNCTIONAREA_SEARCH_CHOICES).get(int(self.search_params['area']),'')
                if search_param == 'walkin':
                    seo_tags[tag] = seo_tags[tag]
                else:
                    if search_param == 'loc':
                        search_params[search_param] = search_params.get(search_param).split(',')
                        search_params[search_param] = ' '.join(search_params.get(search_param))

                seo_tags[tag] = seo_tags[tag].replace('<'+search_param+'>' ,handle_special_chars(search_params.get(search_param,''),False,True).title())
            context[context_tag_key] = seo_tags.get(tag)
        return context

    def get_extra_context(self):

        context = super(SearchMixin, self).get_extra_context()
        context['searchquery'] = self.request.get_full_path()
        context['form'] = self.form(self.search_params)
        context['search_params'] = self.search_params
        context['QUERY_STRING'] = self.request.get_full_path()

        context['facets'] = self.results.facet_counts()
        if hasattr(self, 'locid'):
            context['locid'] = self.locid
        context['jsrp_values'] = JSRP_VALUES
        context['search_params_string'] = self.search_params.urlencode()
        context = self.set_form_attributes_in_context(context)
        context['search_type'] = self.search_type
        context['fshift'] = self.search_params.getlist('fshift',[])
        context['fcid'] = self.search_params.getlist('fcid',[])
        context['prod_type'] = self.search_params.getlist('prod_type', [])

        context['CLICK_TRACKING'] = settings.CLICK_TRACKING
        context['tracking_source'] = self.request.META['PATH_INFO']
        context['tracking_drive'] = 'logo_tracking'
        if self.request.is_mobile:
            context['tracking_medium'] = 'msite'
            context.update(MOBILE_CALL)
        else:
            context['tracking_medium'] = 'web'

        return context

    def build_page(self):
        """
        Paginates the results appropriately
        """

        try:
            page_no = int(self.search_params.get('page', 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 1:
            page_no = 1     # some direct urls hit with page = 0
            error_log="ZeroPageSearch: POST | "+str(self.request.POST) + " | GET | " + str(self.request.GET) + \
                      " | PATH : " + self.request.get_full_path() + " | HTTP_REFERER: " + \
                      self.request.META.get("HTTP_REFERER", "NO HTTP_REFERER")
            logger.info(error_log)

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
        Creates the final response. Executes a series of functionalities:
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
            'paginator': paginator
        }

        context.update(self.get_extra_context())
        try:
            context['search_params'].update({'prod_count': self.results.count()})
        except Exception:
            context['search_params'].update({'prod_count': 0})

        if self.request.is_ajax():
            return render(self.request, self.ajax_template, context)
        else:
            return render(self.request, self.template, context)
