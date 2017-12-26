import datetime
import random
from django.contrib.sitemaps import Sitemap
from django.conf import settings

from shop.models import Product, Category, ProductCategory
from cms.models import Page
from blog.models import Blog, Category as BlogCategory, Author

EXCULDE_CATEGORY = [247, 176, 170, 145, 139, 87, 147, 132, 76, 73, 69, 65, 61, 249]

class CustomSitemap(Sitemap):

    def _urls(self, page, protocol, domain):
        urls = super(CustomSitemap, self)._urls(page, protocol, domain)
        for url in urls:
            url['loc_mobile'] = "%s://%s%s" % (protocol, settings.MOBILE_SITE_DOMAIN, self.location(url['item']))
        return urls


class CourseSitemap(CustomSitemap):
    changefreq = lambda x, y: random.choice(['weekly', 'weekly'])

    def location(self,item):
        return item.get_url(relative=True)

    def mobile_loc(self, item):
        return item.get_mob_url(relative=True)
    
    def priority(self, item):
        return 0.8

    def items(self):
        p_list = list(ProductCategory.objects.filter(active=True).values_list(
            'product__pk', flat=True).distinct())
        
        return Product.browsable.exclude(
            product_class__isnull=True).filter(product_class__slug='course', pk__in=p_list)

    def lastmod(self, item):
        return datetime.date.today() - datetime.timedelta(1)


class SkillSitemap(CustomSitemap):
    changefreq = lambda x, y: random.choice(['daily', 'daily'])

    def priority(self, item):
        return 0.9

    def items(self):
        return Category.objects.filter(is_skill=True, active=True, type_level__in=[3,4])

    def lastmod(self, item):
        return datetime.date.today() - datetime.timedelta(1)


class CategorySitemap(CustomSitemap):
    changefreq = lambda x, y: random.choice(['daily', 'daily'])


    def priority(self, item):
        return 0.7

    def items(self):
        return Category.objects.filter(active=True, type_level=2, is_skill=False).exclude(pk__in=EXCULDE_CATEGORY)

    def lastmod(self, item):
        return datetime.date.today() - datetime.timedelta(1)


class ServiceSitemap(CustomSitemap):
    changefreq = lambda x, y: random.choice(['daily', 'daily'])


    def location(self,item):
        return item.get_url(relative=True)
    
    def priority(self, item):
        return 0.8

    def items(self):
        p_list = list(ProductCategory.objects.filter(active=True).values_list(
            'product__pk', flat=True).distinct())
        
        return Product.browsable.filter(pk__in=p_list).exclude(
            product_class__isnull=True).exclude(product_class__slug='course')

    def lastmod(self, item):
        return datetime.date.today() - datetime.timedelta(1)


class CMSSitemap(CustomSitemap):
    changefreq = lambda x, y: random.choice(['weekly', 'weekly'])

    def priority(self, item):
        return 0.9

    def items(self):
        return Page.objects.filter(is_active=True)

    def lastmod(self, item):
        return datetime.date.today() - datetime.timedelta(1)


class ArticleSitemap(CustomSitemap):
    changefreq = lambda x, y: random.choice(['weekly', 'weekly'])


    def priority(self, item):
        return 0.5

    def items(self):
        return Blog.objects.filter(status=1, visibility=1)

    def lastmod(self, item):
        return datetime.date.today() - datetime.timedelta(1)


class ArticleCategorySitemap(CustomSitemap):
    changefreq = lambda x, y: random.choice(['daily', 'daily'])


    def priority(self, item):
        return 0.8

    def items(self):
        return BlogCategory.objects.filter(is_active=True, visibility=1)

    def lastmod(self, item):
        return datetime.date.today() - datetime.timedelta(1)


class TalentEconomySitemap(CustomSitemap):
    changefreq = lambda x, y: random.choice(['daily', 'daily'])


    def priority(self, item):
        return 0.9

    def items(self):
        return Blog.objects.filter(status=1, visibility=2)

    def lastmod(self, item):
        return datetime.date.today() - datetime.timedelta(1)


class TalentCategorySitemap(CustomSitemap):
    changefreq = lambda x, y: random.choice(['daily', 'daily'])


    def priority(self, item):
        return 0.8

    def items(self):
        return BlogCategory.objects.filter(is_active=True, visibility=2)

    def lastmod(self, item):
        return datetime.date.today() - datetime.timedelta(1)


class TalentAuthorSitemap(CustomSitemap):
    changefreq = lambda x, y: random.choice(['daily', 'daily'])


    def priority(self, item):
        return 0.7

    def items(self):
        return Author.objects.filter(is_active=True, visibility=2)

    def lastmod(self, item):
        return datetime.date.today() - datetime.timedelta(1)
