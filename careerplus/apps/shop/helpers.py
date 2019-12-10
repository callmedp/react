# python imports
import ast
import re 

# django imports
from django.utils.text import slugify

# third party imports
from django_redis import get_redis_connection

redis_server = get_redis_connection("candidate_search_lookup")

TYPE_MAPPING = {
    1: ('job_title', 'q'),
    2: ('skill', 'q'),
    3: ('loc', ),
    4: ('minexp', ),
    5: ('ind', ),
    6: ('area', ),
    7: ('company_name', 'q'),
    8: ('walkin', ),
    9: ('junk', 'q'),
}

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


def get_ngrams(words_list, ngram):
    counter = 0
    end = len(words_list)
    words_to_pop = []
    ngrams = []
    while counter + ngram <= end:
        word = slugify(" ".join(words_list[counter:counter + ngram]))
        if word:
            semantic_entity = redis_server.get(word)
            if semantic_entity:
                words_to_pop.append(word)
                value = ast.literal_eval(semantic_entity.decode('utf-8'))
                value.append(word)
                ngrams.append(value)
                counter = counter + ngram
                continue
        counter = counter + 1
    return words_to_pop, ngrams


def pop_inferred_words_from_query(words_to_pop, query):
    inferred_words_lookup = {slugify(str(a)): True for a in words_to_pop}
    # inferred_words_lookup.pop('fresher','')
    # inferred_words_lookup.pop('freshers','')
    slugified_query = slugify(str(" ".join(query.split("\"")[0::2])))
    for word in list(inferred_words_lookup.keys()):
        slugified_query = re.sub(
            r'("[^"]*")|\b%s\b' % re.escape(word), lambda m: m.group(1) if m.group(1) else "",
            slugified_query)
    query_to_return = slugified_query.strip()
    if query.split("\"")[1::2]:
        query_to_return = "\"" + " ".join(query.split("\"")[1::2]) + "\" " + query_to_return
    return query_to_return


def get_semantic_inferred_words_and_ngrams(ngram_size, words_list, slugified_query):
    inferred_words = dict()
    ngrams_all = []
    for i in range(ngram_size, 0, -1):
        words_to_pop, ngrams = get_ngrams(words_list, i)
        if ngrams:
            ngrams_all += ngrams

        words_to_pop = dict((word, "") for word in words_to_pop)

        inferred_words = classify_ngrams(inferred_words, ngrams)
        slugified_query = pop_inferred_words_from_query(words_to_pop, slugified_query)
        words_list = slugified_query.split("-")
        try:
            words_list.remove('')
        except ValueError:
            pass

    return inferred_words, words_list, ngrams_all


def get_inferred_skills(text):
    slugified_query = slugify(text)
    words_list = slugified_query.split('-')
    inferred_words, non_inferred_words_list, ngrams_all = \
        get_semantic_inferred_words_and_ngrams(5,words_list,slugified_query)
    print(inferred_words)
    inferred_skills = inferred_words.get('skill',[])
    inferred_skills = list(set([x for x in inferred_skills if x]))
    return inferred_skills

