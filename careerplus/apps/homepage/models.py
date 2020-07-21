# python imports

#django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

# local imports
from .config import PAGECHOICES, STATIC_PAGE_NAME_CHOICES

# interapp imports
from seo.models import AbstractAutoDate
from shop.models import FunctionalArea

# third party imports
from ckeditor.fields import RichTextField


class TopTrending(AbstractAutoDate):
    name = models.CharField(max_length=255, unique=True)
    products = models.ManyToManyField(
        "shop.Product",
        through='TrendingProduct',
        related_name='trendingcourses')

    view_all = models.CharField(
        max_length=255,
        help_text=_('provide full url with http:// to redirect on click.'))

    is_jobassistance = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    fa = models.ManyToManyField(FunctionalArea,null=True, blank=True)

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return self.name

    def get_trending_products(self):
        tprds = self.trendingproduct_set.filter(is_active=True).select_related('product')
        tprds = tprds.filter(product__type_product__in=[0, 1, 3])
        return tprds


class TrendingProduct(AbstractAutoDate):
    trendingcourse = models.ForeignKey(
        TopTrending,
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        "shop.Product",
        on_delete=models.CASCADE)

    priority = models.IntegerField(default=0)

    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('trendingcourse', 'product')
        ordering = ['priority']

    def __str__(self):
        return self.trendingcourse.name + '-' + self.product.name


class Testimonial(AbstractAutoDate):
    page = models.PositiveIntegerField(
        default=0, choices=PAGECHOICES)
    user_id = models.CharField(
        max_length=100,
        verbose_name=_("User ID"),)
    user_name = models.CharField(
        max_length=100,
        verbose_name=_("User Name"))
    title = models.CharField(max_length=255, null=True, blank=True)
    review = models.TextField(max_length=1024)
    rating = models.DecimalField(
        max_digits=8, decimal_places=2,
        default=2.5)
    designation = models.CharField(max_length=200)
    # location = models.CharField(max_length=200, null=True, blank=True)
    company = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(
        _('Profile Image'),
        upload_to='images/testimonial/', null=True, blank=True)
    priority = models.IntegerField(default=0)

    is_active = models.BooleanField(default=False)

    # for university/Course skill page
    object_id = models.PositiveIntegerField(
        null=True, blank=True)

    def __str__(self):
        return str(self.user_name) + ' - ' + str(self.id)

    class Meta:
        ordering = ['priority']

    def get_image_url(self):
        if self.image:
            return self.image.url
        return settings.STATIC_URL + 'shinelearn/images/executive/default-user-pic.jpg'

    def page_choice_text(self):
        currency_dict = dict(PAGECHOICES)
        return currency_dict.get(self.page)


class TestimonialCategoryRelationship(AbstractAutoDate):
    category = models.ForeignKey('shop.Category',on_delete=models.CASCADE)
    testimonial = models.ForeignKey('homepage.Testimonial',on_delete=models.CASCADE)


class StaticSiteContent(models.Model):
    page_type = models.PositiveIntegerField(
        default=-1, choices=STATIC_PAGE_NAME_CHOICES , help_text=_('page id'))

    content = RichTextField(
        verbose_name=_('content'), help_text=_('html content'))
    
    @property
    def page_name(self):
        return STATIC_PAGE_NAME_CHOICES[self.page_type-1][1]

    def __str__(self):
        return str(STATIC_PAGE_NAME_CHOICES[self.page_type-1][1])

class HomePageOffer(AbstractAutoDate):
    name = models.CharField(
        _('Offer Name'), max_length=50,blank=True,null=True)
    sticky_text = models.CharField(
        _('Offer Sticky Text'), max_length=100,blank=True,null=True)
    offer_value = models.CharField(
        _('Offer value Text'), max_length=100,blank=True,null=True, 
            help_text=("For eg. 'Upto 30%\' off!' or 'Flat 20%\' off!'"))
    banner_text = models.CharField(
        _('Offer Banner Text'), max_length=100, blank=True, null=True)
    start_time = models.DateTimeField(
        _('Start Time'))
    end_time = models.DateTimeField(
        _('End Time'))
    is_active = models.BooleanField(
        _('Active'), default=False)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return self.name if self.name else "Offer - " + str(self.id)

    def clean(self):
        super().clean()
        now = timezone.now()
        if(self.sticky_text and self.banner_text and self.offer_value):
            if (self.start_time and self.end_time):
                if self.is_active:
                    if not (self.end_time < now):
                        if self.start_time > self.end_time:
                            raise ValidationError('End time Cannot be less than Start time')
                        elif self.start_time == self.end_time :
                            raise ValidationError('End time Cannot be same as Start time')
                    else : raise ValidationError('Offer End Date cannot be less than Current Date')
                else:
                    if self.start_time > self.end_time:
                            raise ValidationError('End time Cannot be less than Start time')
                    elif self.start_time == self.end_time :
                            raise ValidationError('End time Cannot be same as Start time')
            else :
                raise ValidationError('Date Time cannot be Empty')
        else:
            raise ValidationError('Sticky Text, Banner Text or Offer value cannot be empty')

    def get_active_offer(self):
        active_offer = HomePageOffer.objects.filter(is_active=True).first()
        return active_offer


class NavigationSpecialTag(AbstractAutoDate):
    display_name = models.CharField(
        _('Display Name'), max_length=25, blank=False, unique=True)
    skill_page_url = models.CharField(
        _('URL of Skill Page'), max_length=60, blank=True)
    tag = models.CharField(
        _('Tag on Display Name (Optional)'), max_length=100,blank=True, null=True, 
            help_text=("For eg. 'New\' or 'Limited time offer\'. Recommended 'New\' only"))
    icon = models.ImageField(
        _('Mobile Icon'), upload_to="images/mobile/homepage/", blank=True, null=True)
    is_active = models.BooleanField(
        _('Active'), default=False)

    class Meta:
        ordering = ['-modified' ,]

    def __str__(self):
        return 'NavTag-' + str(self.id)

    def get_active_navlink(self):
        active_navlink = list(NavigationSpecialTag.objects.filter(is_active=True))
        nav_list = []
        if len(active_navlink):
            if len(active_navlink) >= 2:
                return list(active_navlink[:2])
            nav_list.append(active_navlink[0])
        return nav_list

@receiver(post_save, sender=NavigationSpecialTag)
def latest_active_link_fetch(sender, instance, created, **kwargs):
    data = NavigationSpecialTag().get_active_navlink()
    cache.set('active_homepage_navlink', data, 24*60*60)

        