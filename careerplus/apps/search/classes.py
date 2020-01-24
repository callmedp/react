# python imports
import re
import itertools

# django imports
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ImproperlyConfigured

# third party imports
from haystack.inputs import Raw

# local imports
from search import inputs
from .helpers import clean_all_fields, clean_id_fields, clean_list_fields, \
    handle_special_chars, get_filters, remove_quote_in_q, clear_empty_keys, \
    search_clean_fields, get_recommendations
from .lookups import FILLERS

# inter app imports
from core.library.haystack.query import SQS

RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)


class BaseSearch(object):
    results = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS)
    results_per_page = RESULTS_PER_PAGE
    search_params = {}
    allow_empty_query = True

    fields = ["text", "pURL", "pTt", "pHd", "pTP", "pStar", "pImA", "id", "pARx", "pRC", "pNJ", "pImg",
              "pPvn", "pCmbs", "pVrs", "pPinr", "pPfinr", "pPusd", "pPfusd", "pPaed", "pPfaed", "pPgbp", "pPfgbp", "pCC",
              "pPin", "pPfin", "pPus", "pPfus", "pPae", "pPfae", "pPgb", "pPfgb",
              "pPinb", "pPfinb", "pPusb", "pPfusb", "pPaeb", "pPfaeb", "pPgbb", "pPfgbb",
              "pPc", "pFA", "pNm", "pBC","pVid"]

    similar_fields = []

    extra_params = {
        'mm': '1',
        'qt': 'edismax',
        'facet': 'on',
        'facet.mincount': '1',
        'facet.sort': 'index',
        'qf': 'text pHd^10 pFA^6 pCtg^4 pCC^2 pAb^1',
        'pf': 'pHd^10 pFA^4 pCtg^4 pMtD^2 pMK^2 pPCC^2 pAb^1',
        'pf2': 'pFA^6 pCtg^4 pPCC^2',
        'ps2': 1,
        'tie': 1,
        'hl': 'false',
        'spellcheck': 'false'
    }

    facet_list = [
        '{!ex=pCL}pCL',
        '{!ex=pAR}pAR',
        '{!ex=funa}pFA',
        '{!ex=pVid}pVid',
        '{!ex=ratng,inrp}pAR',
        '{!ex=inr}pDM',
        '{!ex=inr}pCert',
        '{!ex=inr}pStM',
        '{!ex=inr}pPinr'
    ]

    # These are the filters shown on search page
    filter_mapping = {
        '{!tag=funa}pFA': 'farea',
        '{!tag=ratng}pAR': 'frating',
        '{!tag=pVid}pVid': 'fvid',
        '{!tag=inr}pAttrINR': ['fclevel', 'fcert', 'fduration', 'fmode', 'fprice'],
    }

    boost_mapping = {}

    needed_params_options = {}

    sort_mapping = {'sort': {'1': '-pCD', '2': '-pARx'}}

    query_param_name = 'q'

    user = AnonymousUser()

    def set_query(self, query):
        """
        Set the actual query string upon which the Raw search needs to be performed.
        Use this method to set the query for search.
        """
        self.query = query

    def get_query(self):
        """
        Get the query upon which the actual Raw query needs to be performed.
        This is to be set by the calling instance.
        Raises an exception if the query is not set by the calling instance.
        """
        if not hasattr(self, 'query'):
            raise ImproperlyConfigured("'%s' must define query" % self.__class__.__name__)
        return self.query

    def set_params(self, params):
        """
        All the search classes take the processed search params.
        Set them using this method.
        No cleaning/processing of the params to be performed in search classes.
        """
        self.params = params

    def set_results(self):
        """
        Spell check query not needed in every case.
        Pop spell check parameters wherever possible.
        """
        if 'no_spelling' in self.params and self.params.get('no_spelling') == True:
            self.results = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).using('no_spellcheck')

    def get_params(self):
        """
        Returns the search params set the calling instance.
        Raises an exception if the calling instance does not set the search params.
        """

        if not hasattr(self, 'params'):
            raise ImproperlyConfigured("'%s' must define params" % self.__class__.__name__)

        self.set_results()
        return self.params

    def get_rps(self):
        """
        Customize no of results to be fetched from Solr.
        Reduce data to be fetched in requests.
        """
        results_per_page = self.results_per_page
        perpage = self.params.get('perpage')
        if perpage and perpage.isdigit() and int(perpage) > 0:
            results_per_page = min(int(perpage), self.results_per_page)
        if self.params.get('count_only'):
            return 0
        return results_per_page

    def set_user(self,user):
        """
        Set the user_id for authenticated users.
        Set it using the class instance and additional filters will be applied.
        """
        self.user = user

    def get_user(self):
        """
        Get user_id for applying filters for authenticated users.
        Returns None if not set by the calling instance.
        """
        return self.user

    def get_facet_list(self):
        """
        Returns the facet lists to be shown on results page. List is maintained
        in 'facet_list' list and is supposed to be defined at class level.

        In case you want to override and have a completely new list, just define
        the list in your extended class.

        In case you want to append more facets to existing list then you are
        suppose to override this method and return updated list
        """
        return self.facet_list

    def get_filter_mapping(self):
        """
        Returns the filter mappings to be used in add_filter method. List is maintained
        in 'filter_mapping' dictionary and is supposed to be defined at class level.

        Incase you want to override and have a completely new mapping, just define
        the dictionary in your extended class.

        Incase you want to append more keys to existing dictionary then you are
        suppose to override this method and return updated dictionary
        """
        return self.filter_mapping.copy()

    def get_boost_mapping(self):
        """
        Returns the boost mappings to be used in add_boost method. List is maintained
        in 'boost_mapping' dictionary and is supposed to be defined at class level.

        Incase you want to override and have a completely new mapping, just define
        the dictionary in your extended class.

        Incase you want to append more keys to existing dictionary then you are
        suppose to override this method and return updated dictionary
        """
        return self.boost_mapping.copy()

    def get_sort_mapping(self):
        """
        Returns sort mappings to be used in add_sort method. List is maintained
        in 'sort_mapping' dictionary and is supposed to be defined at class level.

        Incase you want to override and have a completely new mapping, just define
        the dictionary in your extended class.

        Incase you want to append more keys to existing dictionary then you are
        suppose to override this method and return updated dictionary
        """
        return self.sort_mapping.copy()

    def get_extra_params(self):
        """
        Returns extra parameters to be included in solr query. Mapping is maintained
        in 'extra_params' dictionary and is supposed to be defined at class level.

        Incase you want to override and have a completely new mapping, just define
        the dictionary in your extended class.

        Incase you want to append more keys to existing dictionary then you are
        suppose to override this method and return updated dictionary
        """

        extra_params = self.extra_params.copy()

        # if self.user.is_authenticated:
        #     extra_params.update({"cid": str(self.user.pk)})

        if 'no_spelling' in self.params and self.params.get('no_spelling') == True:

            params_to_pop = ['spellcheck', 'spellcheck.dictionary',
            'spellcheck.maxCollations',
            'spellcheck.onlyMorePopular', 'spellcheck.maxResultsForSuggest',
            'spellcheck.maxCollationTries', 'spellcheck.collateExtendedResults']
            
            for param in params_to_pop:
                extra_params.pop(param, None)

        return extra_params

    def add_basic_filters(self, results):
        """
        Filter search results on the basis of form params sent by user.
        Search filter mapping used for filtering.
        """
        for field, param in self.get_filter_mapping().items():
            if type(param) == tuple:
                if self.params.get(param[0]) or self.params.get(param[1]):
                    p1 = self.params.get(param[0], '*')
                    p1 = '*' if not p1 else p1
                    p2 = self.params.get(param[1], '*')
                    p2 = '*' if not p2 else p2
                    results = results.narrow('%s:[%s TO %s]' % (field, p1, p2))
            elif type(param) == list:
                attrs = []
                for p in param:
                    if self.params.get(p):
                        attrs.append(self.params.getlist(p))
                if attrs:
                    attrs = list(itertools.product(*attrs))
                    solr_attrs = ['"{}"~4'.format(' '.join(attr)) for attr in attrs]
                    results = results.narrow('%s:(%s)' % (field, ' OR '.join(solr_attrs)))
            else:
                if self.params.get(param):
                    fields = field.split(',')
                    if len(fields) > 1:
                        filters = []
                        for key in fields:
                            filters.append('%s:(%s)' % (key, ' '.join(self.params.getlist(param))))
                        results = results.narrow(' '.join(filters))
                    else:
                        results = results.narrow('%s:(%s)' % (field, ' '.join(self.params.getlist(param))))

        return results

    def add_sort(self):
        """
        Sort the results depending on the sort mapping.
        Set the sort mapping in child class to change behaviour.
        """
        results = self.results
        for field, param in self.get_sort_mapping().items():
            if self.params.get(field):
                results = results.order_by(param[self.params.get(field)])
        return results

    def add_facets(self):
        """
        Facet on the results depending on the facet_mapping.
        Set facet mapping in child class to change behaviour.
        """
        results = self.results
        for facet in self.get_facet_list():
            results = results.facet(facet)
        return results

    # def add_sws_filters(self,results):
    #     """
    #     sws stands for Search-Within-Search.
    #     Basic filtering already performed.
    #     Get sws data from the params and filter further.
    #     """
    #     self.swsh = {'valid': [], 'exclude': []}
    #
    #     if self.params.get('swsv'):
    #         self.swsh['valid'] = []
    #         sws_list = self.params.get('swsv').split('||')
    #         for sws in sws_list:
    #             if sws.lower() != "search within results":
    #                 self.swsh['valid'].append(sws)
    #
    #     if self.params.get('swse'):
    #         self.swsh['exclude'] = self.params.get('swse').split('||')
    #
    #     if self.params.get('sws') and str(self.params.get('sws')).lower() != "search within results":
    #         self.swsh['valid'].append(self.params.get('sws'))
    #
    #     for sws in self.swsh['valid']:
    #         results = results.narrow('text:(%s)' % inputs.Cleaned().prepare(sws))
    #
    #     return results

    def add_filters(self):

        results = self.results
        found = True
        results = self.add_basic_filters(results)
        if not results.count():
            results = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).only('pTt pURL pHd pAR pNJ pImA pImg pNm').order_by('-pBC')[:20]
            found = False
        # results = self.add_sws_filters(results)
        return results, found

    def add_custom_boost(self):
        """
        Perform extra boost for simple and similar views.
        Call this method from the Child classes.
        Override whenever the need arises.
        """
        results = self.results

        return results

    def add_boost(self):
        """
        All boosting related logic should go here. Override as one key can have range of boosts.
        So technically implemented by enabling one tuple to have multiple tuples or lists and
        iterating over these tuples.
        """
        results = self.results
        for field, params in self.get_boost_mapping().items():
            for param in params:
                if type(param[0]) == list:
                    if self.params.get(param[0][0]) or self.params.get(param[0][1]):
                        p1 = self.params.get(param[0][0], '*')
                        p1 = '*' if not p1 else p1
                        p2 = self.params.get(param[0][1], '*')
                        p2 = '*' if not p2 else p2
                        results = results.boost('%s:[%s TO %s]' % (field, p1, p2), param[1])
                else:
                    if self.params.get(param[0]):
                        results = results.boost('%s:(%s)' % (field, ' '.join(self.params.getlist(param[0]))), param[1])
        results = self.add_custom_boost()
        return results

    def get_load_range(self):

        """
        We need to iterate over the results before returning.
        This will save the extra query due to lazy loading.
        """

        page_no = str(self.params.get('page', '1'))
        if not page_no.isdigit() or not int(page_no) > 0:
            page_no = 1
        page_no = int(page_no)
        start_offset = (page_no - 1) * self.results_per_page
        end_offset = start_offset + self.results_per_page
        return (start_offset, end_offset)

    def get_results(self):
        """
        The core function which gets called by the views/APIs.
        Calls all other functions and returns the results.
        """
        if self.needed_params_options and not self.needed_params_options.intersection(self.get_params().keys()):
            results = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).only('pTt pURL pHd pAR pNJ pImA pImg pNm').order_by('-pBC')[:20]
            found = False
            return results, found
        self.results_per_page = self.get_rps()
        self.results, found = self.add_filters()
        if self.params.get("sort") != "1":
            self.results = self.add_boost()
        if found:
            self.results = self.add_sort()
            self.results = self.results.extra(self.get_extra_params())
            if self.get_query():
                self.results = self.results.filter(content=Raw(self.get_query()))
            self.results = self.add_facets()
            if self.fields and not self.params.getlist('fl'):
                self.results = self.results.only(*self.fields)
            else:
                asked_fields = map(str, self.params.getlist('fl')[0].split(","))
                self.results = self.results.only(*asked_fields)
            if not self.results.count():
                self.results = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).only('pTt pURL pHd pAR pNJ pImA pImg pNm').order_by('-pBC')[:20]
                found = False
        (start_offset, end_offset) = self.get_load_range()
        # self.results[start_offset:end_offset]
        return self.results, found

    def get_results_count_only(self):
        """
        Separate out the functionality when only count is required.
        Override in child classes when needed.
        """
        fields = ['id', 'django_ct', 'django_id', 'score']
        if self.needed_params_options and not self.needed_params_options.intersection(self.get_params().keys()):
            return 0

        self.results, self.found = self.add_filters()
        self.results = self.add_facets()
        self.results = self.results.filter(content=Raw(self.get_query()))
        self.results = self.results.only(*fields)
        return self.results.count()


class BaseParams(object):
    args = ''
    keywords = ''
    clean_query = True
    query_param_name = 'q'

    def query_builder(self):
        return self.search_params.get(self.query_param_name, "")

    def get_request_params(self):
        """
        Return a copy of both GET/POST parameters.
        GET params are set irrespective of Request Method.
        This is done to handle user profile params
        """
        params = self.request.GET.copy()
        if self.request.method == 'POST':
            params.update(self.request.POST.copy())

        for param in params:
            values = params.getlist(param)
            values = [value.strip() if isinstance(value, str) else value for value in values]
            params.setlist(param, values)
        return params

    def clean_search_params(self):
        """
        Clean search params before processing.
        Cleaning includes field, id and list cleaning.
        """
        self.search_params = clean_all_fields(self.search_params)
        self.search_params = clean_id_fields(self.search_params)
        self.search_params = clean_list_fields(self.search_params)

    def set_args(self, args, kwargs):
        self.args = args
        self.keywords = self.args
        self.kwargs = kwargs

    def query_cleaner(self):
        query = inputs.Cleaned().prepare(self.query)
        return query

    def get_search_query(self):

        self.query = self.query_builder()
        if self.clean_query:
            self.query = self.query_cleaner()
        return self.query

    def get_search_params(self):
        self.search_params = self.get_request_params()
        self.clean_search_params()
        return self.search_params


class SimpleSearch(BaseSearch):

    needed_params_options = {'q', 'fclevel', 'fcert', 'farea', 'frating', 'fduration', 'fmode','fvid'}

    def get_extra_params(self):
        """
        Override to selectively boost the results.
        Take into consideration semantic inferred_words.
        """
        extra_params = super(SimpleSearch, self).get_extra_params()
        extra_params.update({'search_type': 'simple'})
        return extra_params


class SimpleParams(BaseParams):

    def set_params_from_lookups(self, params):
        params['q'] = " ".join(self.keywords)
        params['q'] = handle_special_chars(params['q'], False, True, False, False)
        params = get_filters(params)
        return params

    def get_request_params(self):
        """
        Collect and prepare all the request params.
        All the processing of params is done here.
        The view calls this method if the request is for web/mobile.
        The API will call this method if the request is for app.
        """
        params_filtered = False
        params = super(SimpleParams, self).get_request_params()

        # resolve single quote and double quote issue
        if params.get("q"):
            params["q"] = remove_quote_in_q(params.get("q"))

        if not params.get('page') and len(self.keywords) > 1 and self.keywords[-1].isdigit():
            page = self.keywords[-1]
            params['page'] = page
            self.keywords = list(self.keywords)
            self.keywords.remove(page)

        if self.request.method != 'POST' and hasattr(self, 'keywords') and \
                len(self.keywords):

            params = self.set_params_from_lookups(params)
            if 'q' not in params:
                params['keywords'] = ""
            else:
                params['keywords'] = params.get('q')
            params_filtered = True

        # Incase of GET request if all arguments are found in lookup then it states that no keyword
        # have been entered so set solr query as *:* in separate param so that it does not get displayed in form

        params = clear_empty_keys(params)

        if not params_filtered:
            if 'q' not in params:
                params['keywords'] = ""
            else:
                params = get_filters(params)
                params['keywords'] = params.get('q')
        return params

    def query_builder(self):
        q = self.search_params.get('q', "")
        if not q:
            return q

        # Exception for course and courses in search terms.
        if q == "courses" or q == "course" or q == "course courses" or q == "courses courses":
            return " ".join(settings.PRODUCT_ALTERNATE_SEARCH_TERMS)

        quoted_string = ""
        for s in q.split("\"")[1::2]:
            quoted_string = quoted_string + "\"" + s + "\" " if s else quoted_string

        quoted_string = quoted_string.strip()
        unquoted_string = (" ".join(q.split("\"")[0::2])).lower()
        # classifiers_to_process = ["area", "skills"]
        # words_to_and = []
        # for classifier in classifiers_to_process:
        #     words_to_and = words_to_and + self.search_params.get(classifier, [])

        # for word in words_to_and:
        #     unquoted_string = re.sub('(^{0}(?=\s))|((?<=\s){0}(?=\s))|((?<=\s){0}$)|(^{0}$)'.format(
        #         re.escape(word.lower())),"", unquoted_string)

        classified_words = quoted_string
        # for word in words_to_and:
        #     classified_words = classified_words+" ("+" AND ".join(word.split(" "))+")"

        split_query = unquoted_string.split(" ")
        filler_words = ""
        actual_words = ""

        for word in split_query:
            if word == "courses":
                continue
            if word in FILLERS:
                filler_words = filler_words + " AND " + word if filler_words else filler_words + word
            else:
                actual_words = actual_words + " " + word if actual_words else actual_words + word

        if filler_words:
            filler_words = "(" + filler_words + ")"
        if actual_words:
            actual_words = "(" + handle_special_chars(actual_words, False, True) + ")"
        if filler_words and actual_words:
            query_to_return = classified_words + " " + actual_words + " AND " + filler_words
        elif filler_words:
            query_to_return = classified_words + " AND " + filler_words if classified_words else filler_words
        else:
            query_to_return = classified_words + " " + actual_words
        query_to_return = re.sub("\(\s\s+\)", "", query_to_return).strip()
        return query_to_return


class FuncAreaSearch(BaseSearch):

    needed_params_options = {'pk', 'fclevel', 'fcert', 'farea', 'frating', 'fduration', 'fmode'}

    def add_filters(self):
        self.results, self.found = super(FuncAreaSearch, self).add_filters()

        # Functional Area Filter
        if self.params.get('pk') and search_clean_fields(self.params.get('pk')) and self.found:
            self.results = self.results.narrow('pFA:%s' % self.params.get('pk'))
        if not self.found:
            self.results = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).only('pTt pURL pHd pAR pNJ pImA pImg pNm').order_by('-pBC')[:20]
            self.found = False
        return self.results, self.found


class FuncAreaParams(BaseParams):
    query_param_name = None
    clean_query = False

    def get_search_params(self):
        self.search_params = self.get_request_params()
        self.clean_search_params()
        self.search_params['pk'] = self.kwargs.get('pk')
        return self.search_params


class RecommendedSearch(BaseSearch):
    needed_params_options = {'area', 'skills'}  # , 'fclevel', 'fcert', 'farea', 'frating', 'fduration', 'fmode'}

    def add_filters(self):
        results, found = super(RecommendedSearch, self).add_filters()
        results = get_recommendations(self.params['area'], self.params['skills'], results)
        if not results.count():
            results = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).only('pTt pURL pHd pAR pNJ pImA pImg pNm').order_by('-pBC')[:20]
            found = False
        return results, found


class RecommendedParams(BaseParams):
    query_param_name = None
    clean_query = False

    def get_search_params(self):
        self.search_params = super(RecommendedParams, self).get_search_params()
        if self.request.method == 'GET':
            self.search_params['area'] = self.kwargs.get('area')
            self.search_params['skills'] = self.kwargs.get('skills').split('-')
        return self.search_params






