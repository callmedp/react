#python imports
import re
import string

#django imports
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

#third party imports
from haystack.inputs import Raw
from haystack.query import EmptySearchQuerySet

#local imports
from search import inputs
from .helpers import search_clean_fields, pop_stop_words

#inter app imports
from core.library.search.query import SQS


RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)


class BaseSearch(object):

    results = SQS()
    results_per_page = RESULTS_PER_PAGE
    clean_query = True
    none_query = False
    search_params = {}
    allow_empty_query = True

    fields = ["text", "pURL", "pTt", "pHd", "pNm", "pSg", "pTS", "pTP", "pUPC", "pBnr", "pIc", "pIBg", "pImg",
              "pImA", "pVd", "pDM", "pDD", "id", "pCert", "pSM", "pCT", "pAR", "pRC", "pNJ", "pSK", "pCds",
              "pVnd", "pPrs"]

    similar_fields = []

    extra_params = {
        'mm': '1',
        'qt': 'dismax',
        'facet': 'on',
        'facet.mincount': '1',
        'qf': 'text pHd^0.5 pFA^0.3 pCtg^0.2 pMtD^0.1 pMK^0.1 pChts^0.1 pAb^0.05',
        'pf': 'pHd^0.5 pFA^0.2 pCtg^0.2 pMtD^0.1 pMK^0.1 pChts^0.1 pAb^0.05',
        'pf2': 'pFA^03 pCtg^0.2 pChts^0.1',
        'ps2': 1,
        'tie': 1,
        'hl': False,
        # 'boost': 'product(recip(ms(NOW/HOUR,jPDate),3.16e-11,0.08,0.05),jDup)',
        'bq': 'date:[NOW/DAY-1YEAR TO NOW/DAY]'
    }

    facet_list = ['{!ex=loc}jFLoc',
                  '{!ex=exft}jFEx',
                  '{!ex=slft}jFSal',
                  '{!ex=jfunT}pFA',
                  '{!ex=indT}jIndID',
                  'jNSTs']

    # These are the filters shown on search page
    filter_mapping = {
        '{!tag=loc}jFLoc': 'location',
        '{!tag=exft}jFEx': 'fexp',
        '{!tag=slft}jFSal': 'fsalary',
        '{!tag=jfunT}jFA': 'farea',
        '{!tag=indT}jIndID': 'findustry',
        'jCIDF':'fcid',
        'jNSTs': 'fshift',
        'jCType': 'rectype',
        'jCID': 'rect',
        'jCUID': 'rect_uid',
        'jJobType':'job_type'
    }

    boost_mapping = {
        'jIndID': (('IndustryCurr', 2), ('IndustryPrev', 1)),
        'jAreaID': (('SubFunctionalAreaCurr', 2), ('SubFunctionalAreaPrev', 1)),
        'jExID': (('Experience', 2),),
        'jLocID': (('Location', 2),),
    }

    needed_params_options = {}

    sort_mapping = {'sort': {'1': '-jPDate'}}

    query_param_name = 'q'

    user = AnonymousUser()



    def set_query(self,query):
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
        if not hasattr(self,'query'):
            raise ImproperlyConfigured("'%s' must define query" %self.__class__.__name__)
        return self.query

    def set_params(self,params):
        """
        All the search classes take the processed search params.
        Set them using this method.
        No cleaning/processing of the params to be performed in search classes.
        """

        self.params = params

    def set_results(self):
        """
        Spellcheck query not needed in every case.
        Pop spellcheck parameters wherever possible.
        """
        if self.params.has_key('no_spelling') and self.params.get('no_spelling') == True:
            self.results = SQS().using('no_spellcheck')


    def get_params(self):
        """
        Returns the search params set the calling instance.
        Raises an exception if the calling instance does not set the search params.
        """

        if not hasattr(self,'params'):
            raise ImproperlyConfigured("'%s' must define params" %self.__class__.__name__)

        self.set_results()
        return self.params

    def get_rps(self):
        """
        Customize no of results to be fetched from Solr.
        Reduce data to be fetched in requests.
        """
        results_per_page = self.results_per_page
        perpage = self.params.get('perpage')
        if perpage and perpage.isdigit() and int(perpage)>0:
            results_per_page = min(int(perpage),self.results_per_page)
        if self.params.get('count_only'):
            return 0
        return results_per_page


    def set_user(self,user):
        """
        Set the user_id for authenticated users.
        Set it using the class instance and additional filters will be applied.
        Filters like applied jobs etc. can be applied using user_id.
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

        Incase you want to override and have a completely new list, just define
        the list in your extended class.

        Incase you want to append more facets to existing list then you are
        suppose to override this method and return updated list
        """
        if getattr(self,'featured_company_call',None):
            return self.fc_facet_list
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

        if self.user.is_authenticated():
            extra_params.update({"cid":str(self.user.pk)})

        if self.params.has_key('no_spelling') and self.params.get('no_spelling') == True:

            params_to_pop = ['spellcheck','spellcheck.dictionary','spellcheck.maxCollations',
                            'spellcheck.onlyMorePopular','spellcheck.maxResultsForSuggest',
                            'spellcheck.maxCollationTries','spellcheck.collateExtendedResults']
            for param in params_to_pop:
                extra_params.pop(param,None)

        return extra_params


    def add_basic_filters(self,results):
        """
        Filter search results on the basis of form params sent by candidate.
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
                for p in param:
                    if self.params.get(p):
                        results = results.narrow('%s:(%s)' % (field, ' '.join(self.params.getlist(p))))
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

    def add_sws_filters(self,results):
        """
        sws stands for Search-Within-Search.
        Basic filtering already performed.
        Get sws data from the params and filter further.
        """
        self.swsh = {'valid': [], 'exclude': []}

        if self.params.get('swsv'):
            self.swsh['valid'] = []
            sws_list = self.params.get('swsv').split('||')
            for sws in sws_list:
                if sws.lower() != "search within results":
                    self.swsh['valid'].append(sws)

        if self.params.get('swse'):
            self.swsh['exclude'] = self.params.get('swse').split('||')

        if self.params.get('sws') and str(self.params.get('sws')).lower() != "search within results":
            self.swsh['valid'].append(self.params.get('sws'))

        for sws in self.swsh['valid']:
            results = results.narrow('text:(%s)' % inputs.Cleaned().prepare(sws))

        return results

    def add_filters(self):

        results = self.results
        results = self.add_basic_filters(results)

        # Job Freshness Filter
        if self.params.get('active') and search_clean_fields(self.params.get('active')):
            results = results.narrow('jPDate:[NOW/DAY-%sDAYS TO *]' % self.params.get('active'))

        results = self.add_sws_filters(results)
        if self.params.get("rect") and search_clean_fields(self.params.get("rect")):
            results = results.narrow('jAC:(%s)' % 'False')

        return results

    def add_custom_boost(self):
        """
        Perform extra boost for simple and similar views.
        Call this method from the Child classes.
        Override whenever the need arises.
        """
        results = self.results

        if str(self.params.get('Salary')).isdigit() and search_clean_fields(self.params.get('Salary')):
            sal1 = int(self.params.get('Salary')) + 1
            sal2 = int(self.params.get('Salary')) + 2
            results = results.boost('jSalMinID:(%s)' % sal1, 1)
            results = results.boost('jSalMinID:[%s TO *]' % sal2, 2)

        # Company Jobs Boosting vs Consultant Jobs
        results = results.boost('jCType:0', settings.SEARCH_COMPANY_BOOST)

        # boost paid jobs
        results = results.boost('jPaid:1', settings.SEARCH_PAID_BOOST)

        # boost jobs where the company is not anonymous
        results = results.boost('jAC:0', 2)

        #boost enterprise jobs
        results = results.boost('jEnt:2', settings.SEARCH_ENT_BOOST)

        return results

    def add_boost(self):
        """
        All boosting related logic should go here. Override as one key can have range of boosts.
        So technicanlly implemented by enabling one tuple to have multiple tuples or lists and
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
        return results

    def get_load_range(self):

        """
        We need to iterate over the results before returning.
        This will save the extra query due to lazy loading.
        """

        page_no = str(self.params.get('page','1'))
        if not page_no.isdigit() or not int(page_no)>0:
            page_no = 1
        page_no = int(page_no)
        start_offset = (page_no-1)*self.results_per_page
        end_offset = start_offset + self.results_per_page
        return (start_offset,end_offset)


    def get_results(self):
        """
        The core function which gets called by the views/APIs.
        Calls all other functions and returns the results.
        """
        if self.needed_params_options and not self.needed_params_options.intersection(self.get_params().keys()):
            return EmptySearchQuerySet()

        self.results_per_page = self.get_rps()
        self.results = self.add_filters()
        if self.params.get("sort")!="1":
            self.results = self.add_boost()
        self.results = self.add_sort()
        self.results = self.results.extra(self.get_extra_params())
        self.results = self.results.filter(content=Raw(self.get_query()))
        self.results  = self.add_facets()
        self.results = self.results.highlight()
        if self.fields and not self.params.getlist('fl'):
            self.results = self.results.only(*self.fields)
        else:
            asked_fields = map(str,self.params.getlist('fl')[0].split(","))
            self.results = self.results.only(*asked_fields)
        (start_offset,end_offset) = self.get_load_range()
        self.results = self.results[start_offset:end_offset]

        return self.results


    def get_results_count_only(self):
        """
        Separate out the functionality when only count is required.
        Override in child classes when needed.
        """
        fields = ['id','django_ct','django_id','score']
        if self.needed_params_options and not self.needed_params_options.intersection(self.get_params().keys()):
            return 0

        self.results = self.add_filters()
        self.results = self.add_facets()
        self.results = self.results.filter(content=Raw(self.get_query()))
        self.results = self.results.only(*fields)
        return self.results.count()


class SimpleSearch(BaseSearch):

    fields = ["jPDate", "jRUrl", "jSpt", "jJT", "jCName", "jLoc", "jExp","jCL", "jKwd","id","jCTU","jCID","jFR","jQA","jRR","jGovt","jEXID","jJobType","jWSD","jExpDate","jWLC","jJDT"]
    needed_params_options = {'q','loc','minsal','minexp','ind','area','location','fexp','fsalary','farea','findustry','rect','fshift','rect_uid','job_type'}
    sort_mapping = {'sort': {'1': '-jPDate'}}
    query_param_name = 'q'

    facet_list = ['{!ex=loc}jFLoc',
                  '{!ex=exft}jFEx',
                  '{!ex=slft}jFSal',
                  '{!ex=jfunT}jFArea',
                  '{!ex=indT}jIndID',
                  'jNSTs',
                  'jCIDF',
                  'jJobType']

    search_filter_mapping = {
            'jLocID': 'locid',
            'jAreaID': 'area',
            'jIndID': 'ind',
            'jExID': 'minexp',
            }

    extra_params = {
        'search_type': 'simple',
        'mm': '1',
        'qt': 'dismax',
        'facet': 'on',
        'facet.mincount': '1',
        'f.jFEx.facet.sort': 'index',
        'f.jFSal.facet.sort': 'index',
        'qf': 'jLoc^6 jArea^2 jInd^2 text',
        'pf': 'jLoc^6 jArea^2 jInd^2',
        'ps2': 1,
        'tie': 1,
        'hl.simple.pre': "<span class='highlighted'>",
        'hl.simple.post': "</span>",
        'hl.fragsize':0,
        'hl.fl': 'jSpt jKwd jJT jCName jJDT',
        'spellcheck': 'true',
        'spellcheck.dictionary': 'default',
        'spellcheck.onlyMorePopular': 'true',
        'spellcheck.maxResultsForSuggest': 10000,
        'spellcheck.maxCollations': 4,
        'spellcheck.maxCollationTries': 100,
        'spellcheck.collateExtendedResults':'true',
        'boost':'product(recip(ms(NOW/HOUR,jPDate),3.16e-11,0.08,0.05),jDup)',
    }

    def get_filter_mapping(self):
        """
        Overridden to update the filters for simple search.
        Added extra filter mapping apart from the default.
        """
        mapping = super(SimpleSearch, self).get_filter_mapping()
        mapping.update(self.search_filter_mapping)
        return mapping

    def get_extra_params(self):
        """
        Override to selectively boost the results.
        Take into consideration semantic inferred_words.
        """
        extra_params = super(SimpleSearch,self).get_extra_params()

        params_solr_mapping = {'job_title':'jJT',
                    'skill':'jKwd',
                    'company_name':'jCName'}

        default_boosts = {'pf': ['jLoc^6','jArea^2','jInd^2'],
                'pf2': [],
                'pf3':[]}

        field_related_pf_boost = {"jJT":{"pf2":"20","pf3":"20"},
                                "jCName":{"pf2":"20","pf3":"20"},
                                "jKwd":{"pf2":"20","pf3":"20",},}


        for key,value in params_solr_mapping.items():
            pf_covered = False
            pf2_covered = False
            pf3_covered = False

            for param in self.params.get(key,[]):

                if len(param.split(" ")) == 2 and not pf2_covered:
                    pf2_covered = True
                    default_boosts["pf2"].append(value+"^"+field_related_pf_boost[value]["pf2"])

                if len(param.split(" ")) == 3 and not pf3_covered:
                    pf3_covered = True
                    default_boosts["pf3"].append(value+"^"+field_related_pf_boost[value]["pf3"])

        if default_boosts['pf2']:
            extra_params.update({'pf2':" ".join(default_boosts['pf2'])})

        if default_boosts['pf3']:
            extra_params['pf3'] = " ".join(default_boosts['pf3'])

        if self.params.get('skill'):
            extra_params['qf'] = extra_params['qf']+" "+"jKwd^40"
        else:
            extra_params['qf'] = extra_params['qf']+" "+"jKwd^6"

        if self.params.get('company_name'):
            extra_params['qf'] = extra_params['qf']+" "+"jCName^25"
        else:
            extra_params['qf'] = extra_params['qf']+" "+"jCName^5"


        if self.params.get('job_title'):
            extra_params['qf'] = extra_params['qf']+" "+"jJT^35"

        else:
            extra_params['qf'] = extra_params['qf']+" "+"jJT^15"

        return extra_params

    def add_filters(self):
        results = super(SimpleSearch, self).add_filters()
        loc = ''
        jobs_near_candidate = False
        # #Find jobs near the candidate. Only when requested.
        if self.user.is_authenticated() and (self.params.get('best_matches')=='2' or self.params.get('best_matches_ajax')=='2'):
            jobs_near_candidate = True

        # Text Location Filter
        if self.params.get('loc') and not self.params.get('locid') and search_clean_fields(self.params.get('loc')):
            results = results.narrow('jLoc:(%s)' % inputs.Phraser().prepare(self.params.get('loc')))

        if loc:
            results = results.narrow('jLoc:(%s)' % inputs.Phraser().prepare(loc))

        # Salary Filter
        if self.params.get('minsal') and search_clean_fields(self.params.get('minsal')):
            results = results.narrow('jSalMinID:[%(sal)s TO *] jSalMaxID:[%(sal)s TO *]' % {'sal': self.params.get('minsal')})

        return results

    def add_user_preferences_boost(self,results):

        job_title_value = pop_stop_words(self.user.latest_job_title)
        if job_title_value:
            job_title_value = job_title_value.encode('ascii', 'ignore')
            job_title_value = filter(lambda x:x in string.printable,job_title_value)
            job_title_value = pop_stop_words(inputs.Cleaned().prepare(job_title_value,clean=True))
            job_title_value = job_title_value.split('"')

            jts = []
            for jt in job_title_value:
                if jt == ' ' or jt == '':
                    continue

                jt = re.sub("\s\s+" , " ", jt).strip()
                jts.append(jt)

            results = results.boost('jJT:(%s)' % (' AND ').join(jts[0].split(' ')),8)

        candidate_experience = self.user.experience_in_years
        if candidate_experience:
            results = results.boost('(jExMinId:[%s TO *] AND jExMaxId:[* TO %s])' %(candidate_experience-1,candidate_experience),8)

        if self.user.get_functional_areas():
            candidate_functional_area = self.user.get_functional_areas()
            candidate_functional_area = ' '.join(map(str,set(candidate_functional_area)))
            results = results.boost('jAreaID:(%s)' %str(candidate_functional_area),2)

        candidate_profile_skills = CandidatePreferences.objects.get_all_skills(str(self.user.id))
        if candidate_profile_skills:

            for candidate_skills in candidate_profile_skills:
                candidate_skills = candidate_skills.value_custom

                if candidate_skills:
                    candidate_skills = candidate_skills.encode('ascii', 'ignore')
                    candidate_skills = filter(lambda x:x in string.printable,candidate_skills)
                    candidate_skills = pop_stop_words(inputs.Cleaned().prepare(candidate_skills,clean=True))
                    candidate_skills = candidate_skills.split('"')
                    skills = []

                    for skill in candidate_skills:
                        if skill == ' ' or skill == '':
                            continue
                        skill = re.sub("\s\s+" , " ", skill).strip()
                        skills.append(skill)
                    for skill in skills:
                        results = results.boost('jKwd:(%s)' %str(skill),8)
        return results

    def add_boost(self):
        """
        Perform basic boosts by calling the Parent class.
        Also, perform custom_boost defined for Simple/Similar search.
        """
        self.results = super(SimpleSearch,self).add_boost()
        results = self.add_custom_boost()
        boost_rect = self.params.get('boost_rect')
        if boost_rect and str(boost_rect).isdigit():
            results = results.boost('jCID:%s' %str(boost_rect), 100)

        if self.params.has_key('rect') and self.user.is_authenticated():
            results = self.add_user_preferences_boost(results)
        return results
