


def pop_stop_words(query):
    for word in query.split("-"):
        if not SEARCH_STOPWORDS_LOOKUP.get(slugify(unicode(word))) == '': continue
        query = re.sub(r'("[^"]*")|\b%s\b' % re.escape(word), lambda m: m.group(1) if m.group(1) else "", query)

    for word in query.split():
        if not SEARCH_STOPWORDS_LOOKUP.get(slugify(unicode(word))) == '': continue
        query = re.sub(r'("[^"]*")|\b%s\b' % re.escape(word), lambda m: m.group(1) if m.group(1) else "", query)

    return query.strip()

def search_clean_fields(key):
    return key not in [None, "None", -1 , "-1", "-1'", "", " "]
