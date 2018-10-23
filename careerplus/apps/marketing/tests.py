from django.test import TestCase,Client
from django.conf import settings
from django.urls import reverse
from .test_file.factories import CountryFactory
from django.core.cache import cache
from.data import *
from django.db import connections,reset_queries
from shop.models import Product
import factory
import redis
# Create your tests here.

class TestMarketing(TestCase):


    def setUp(self):
        settings.DEBUG = True
        self.client = Client()
        self.country = CountryFactory()
    #
    #
    # def test_query_count_before_request(self):
    #     before_req=len(connections['slave'].queries)+len(connections['master'].queries)
    #     self.assertEquals(before_req,2)
    #
    # def test_query_count_after_request(self):
    #     cache.delete('cache_key_country')
    #     reset_queries()
    #     res = self.client.get(reverse('marketing:linkedin-1'))
    #     after_req = len(connections['slave'].queries) + len(connections['master'].queries)
    #     reset_queries()
    #     self.assertEquals(after_req, 10)
    #
    # def test_get(self):
    #     url = '/linkedin-1.html'
    #     res = self.client.get(url)
    #     reset_queries()
    #     self.assertEqual(res.status_code, 301)
    #
    # def test_context_country(self):
    #     cache.delete('cache_key_country')
    #     res = self.client.get(reverse('marketing:linkedin-1'))
    #     country = cache.get('cache_key_country')
    #     reset_queries()
    #     self.assertEqual(res.context_data.get('countries'),country)
    #
    # def test_context_prod_list(self):
    #     res = self.client.get(reverse('marketing:linkedin-1'))
    #     prod_list,selected=URL_MAPPING_TO_PRODUCT.get('linkedin-1')
    #     product=list(Product.objects.filter(id__in=prod_list))
    #     reset_queries()
    #     self.assertEqual(res.context_data.get('products_lists'), product)
    #     self.assertEqual(res.context_data.get('select'), selected)
    #
    # def urls_arguments(self,url):
    #     path1 = url.split('?')[1:]
    #     path1 = path1[0]
    #     path1 = path1.split('&')
    #     path1.sort()
    #     return path1
    #
    #
    # def test_auto_filler_redirection(self):
    #     url='/gst-cert?token=adasdsadasdas&alt=1112222ssssw&test=11111'
    #     path1=self.urls_arguments(url)
    #     res = self.client.get(url)
    #     path = self.urls_arguments(res.url)
    #     reset_queries()
    #     self.assertListEqual(path, path1)
    #
    # def test_argument_count(self):
    #     url='/gst-cert?token=adasdsadasdas&alt=1112222ssssw&test=11111'
    #     path1 = len(self.urls_arguments(url))
    #     res = self.client.get(url)
    #     path = len(self.urls_arguments(res.url))
    #     reset_queries()
    #     self.assertEquals(path,path1)
    #
    #
    # def test_query_count_after_request_no_cache(self):
    #     reset_queries()
    #     res = self.client.get(reverse('marketing:linkedin-1'))
    #     after_req = len(connections['slave'].queries) + len(connections['master'].queries)
    #     reset_queries()
    #     self.assertEquals(after_req, 9)
    #
    #
    # def test_exceed_query(self):
    #     before_req = len(connections['slave'].queries) + len(connections['master'].queries)
    #     reset_queries()
    #     res = self.client.get(reverse('marketing:linkedin-1'))
    #     after_req = len(connections['slave'].queries) + len(connections['master'].queries)
    #     reset_queries()
    #     self.assertEquals(after_req, before_req+7)

    def test_get_url_queries(self):
        reset_queries()
        url = '/linkedin-1'
        res = self.client.get(url)
        after_req = len(connections['slave'].queries) + len(connections['master'].queries)
        reset_queries()
        self.assertEqual(after_req, 12)



    # def test_query_count_before_request_nocache(self):
    #     before_req = len(connections['slave'].queries) + len(connections['master'].queries)
    #     self.assertEquals(before_req,11)















