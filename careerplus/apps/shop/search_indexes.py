from haystack import indexes
from .models import Product


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField()
    pAR = indexes.DecimalField()    # average_rating
    pRC = indexes.IntegerField(default=0)   # review_count
    pBC = indexes.IntegerField(default=0)  # buy_count
    pNJ = indexes.IntegerField(default=0)  # num_jobs
    pSK = indexes.CharField(default='')   # search_keywords
    pCts = indexes.MultiValueField()    # countries
    pVtn = indexes.MultiValueField()    # variation
    pRtd = indexes.MultiValueField()    # related
    pCds = indexes.MultiValueField()    # childs
    pCtg = indexes.MultiValueField()    # categories
    pKwds = indexes.MultiValueField()    # keywords
    pVds = indexes.IntegerField()   # vendor
    pChts = indexes.MultiValueField()    # chapters
    pFqs = indexes.MultiValueField()    # faqs
    pAts = indexes.MultiValueField()    # attributes
    pPrs = indexes.MultiValueField()    # prices
    pIA = indexes.BooleanField(default=False)  # active

    def get_model(self):
        return Product
