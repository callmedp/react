import re
import shlex

STOP_WORDS = ('and', 'or', 'not')
BOOLEAN_OPERATORS = ('and', 'or', 'not')

# Copying new ESCAPE_CHARS, REPLACE_CHARS from
# recruiter codebase (master_rect)
ESCAPE_CHARS = ('+', '&&', '!', '^', '*', '.')
REPLACE_CHARS = (',', '\\', '/', '-', ':')

#ESCAPE_CHARS = ('+', '&', '!', '^')
#REPLACE_CHARS = (',', '\\', '/', '-')


class Stopper(object):
    """
    Removes stop words from query. Also removes '(' and ')' from query.
    Used by other inputs and not to be used directly
    """
    def prepare(self, query):
        query = query.lower()
        for word in STOP_WORDS:
            query = re.sub(r'\b%s\b' % word, '', query)
        query = query.replace('(', '')
        query = query.replace(')', '')
        query1 = query.split(',')
        strQuery = ""
        for q in query1:
                q = q.replace('\'','')
                q = q.replace('\"','')
                strQuery += "\""+q.strip()+"\","
        query = strQuery[:-1]
        return query


class Tokenizer(object):
    """
    Tokenizes query basis comma and space. Used by other inputs and not to be used directly
    """
    def prepare(self, query, clean=False):
        if clean:
            query = Stopper().prepare(query)
        else:
            for word in BOOLEAN_OPERATORS:
                query = re.sub(r'\b%s\b' % word, word.upper(), query)
        for char in REPLACE_CHARS:
            query = query.replace(char, ' ')
        for char in ESCAPE_CHARS:
            query = query.replace(char, '\%s' % char)

        query = shlex.split(str(query), False, False)
        query = map(lambda x: x.strip(), query)
        return query


class Cleaned(Tokenizer):
    """
    General query cleaner. To be called for general queries as it prepares
    a query as per solr standards.
    1> Tokenizes
    2> Capitalize boolean operators
    3> Escape reserved characters
    4> Replace ',' with space
    5> Strips each token for whitespace
    6> Joins each token with space and returns the query as string
    """
    def prepare(self, query, clean=False):
        query = super(Cleaned, self).prepare(query, clean)
        return ' '.join(query)


class Compulsary(Tokenizer):
    """
    Use to make a 'AND' query where all tokens in the query are compulsary
    """
    def prepare(self, query, clean=True):
        query = super(Compulsary, self).prepare(query, clean)
        if query:
            return "(%s)" % ' AND '.join(query)
        else:
            return ''


class Optional(Tokenizer):
    """
    Use to make a 'OR' query where all tokens in the query are optional
    """
    def prepare(self, query, clean=True):
        query = super(Optional, self).prepare(query, clean)
        if query:
            return "(%s)" % ' OR '.join(query)
        else:
            return ''


class Exclude(Tokenizer):
    """
    Use to make a 'NOT' query where all tokens in the query are excluded
    """
    def prepare(self, query, clean=True):
        query = super(Exclude, self).prepare(query, clean)
        return "NOT(%s)" % ' OR '.join(query)


class Phraser(object):
    """
    Passed each token as a phrase query using quotes
    """
    def prepare(self, query, clean=False, stringify=True):
        query = query.split(',')
        query = map(lambda x: x.strip(), query)

        def quotes(token):
            if token.startswith('"'):
                return token
            else:
                return '"%s"' % token

        query = map(quotes, query)
        if stringify:
            return ' '.join(query)
        else:
            return query

CSEARCH_KEYWORD_REPLACE = {
    "-plus": "+",
    "-dot-": ".",
    "dot-": ".",
    "-sharp": "#",
    "quotes-": "\"",
    "-quotes": "\"",
    "-n-": "&",
}


#################PATCH FOR SPECIAL METHODS STARTS #############################
def specialcharin(kwrd):
    kwrd=kwrd.lower()
    return "c++" in kwrd or "j++" in kwrd or "c#" in kwrd or ".net" in kwrd or "j#" in kwrd


def replaced_character_in(kw):
    if kw:
        return "c-plus-plus" in kw or "j-plus-plus" in kw or "c-sharp" in kw or "dot-net" in kw or "j-sharp" in kw


def replace_special_char(kw):
    return kw.replace("c-plus-plus","c++").replace("j-plus-plus","j++").replace("dot-net",".net").replace("c-sharp","c#").replace("j-sharp","j#")


class Canonical(object):
    """
    Replace canonical strings with solr specific params
    """
    def prepare(self, query):
        for k, v in CSEARCH_KEYWORD_REPLACE.items():
            query = query.replace(k, v)
        return query

