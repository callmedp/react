# python built-in imports
import re
import time
import logging
import ast

# django imports
from django.utils.text import slugify
from django.conf import settings
from django_redis import get_redis_connection
from django.core.cache import cache

# local imports
from .lookups import SEARCH_STOPWORDS_LOOKUP
from search import inputs

# interapp imports
from shop.models import Product,ProductFA,ProductSkill

# third party imports
from core.library.haystack.query import SQS
from haystack.query import EmptySearchQuerySet


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


def sort_prod_list(prod_skill_dict):
    if not prod_skill_dict:
        return []
    return [prod_id[0] for prod_id in sorted(prod_skill_dict.items(),
                                      key=lambda k: (len(k[1])), reverse=True)]

# return the default products with skills id list
def default_product_get_set_cache(skills=None):
    cache_key = 'cache_key_for_static_recommend_product'
    if cache.get(cache_key):
        return cache.get(cache_key)

    default_prod = SQS().filter(id__in=settings.DEFAULT_RECOMMEND_PRODUCT)
    product_skill_map = convert_qs_to_pskill_mapping(default_prod,skills)
    cache.set(cache_key,product_skill_map,60*24*24)
    return cache.get(cache_key)


def get_recommend_for_job_title_skills(job_title=None,skills=None,fa=None):

    # when nothing  default product is returned
    if not job_title and not skills and not fa:
        return sort_prod_list(default_product_get_set_cache())

    if not job_title and skills:
        return get_recommendation_for_skill_and_fa(skills,fa)

    jt_products = SQS().filter(pJbtn=job_title,pTF=2)

    if not jt_products:
        return get_recommendation_for_skill_and_fa(skills,fa)

    product_list = sort_prod_list(convert_qs_to_pskill_mapping(jt_products,
                                                               skills))
    if len(product_list) >= 6:
        return product_list[:6]

    skill_product_list = get_skill_product_list(skills)
    product_list_id = [prod.id for prod in product_list]
    distinct_prod_list = [prod_id for prod_id in skill_product_list if
                        prod_id.id not in product_list_id]
    product_list += distinct_prod_list

    if len(product_list) >= 6:
        return product_list[:6]
    product_list_id = [prod.id for prod in product_list]

    rest_jt_products = [prod for prod in jt_products if prod.id not in
                        product_list_id]
    product_list += rest_jt_products
    if len(product_list) >= 6:
        return product_list[:6]
    fa_products = get_recommendation_for_fa(fa)
    fa_products_list = [ prod for prod in fa_products if
                         prod.id not in product_list_id ]
    product_list += fa_products_list
    return product_list[:6]


def convert_qs_to_pskill_mapping(qs,skill=None):
    new_dict = {}
    for prod in qs:
        if not prod or (skill and not prod.uSkill):
            continue
        if not skill:
            new_dict.update({prod: set(prod.uSkill) if prod.uSkill else {}})
        else:
            skill_len = len(set(prod.uSkill).intersection(set(skill)))
            if not skill_len:
                continue
            new_dict.update({prod: set(prod.uSkill).intersection(set(
                skill))})
    return new_dict


def get_fa_product_list(fa):
    product_list = SQS().filter(pFnA=fa,pTF=2)

    return sort_prod_list(convert_qs_to_pskill_mapping(product_list))


def get_recommendation_for_fa(fa=None):


    if not fa:
        # if no fa found return the static product_ids
        return sort_prod_list(default_product_get_set_cache())

    fa_prod_list = get_fa_product_list(fa)
    if len(fa_prod_list) < 6:
        fa_prod_ids = [ prd.id for prd in fa_prod_list ]
        default_products = sort_prod_list(default_product_get_set_cache())
        default_products =[dfproduct for dfproduct in default_products if
                           dfproduct.id not in fa_prod_ids]

        fa_prod_list += default_products

    return fa_prod_list[:6]


def get_skill_product_list(skills):
    if not skills:
        return []
    all_prod_skill = SQS().filter(uSkill__in=skills, pTF=2)
    if not all_prod_skill:
        return []
    return sort_prod_list(convert_qs_to_pskill_mapping(
        all_prod_skill,skills))


def get_recommendation_for_skill_and_fa(skills=None,fa=None):

    if not skills and not fa:
        return sort_prod_list(default_product_get_set_cache())

    if not skills and fa:
        return get_recommendation_for_fa(fa)

    product_list = get_skill_product_list(skills)

    if len(product_list) >= 6:
        return product_list[:6]

    secondary_product_list = get_fa_product_list(fa)
    product_list_id =[prod.id for prod in product_list]

    fa_product_list = [prod_id for prod_id in secondary_product_list if
                       prod_id.id not in product_list_id]

    product_list += fa_product_list
    if len(product_list) >= 6:
        return product_list[:6]
    product_list_id = [ prod.id for prod in product_list]
    default_product = sort_prod_list(default_product_get_set_cache(skills))
    default_product_list = [prod_id for prod_id in default_product if
                       prod_id.id not in product_list_id]

    product_list += default_product_list
    return product_list[:6]


def get_recommended_products(job_title=None, skills=None, func_area=None):

    # if not job_title and not skills and not func_area:
    #     return sort_prod_list(default_product_get_set_cache())
    #
    # if not job_title and not skills and func_area:
    #     return get_recommendation_for_fa(func_area)
    #
    # if not job_title and skills:
    #     return get_recommendation_for_skill_and_fa(skills, func_area)

    return get_recommend_for_job_title_skills(job_title, skills,func_area)

class RecommendationBasedOnGaps():

    def create_product_info_list(self, products_list=None):
        if products_list:
            products_info_list = [{
                'product_id': prd.id,
                'product_name': prd.pNm,
                'product_url': prd.pURL,
                'product_title': prd.pTt,
                'product_icon': prd.pIc,
                'product_image': prd.pImg,
                'product_desc': prd.pDsc,
                'product_ratings': prd.pStar,
                'product_combos': prd.pCmbs,
                'product_variations': prd.pVrs,
                'product_offers': prd.pOff,
                'product_inr_price': prd.pPinb,
                'product_usd_price': prd.pPusb,
                'product_functional_area': prd.pFAn,
                'product_type': prd.pTF
            } for prd in products_list]
            return products_info_list

        return []

    def convert_qs_to_pskill_mapping_api_method(self, qs,skill=None, is_skill_id=False):
        new_dict = {}
        for prod in qs:
            if is_skill_id:
                user_skill = prod.uSkill
            else:
                user_skill = prod.uSkilln
            if not prod or (skill and not user_skill):
                continue
            if not skill:
                new_dict.update({prod: set(user_skill) if user_skill else {}})
            else:
                skill_len = len(set(user_skill).intersection(set(skill)))
                if not skill_len:
                    continue
                new_dict.update({prod: set(user_skill).intersection(set(
                    skill))})
        return new_dict

    def skill_product_list(self, skills):
        is_skill_id = False
        if not skills:
            return []
        if skills[0].isdigit():
            all_prod_skill = SQS().filter(uSkill__in=skills, pTF__in=[2,16])
            is_skill_id = True
        else:
            all_prod_skill = SQS().filter(uSkilln__in=skills, pTF__in=[2,16])
        if not all_prod_skill:
            return []
        return sort_prod_list(self.convert_qs_to_pskill_mapping_api_method(
            all_prod_skill,skills, is_skill_id))

    def get_recommended_products_based_on_job_title_gap(self, desired_job_title=None, actual_job_title=None):
            data = {}
            recommended_products = []
            recommended_products_list = []
            try:
                if desired_job_title:

                    desired_jt_products = SQS().filter(pJbtn=desired_job_title, pTF__in=[2,16])
                    if actual_job_title:
                        actual_jt_products = SQS().filter(pJbtn=actual_job_title, pTF__in=[2,16])
                        rproducts = list(set(desired_jt_products) -
                                        set(actual_jt_products))
                        if rproducts:
                            recommended_products_list = rproducts
                        else:
                            recommended_products_list = list(
                                set(desired_jt_products))

                    elif not actual_job_title:
                        if desired_jt_products:
                            recommended_products_list = list(
                                set(desired_jt_products))
                if recommended_products_list:
                    recommended_products = self.create_product_info_list(
                        recommended_products_list)
                default_recommended_products_list = sort_prod_list(
                    default_product_get_set_cache())
                default_recommended_products = self.create_product_info_list(
                    default_recommended_products_list)

                data.update({
                    "recommended_products": recommended_products,
                    "default_recommended_products": default_recommended_products
                })

            except Exception as e:
                logging.getLogger('error_log').error(
                    "Error occurred for job title based recommendation : " + str(e))
                data = {'msg': 'error'}

            return data

    def get_recommended_products_based_on_skill_gap(self, job_description_skills=[], candidate_profile_skills_list=[]):

            data = {}
            recommended_skill_product_list = []
            if job_description_skills:
                jd_skills = eval(job_description_skills)
            else:
                jd_skills = job_description_skills
            if candidate_profile_skills_list:
                candidate_profile_skills = eval(candidate_profile_skills_list)
            else:
                candidate_profile_skills = candidate_profile_skills_list

            try:
                skills_list = list(set(jd_skills) - set(candidate_profile_skills))
                recommended_skill_product_list = self.skill_product_list(
                    skills_list)

                recommended_skill_products = self.create_product_info_list(
                    recommended_skill_product_list)
                default_recommended_products_list = sort_prod_list(
                    default_product_get_set_cache(candidate_profile_skills))
                default_recommended_products = self.create_product_info_list(
                    default_recommended_products_list)

                data.update({
                    "recommended_products": recommended_skill_products,
                    "default_recommended_products": default_recommended_products
                })

            except Exception as e:
                logging.getLogger('error_log').error(
                    "Error occurred for skill gap recommendation : " + str(e))
                data = {'msg': 'error'}

            return data