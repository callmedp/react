from haystack.query import SearchQuerySet


class SQS(SearchQuerySet):
    """
    Extend SearchQuerySet to to add extra/raw params to the query.
    """

    def extra(self, params=None, **kwargs):
        """
        Add extra params to the query to be sent to Solr.
        Any raw params are to be added here.
        """
        if params:
            kwargs.update(params)
        clone = self._clone()
        kwargs.update({'hl.fragsize':0}) #Highlight the entire fragment each time.
        clone.query.add_extra_params(**kwargs)
        return clone

    def only(self, *fields):
        """
        Modify the fields to be returned by Solr.
        If not used, all the fields will be returned.
        """
        clone = self._clone()
        clone.query.add_fields(fields)
        return clone
