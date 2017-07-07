from core.library.search.query import SQS
from . import inputs

from haystack.inputs import Raw
from haystack.query import EmptySearchQuerySet


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


class SearchAPIModelMixin(SearchModelMixin):
    
    needed_params_options = {'job_company_id'}

    filter_mapping = {
        'jCID': 'job_company_id',
        'id': 'job_id',
    }
    
    boost_mapping = {
    }
    
    facet_list = []
    
    queryset = SQS()

    def query_cleaner(self):
        if self.search_params.get('q'):
            self.search_params['q'] = inputs.Cleaned().prepare(self.search_params['q'])
        return inputs.Cleaned().prepare(self.query)
    
    def get_extra_params(self):
        params = super(SearchAPIModelMixin, self).get_extra_params()
        params['ersearch'] = self.search_type
    
    def get_fields(self):
        if self.request:
            field_list = self.request.GET.get('fl', '').split(',')
            if field_list and field_list != ['']:
                return filter(lambda field: field != None, [self.field_mapping.get(field) for field in field_list])
        return self.fields
    
    def get(self, request, *args, **kwargs):
        self.search_params = request.query_params.copy()
        self.search_params.update(kwargs.copy())
        self.field_mapping = dict([(k, v.source) for k, v in self.get_serializer_class()().fields.items()])
        return super(SearchAPIModelMixin, self).get(request, *args, **kwargs)
