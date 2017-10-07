import datetime
import random
from django.contrib.sitemaps import Sitemap

from shop.models import Product, Category
from cms.models import Page
from blog.models import Blog, Category as BlogCategory


class CourseSitemap(Sitemap):
    changefreq = lambda x, y: random.choice(['weekly', 'weekly'])


    def location(self,item):
        return item.get_url(relative=True)
    
    def priority(self, item):
        return 0.8

    def items(self):
        return Product.objects.exclude(
            product_class__isnull=True).filter(is_indexable=True, active=True, product_class__slug='course')

    def lastmod(self, item):
        return datetime.date.today() - datetime.timedelta(1)


class SkillSitemap(Sitemap):
    changefreq = lambda x, y: random.choice(['daily', 'daily'])


    def priority(self, item):
        return 0.9

    def items(self):
        return Category.objects.filter(is_skill=True, active=True)

    def lastmod(self, item):
        return datetime.date.today() - datetime.timedelta(1)


class CategorySitemap(Sitemap):
    changefreq = lambda x, y: random.choice(['daily', 'daily'])


    def priority(self, item):
        return 0.9

    def items(self):
        return Category.objects.filter(active=True)

    def lastmod(self, item):
        return datetime.date.today() - datetime.timedelta(1)


class ServiceSitemap(Sitemap):
    changefreq = lambda x, y: random.choice(['weekly', 'weekly'])


    def location(self,item):
        return item.get_url(relative=True)
    
    def priority(self, item):
        return 0.8

    def items(self):
        return Product.objects.exclude(
            product_class__isnull=True).exclude(product_class__slug='course').filter(is_indexable=True, active=True)

    def lastmod(self, item):
        return datetime.date.today() - datetime.timedelta(1)


class CMSSitemap(Sitemap):
    changefreq = lambda x, y: random.choice(['weekly', 'weekly'])

    def priority(self, item):
        return 0.9

    def items(self):
        return Page.objects.filter(is_active=True)

    def lastmod(self, item):
        return datetime.date.today() - datetime.timedelta(1)


class ArticleSitemap(Sitemap):
    changefreq = lambda x, y: random.choice(['weekly', 'weekly'])


    def priority(self, item):
        return 0.9

    def items(self):
        return Blog.objects.filter(status=1)

    def lastmod(self, item):
        return datetime.date.today() - datetime.timedelta(1)


class ArticleCategorySitemap(Sitemap):
    changefreq = lambda x, y: random.choice(['weekly', 'weekly'])


    def priority(self, item):
        return 0.9

    def items(self):
        return BlogCategory.objects.filter(is_active=True)

    def lastmod(self, item):
        return datetime.date.today() - datetime.timedelta(1)
