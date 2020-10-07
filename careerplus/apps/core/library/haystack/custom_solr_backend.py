#python imports

#django imports

#local imports
from haystack.models import SearchResult

#inter app imports
from ..pysolr.pysolr import ProductSolr

#third party imports
from haystack.backends.solr_backend import SolrSearchBackend, SolrSearchQuery
from haystack.backends import BaseEngine
from haystack.constants import DEFAULT_ALIAS


class CustomSolrSearchBackend(SolrSearchBackend):

    RESERVED_WORDS = ()

    # Characters reserved by Solr for special use.
    # The '\\' must come first, so as not to overwrite the other slash replacements.
    RESERVED_CHARACTERS = (
        '\\', '+', '-', '&&', '||', '!',
        '^', '"', '~', '*', '?'
    )

    def __init__(self, connection_alias, **connection_options):
        """
        Overridden to change Solr connection and use custom Solr Connection.
        Also modifies the timeout value.
        """
        super(CustomSolrSearchBackend, self).__init__(connection_alias, **connection_options)
        self.timeout = connection_options.get('TIMEOUT',30)
        self.conn = ProductSolr(connection_options['URL'], timeout=connection_options.get('TIMEOUT',30))

    def build_search_kwargs(self, query_string, sort_by=None, start_offset=0, end_offset=None,
                            fields='', highlight=False, facets=None,
                            date_facets=None, query_facets=None,
                            narrow_queries=None, spelling_query=None,
                            within=None, dwithin=None, distance_point=None,
                            models=None, limit_to_registered_models=None,
                            result_class=None, stats=None,**kwargs):

        """
        Overridden to include extra_params and boost_params apart from the other params.
        """
        search_params =super(CustomSolrSearchBackend,self).build_search_kwargs(query_string,sort_by,start_offset,end_offset,fields,highlight,facets,date_facets,query_facets,narrow_queries,spelling_query,within,dwithin,distance_point,models,limit_to_registered_models,result_class,stats)

        search_params.update(**kwargs)
        return search_params

    def _process_results(self, raw_results, highlight=False, result_class=None, distance_point=None):
        """
        The processed results contain a suggestion even for a complete match of query string.
        We need not present suggestions when there is an absolute match.
        Suggestions are a dict when there is a complete match.List otherwise.
        """
        result_class =SearchResult
        processed_results = super(CustomSolrSearchBackend,self)._process_results(raw_results,highlight,result_class,distance_point)
        if processed_results.get('spelling_suggestion'):
            if isinstance(processed_results['spelling_suggestion'],dict):
                processed_results['spelling_suggestion'] = None

        return processed_results

class CustomSolrSearchQuery(SolrSearchQuery):

    def __init__(self,using=DEFAULT_ALIAS):
        """
        Initialize extra_params.
        """
        self.extra_params = {}
        super(CustomSolrSearchQuery,self).__init__(using)

    def add_extra_params(self, **kwargs):
        """
        Receive the extra params from SearchQuerySet.
        Set the value of extra_params to be sent to the search_params.
        """
        self.extra_params.update(**kwargs)

    def _clone(self,klass=None,using=None):
        """
        Pass a copy of extra params into the query.
        The clone is used for all operations. Therefore, this method is overridden.
        """
        clone = super(CustomSolrSearchQuery,self)._clone(klass,using)
        clone.extra_params = self.extra_params.copy()
        return clone

    def add_fields(self,fields):
        """
        Return only the desired fields.If not called, return all.
        Also, add the must_fields which are needed in all situations.
        """
        must_fields = ['id','score','django_ct','django_id']
        self.fields.extend(must_fields)
        
        self.fields.extend(fields)

    def build_params(self, spelling_query=None, **kwargs):
        """
        Prepare kwargs to be sent to build_search_kwargs.
        Add extra_params to this list.
        """
        search_kwargs = super(CustomSolrSearchQuery,self).build_params(spelling_query,**kwargs)
        if self.boost:
            bq = []
            for term, boost in self.boost.items():
                bq.append("%s^%s" % (term, boost))
            search_kwargs.update({'bq':bq})
        
        if self.extra_params:
            search_kwargs.update(self.extra_params)

        return search_kwargs

    def build_query(self):
        """
        Builds the final query.
        Extended to remove the boost logic.
        The default functionality of boost is not needed.
        """
        
        final_query = self.query_filter.as_query_string(self.build_query_fragment)
        
        if not final_query:
            # Match all.
            final_query = self.matching_all_fragment()
        return final_query


class CustomSolrEngine(BaseEngine):
    """
    Specify the backend and query-set to be used.
    """
    backend = CustomSolrSearchBackend
    query = CustomSolrSearchQuery
