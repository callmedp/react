# python built-in imports
import re
from collections import OrderedDict
import time
import logging
import ast

# django imports
from django.utils.text import slugify
from django.conf import settings
from core.library.haystack.query import SQS
from haystack.query import EmptySearchQuerySet

# third party imports
from django_redis import get_redis_connection

# local imports
from .lookups import SEARCH_STOPWORDS_LOOKUP #SEARCH_LOCATION_LOOKUP, ,\
# SKILL_SLUG, CITY_SLUG, EXPERIENCE_SLUG, FA_SLUG, INDUSTRY_SLUG, \
# JOBTITLE_SLUG, COMPANY_SLUG, SPECIAL_CHARACTERS_LOOKUP
from search import inputs
from shop.models import ProductFA, ProductSkill
redis_server = get_redis_connection("search_lookup")
logger = logging.getLogger('info_log')

TYPE_MAPPING = {1: ('job_title', 'q'),
                2: ('skills', 'q'),
                3: ('loc',),
                4: ('exp',),
                5: ('ind',),
                6: ('area',),
                7: ('company_name', 'q'),
                8: ('junk', 'q'),}


def pop_stop_words(query):
    for word in query.split("-"):
        if not SEARCH_STOPWORDS_LOOKUP.get(slugify(str(word))) == '': continue
        query = re.sub(r'("[^"]*")|\b%s\b' % re.escape(word), lambda m: m.group(1) if m.group(1) else "", query)

    for word in query.split():
        if not SEARCH_STOPWORDS_LOOKUP.get(slugify(str(word))) == '': continue
        query = re.sub(r'("[^"]*")|\b%s\b' % re.escape(word), lambda m: m.group(1) if m.group(1) else "", query)

    return query.strip()


def search_clean_fields(key):
    return key not in [None, "None", -1 , "-1", "-1'", "", " "]


def clean_all_fields(param):
    """
    @summary: allow only one (#,&,*) other than that should remove
    remove : ,?,forward slashes,back slashes,[,],{,}
    escape . dot
    """
    for key in ["q", "area", "skills"]:
        val = param.get(key, "")
        if val:
            val = str(val)
            # allow only one (#,&,*,\) other than that should remove
            reg_x_kwr = [r'/', r'#', r'&', r'\*']
            for kwr in reg_x_kwr:
                if len(re.findall(kwr, val)) > 1:
                    if r'&' == kwr:
                        val = re.sub(kwr, ' ', val)
                    else:
                        val = re.sub(kwr, '', val)
            # remove : ,?,back slashes,[,],{,}
            val = re.sub(r'[\?\\\[\]\{\}]', "", val)
            #val = val.replace(".","\.") # escape . dot
            param[key] = val
    return param


def clean_list_fields(param):
    """
    :param param:
    :return:
    @summary: to clean list type request parameters ()
    """

    invalid_keyword = {None, "None", -1, "-1", "-1'", "", " "}
    param_prefix_mapping = {
        "fclevel": "CL",
        "fcert": "CERT",
        "frating": "",
        "fduration": "DM",
        "fmode": "SM",
        "skills": "",
        "fprice": "P",
        "fvid": ""
    }
    for key, prefix in param_prefix_mapping.items():
        val = param.getlist(key)
        if val:
            val = set(val)
            cln_list = []
            for v in list(val - invalid_keyword):
                if key == 'fcert' and v == 'true':
                    v = '1'
                cln_list.append("{}{}".format(prefix, v))
            param.setlist(key, cln_list)

    return param


def clean_id_fields(param):
    """
    @summary: function to clean request parameters (area, sort, page )
    """
    for key in ["area", "sort", "page"]:
        val = param.get(key)
        if val:
            val = str(val)
            if not val.isdigit():
                val = re.sub(r'[\?\\\[\]\{\}\'\"/]', "", val)
                if val.isdigit():
                    param[key] = val
                else:
                    param[key] = ""
    none_query = False
    if param.get("q") == "" and param.get("area") == "" and param.get("skills") == "":
        none_query = True
    if param.get("q") in ['*','*.*']:
        none_query = True
    param["none_query"] = none_query
    return param


def handle_special_chars(query, slugified=True, reverse=False, hyphenate=False, ignore_quotes=False):
    # special_chars_mapping = {
    #     "+": " plus ",
    #     "#": " sharp ",
    #     ".": " dot ",
    #     "\"": " quotes ",
    #     "&": " n ",
    #     }
    #
    # if ignore_quotes:
    #     special_chars_mapping.pop("\"")
    # if hyphenate:
    #     special_chars_mapping = {k:"-"+slugify(str(v))+"-" for k,v in special_chars_mapping.items()}
    # if reverse:
    #     scm_copy = special_chars_mapping.copy()
    #     special_chars_mapping = OrderedDict('').copy()
    #     special_chars_mapping.update({"-"+slugify(str(k))+"-":v for v,k in scm_copy.items()})
    #     special_chars_mapping.update({"-"+slugify(str(k)):v for v,k in scm_copy.items()})
    #     special_chars_mapping.update({slugify(str(k))+"-":v for v,k in scm_copy.items()})
    #     special_chars_mapping.update({slugify(str(k)):v for v,k in scm_copy.items()})
    #     [special_chars_mapping.pop(extra_key) for extra_key in ['-n','n','n-']]
    #
    # for key,value in special_chars_mapping.items():
    #     if ignore_quotes:
    #         split_query = re.split(r'(\"[^"]*?\")',query)
    #         query = ''.join([i.replace(key,value) if '"' not in i else i for i in split_query])
    #
    #     else:
    #         query = query.replace(key,value)
    # if not slugified:
    #     return query
    return slugify(str(query))


def get_ngrams(words_list,ngram):
    counter = 0
    end = len(words_list)
    words_to_pop = []
    ngrams = []
    while counter+ngram <= end:
        word = slugify(" ".join(words_list[counter:counter+ngram]))
        if word:
            semantic_entity = None # redis_server.get(word)
            if semantic_entity:
                words_to_pop.append(word)
                value = ast.literal_eval(semantic_entity.decode('utf-8') if isinstance(semantic_entity, bytes)
                                         else semantic_entity)
                value.append(word)
                ngrams.append(value)
                counter = counter + ngram
                continue
        counter += 1
    return words_to_pop, ngrams


def classify_ngrams(inferred_words, ngrams):
    if not ngrams:
        return inferred_words
    for ngram in ngrams:
        param = TYPE_MAPPING.get(ngram[0])
        for p in param:
            inferred_words[p].append(ngram[2]) if inferred_words.get(p) else inferred_words.update({p: [ngram[2]]})
    return inferred_words


def pop_inferred_words_from_query(words_to_pop,query):
    inferred_words_lookup = {slugify(str(a)):True for a in words_to_pop}
    slugified_query = slugify(str(" ".join(query.split("\"")[0::2])))
    for word in inferred_words_lookup.keys():
        slugified_query = re.sub(r'("[^"]*")|\b%s\b' % re.escape(word), lambda m: m.group(1) if m.group(1) else "",
                                 slugified_query)
    query_to_return = slugified_query.strip()
    if query.split("\"")[1::2]:
        query_to_return = "\""+" ".join(query.split("\"")[1::2])+"\" " + query_to_return
    return query_to_return


def prepare_singlevalue_params(inferred_words, params):

    SINGLEVALUE_PARAMS = {'area'}
    for param in SINGLEVALUE_PARAMS:
        if params.get(param) and len(params.get(param)):
            continue
        if inferred_words.get(param):
            params[param] = ast.literal_eval(redis_server[slugify(str(inferred_words[param][0]))])[1]
    return params


def prepare_multivalue_params(inferred_words,params):
    MULTIVALUE_PARAMS = ['skills']
    for param in MULTIVALUE_PARAMS:
        input_value = params.get(param,"")
        for inferred_value in inferred_words.get(param,[]):

            if slugify(str(inferred_value)) in slugify(str(input_value)):
                continue
            if input_value == '' or not input_value: input_value = inferred_value
            else: input_value = input_value+','+inferred_value
        params[param] = input_value
    return params


def clear_empty_keys(params):
    """
    Remove empty valued keys.
    Prevent empty spaces from entering into the params.
    """
    for key in list(params):
        if not params.get(key) or params.get(key) == u'null':
            params.pop(key)
    return params


def get_spaced_special_characters(query, params):
    """
    Provide spacing for special characters.
    Keeps queries such as c++c from merging into each other.
    """

    special_characters = ['++', '#']
    for sp_char in special_characters:
        query = re.sub('{0}' .format(re.escape(sp_char)), sp_char + " ", query)
    return query


def replace_multiple_occurrences(query, params):
    """
    Prevent multiple repetitions of words in query.
    """

    keys_to_process = ['skills', 'area', 'skills']
    words_to_remove = []

    for key in keys_to_process:
        if not params.get(key):
            continue
        for word in params.get(key):
            query_count = params.get(key).count(word)
            if query_count > 1 and word not in words_to_remove:
                words_to_remove.append(word)

            for word in words_to_remove:
                params['q'] = str(handle_special_chars(params['q'])).replace(
                    handle_special_chars(word), '', query_count-1)
                params[key] = list(set(params[key]))

    return handle_special_chars(params['q'], False, True)


def get_filters(params):
    start = time.time()
    query = params.get('q')
    query = inputs.Cleaned().prepare(query)
    query = " ".join(query.split("\"")[::2])
    query = handle_special_chars(query, False, False, True, True)
    query = query.replace(",", " ").strip()
    query = pop_stop_words(str(query))
    slugified_query = slugify(str(query))
    words_list = slugified_query.split("-")
    inferred_words = {}
    excess_params = []

    if len(words_list) > 10:
        excess_params = words_list[10:]
        words_list = words_list[:10]
        slugified_query = '-'.join(words_list)

    for i in range(5,0,-1):
        words_to_pop, ngrams = get_ngrams(words_list, i)
        words_to_pop = dict((word, "") for word in words_to_pop)

        inferred_words = classify_ngrams(inferred_words, ngrams)
        slugified_query = pop_inferred_words_from_query(words_to_pop, slugified_query)
        words_list = slugified_query.split("-")
        try:
            words_list.remove(u'')
        except ValueError:
            pass

    inferred_words['q'] = filter(len,inferred_words.get('q', []) + words_list)
    words_to_pop = inferred_words.get('skills', []) + inferred_words.get('area', [])
    params['q'] = inputs.Cleaned().prepare(params['q'])
    params['q'] = params['q'].replace("/","-")
    params['q'] = handle_special_chars(params['q'], False, False, False, True)
    inferred_words_copy = inferred_words.copy()
    inferred_words_copy.pop("q", None)
    params['q'] = pop_stop_words(str(params['q']))

    params['q'] = ''.join([i.replace(",", " ") if '"' not in i else i for i in params['q']])

    params['q'] = pop_inferred_words_from_query(words_to_pop, params['q'])
    params['q'] = re.sub("\s\s+", " ", params['q'])
    params = prepare_multivalue_params(inferred_words, params)
    params = prepare_singlevalue_params(inferred_words, params)
    params['q'] = handle_special_chars(params['q'], False, True, False, True)
    params = clear_empty_keys(params)

    if params.get('q'):
        params['q'] = get_spaced_special_characters(params['q'], params)
        params['q'] = replace_multiple_occurrences(params['q'], params)
        params['q'] = params['q'].replace("-", " ")
        params['q'] = re.sub("\s\s+", " ", params['q']).strip()

    if excess_params:
        params['q'] = params['q'] + ' ' + ' '.join(excess_params)
    diff = time.time() - start
    if diff > 1:
        logger.info(("Time taken {0} and semantic params {1}".format(diff,params)))

    return params


def remove_quote_in_q(q):
    if 0 != q.count("'") % 2:
        q = q.replace("'","")
    if 0 != q.count('"') % 2:
        q = q.replace('"',"")
    return q


def get_recommendations(func_area, skills, results=None):
    if not func_area:
        func_area = 23
    if not skills:
        # skills = [777, 795, 2064]
        skills = []

    # func_area_prods = set(ProductFA.objects.filter(fa=func_area).values_list('product', flat=True))
    # skill_prods = set(ProductSkill.objects.filter(skill__in=skills).values_list('product', flat=True))
    # products_fa_and_skill = func_area_prods.intersection(skill_prods)
    # ids = list(products_fa_and_skill)
    # ids += list(skill_prods.difference(products_fa_and_skill))
    # ids += list(func_area_prods.difference(products_fa_and_skill))

    # skills = ['244', '310', '4', '10', '320', '389', '3827', '3824']
    if skills:
        if not results:
            results = SQS().exclude(id__in=settings.EXCLUDE_SEARCH_PRODUCTS).only('pTt pURL pHd pARx pNJ pImA pImg pStar pNm pBC pRC')
        # results = results.narrow('id:(%s)' % ' '.join([str(pid) for pid in ids]))
        results = results.filter(pSkill__in=skills, pPc=settings.COURSE_SLUG[0])
    else:
        results = EmptySearchQuerySet()
    return results