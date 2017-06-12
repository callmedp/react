# import itertools
# import operator

# from decimal import Decimal as D
# from django.core import exceptions
# from django.db import models
# from django.db.models.query import Q
# from django.utils.translation import ugettext_lazy as _
# from django.utils.timezone import get_current_timezone, now
# from django.utils.functional import cached_property
# from django.template.defaultfilters import date as date_filter

# from ckeditor.fields import RichTextField

# from seo.models import AbstractSEO, AbstractAutoDate

# from decimal import ROUND_DOWN

# from . import results, utils
# from .managers import ActiveOfferManager, BrowsableRangeManager


# class ConditionalOffer(AbstractAutoDate, AbstractSEO):
#     """
#     (eg. buy 1, get 10% off)
#     """
#     name = models.CharField(
#         _("Name"), max_length=128, unique=True,
#         help_text=_("This is displayed on website if made public"))
#     slug = models.CharField(
#         _('Slug'), unique=True,
#         max_length=100, help_text=_('Unique slug'))
#     description = RichTextField(
#         verbose_name=_('Description'), blank=True,
#         default='', help_text=_("This is displayed on the offer"))
#     PUBLIC, COUPON, USER, SESSION, DEFAULT = (1, 2, 3, 4, 0)
#     TYPE_CHOICES = (
#         (DEFAULT, _("Initial/Default")),
#         (PUBLIC, _("Site offer - available to all users")),
#         (COUPON,
#             _("Coupon offer - only available after entering the coupon code")),
#         (USER, _("User offer - available to certain types of user")),
#         (SESSION, _("Session/Affiliate offer - temporary offer, available for "
#                     "a user for the duration of their session")),
#     )
#     offer_type = models.PositiveSmallIntegerField(
#         _("Type"), choices=TYPE_CHOICES, default=DEFAULT)
#     OPEN, SUSPENDED, CONSUMED = (0, 1, 2)
#     TYPE_STATUS = (
#         (OPEN, _("Open Offer -- Valid/Active")),
#         (SUSPENDED, _("Suspended Offer -- Not Valid/Active ")),
#         (CONSUMED, _("Consumed offer - Used on site")),
#     )
#     status = models.PositiveSmallIntegerField(
#         _("Status"), choices=TYPE_STATUS, default=OPEN)

#     condition = models.ForeignKey(
#         'offer.Condition',
#         on_delete=models.CASCADE,
#         verbose_name=_("Condition"))
#     benefit = models.ForeignKey(
#         'offer.Benefit',
#         on_delete=models.CASCADE,
#         verbose_name=_("Benefit"))
#     priority = models.IntegerField(
#         _("Priority"), default=0,
#         help_text=_("The highest priority offers are visible first"))
#     # Required to ensure offer is not used outside a give date range
#     start_datetime = models.DateTimeField(
#         _("Start date"), blank=True, null=True)
#     end_datetime = models.DateTimeField(
#         _("End date"), blank=True, null=True,
#         help_text=_("Offers are active until the end of the 'end date'"))

#     max_global_applications = models.PositiveIntegerField(
#         _("Max global applications"),
#         help_text=_("The number of times this offer can be used before it "
#                     "is unavailable"), blank=True, null=True)
#     max_user_applications = models.PositiveIntegerField(
#         _("Max user applications"),
#         help_text=_("The number of times a single user can use this offer"),
#         blank=True, null=True)
#     max_cart_applications = models.PositiveIntegerField(
#         _("Max cart applications"),
#         blank=True, null=True,
#         help_text=_("The number of times this offer can be applied to a "
#                     "cart (and order)"))
#     max_discount = models.DecimalField(
#         _("Max discount"), decimal_places=2, max_digits=12, null=True,
#         blank=True,
#         help_text=_("When an offer has given more discount to orders "
#                     "than this threshold, then the offer becomes "
#                     "unavailable"))
#     total_discount = models.DecimalField(
#         _("Total Discount"), decimal_places=2, max_digits=12,
#         default=D('0.00'))
#     num_applications = models.PositiveIntegerField(
#         _("Number of applications"), default=0)
#     num_orders = models.PositiveIntegerField(
#         _("Number of Orders"), default=0)
#     _coupon = None

#     objects = models.Manager()
#     active = ActiveOfferManager()

#     class Meta:
#         app_label = 'offer'
#         ordering = ['-created', 'pk']
#         verbose_name = _("Conditional offer")
#         verbose_name_plural = _("Conditional offers")

#     def save(self, *args, **kwargs):
#         if not self.is_suspended:
#             if self.get_max_applications() == 0:
#                 self.status = self.CONSUMED
#             else:
#                 self.status = self.OPEN
#         return super(ConditionalOffer, self).save(*args, **kwargs)

#     def __str__(self):
#         return self.name

#     def clean(self):
#         if (self.start_datetime and self.end_datetime and
#                 self.start_datetime > self.end_datetime):
#             raise exceptions.ValidationError(
#                 _('End date should be later than start date'))

#     @property
#     def is_open(self):
#         return self.status == self.OPEN

#     @property
#     def is_suspended(self):
#         return self.status == self.SUSPENDED

#     def suspend(self):
#         self.status = self.SUSPENDED
#         self.save()
#     suspend.alters_data = True

#     def unsuspend(self):
#         self.status = self.OPEN
#         self.save()
#     unsuspend.alters_data = True

#     def is_available(self, user=None, test_date=None):
#         if self.is_suspended:
#             return False
#         if test_date is None:
#             test_date = now()
#         predicates = []
#         if self.start_datetime:
#             predicates.append(self.start_datetime > test_date)
#         if self.end_datetime:
#             predicates.append(test_date > self.end_datetime)
#         if any(predicates):
#             return False
#         return self.get_max_applications(user) > 0

#     def is_condition_satisfied(self, basket):
#         return self.condition.proxy().is_satisfied(self, basket)

#     def is_condition_partially_satisfied(self, basket):
#         return self.condition.proxy().is_partially_satisfied(self, basket)

#     def get_upsell_message(self, basket):
#         return self.condition.proxy().get_upsell_message(self, basket)

#     def apply_benefit(self, cart):
#         # if not self.is_condition_satisfied(cart):
#         #     return results.ZERO_DISCOUNT
#         return self.benefit.proxy().apply(
#             cart, self.condition.proxy(), self)

#     def apply_deferred_benefit(self, cart, order, application):
#         return self.benefit.proxy().apply_deferred(cart, order, application)

#     def set_coupon(self, coupon):
#         self._coupon = coupon

#     def get_coupon(self):
#         return self._coupon

#     def get_max_applications(self, user=None):
#         if self.max_discount and self.total_discount >= self.max_discount:
#             return 0
#         limits = [10]
#         if self.max_user_applications and user:
#             limits.append(max(0, self.max_user_applications -
#                           self.get_num_user_applications(user)))
#         if self.max_basket_applications:
#             limits.append(self.max_basket_applications)
#         if self.max_global_applications:
#             limits.append(
#                 max(0, self.max_global_applications - self.num_applications))
#         return min(limits)

#     def get_num_user_applications(self, user):
#         pass
#         # OrderDiscount = get_model('order', 'OrderDiscount')
#         # aggregates = OrderDiscount.objects.filter(offer_id=self.id,
#         #                                           order__user=user)\
#         #     .aggregate(total=models.Sum('frequency'))
#         # return aggregates['total'] if aggregates['total'] is not None else 0

#     def shipping_discount(self, charge):
#         return self.benefit.proxy().shipping_discount(charge)

#     def record_usage(self, discount):
#         self.num_applications += discount['freq']
#         self.total_discount += discount['discount']
#         self.num_orders += 1
#         self.save()
#     record_usage.alters_data = True

#     def availability_description(self):
#         """
#         Return a description of when this offer is available
#         """
#         restrictions = self.availability_restrictions()
#         descriptions = [r['description'] for r in restrictions]
#         return "<br/>".join(descriptions)

#     def availability_restrictions(self):  # noqa (too complex (15))
#         restrictions = []
#         if self.is_suspended:
#             restrictions.append({
#                 'description': _("Offer is suspended"),
#                 'is_satisfied': False})

#         if self.max_global_applications:
#             remaining = self.max_global_applications - self.num_applications
#             desc = _("Limited to %(total)d uses (%(remainder)d remaining)") \
#                 % {'total': self.max_global_applications,
#                    'remainder': remaining}
#             restrictions.append({'description': desc,
#                                  'is_satisfied': remaining > 0})

#         if self.max_user_applications:
#             if self.max_user_applications == 1:
#                 desc = _("Limited to 1 use per user")
#             else:
#                 desc = _("Limited to %(total)d uses per user") \
#                     % {'total': self.max_user_applications}
#             restrictions.append({'description': desc,
#                                  'is_satisfied': True})

#         if self.max_basket_applications:
#             if self.max_user_applications == 1:
#                 desc = _("Limited to 1 use per basket")
#             else:
#                 desc = _("Limited to %(total)d uses per basket") \
#                     % {'total': self.max_basket_applications}
#             restrictions.append({
#                 'description': desc,
#                 'is_satisfied': True})

#         def hide_time_if_zero(dt):
#             # Only show hours/minutes if they have been specified
#             if dt.tzinfo:
#                 localtime = dt.astimezone(get_current_timezone())
#             else:
#                 localtime = dt
#             if localtime.hour == 0 and localtime.minute == 0:
#                 return date_filter(localtime, 'd/m/Y')
#             return date_filter(localtime, 'd/m/Y')

#         if self.start_datetime or self.end_datetime:
#             today = now()
#             if self.start_datetime and self.end_datetime:
#                 desc = _("Available between %(start)s and %(end)s") \
#                     % {'start': hide_time_if_zero(self.start_datetime),
#                        'end': hide_time_if_zero(self.end_datetime)}
#                 is_satisfied \
#                     = self.start_datetime <= today <= self.end_datetime
#             elif self.start_datetime:
#                 desc = _("Available from %(start)s") % {
#                     'start': hide_time_if_zero(self.start_datetime)}
#                 is_satisfied = today >= self.start_datetime
#             elif self.end_datetime:
#                 desc = _("Available until %(end)s") % {
#                     'end': hide_time_if_zero(self.end_datetime)}
#                 is_satisfied = today <= self.end_datetime
#             restrictions.append({
#                 'description': desc,
#                 'is_satisfied': is_satisfied})

#         if self.max_discount:
#             desc = _("Limited to a cost of %(max)s") % {
#                 'max': self.max_discount}
#             restrictions.append({
#                 'description': desc,
#                 'is_satisfied': self.total_discount < self.max_discount})

#         return restrictions

#     @property
#     def has_products(self):
#         return self.condition.range is not None

#     def products(self):
#         """
#         Return a queryset of products in this offer
#         """
#         from shop.models import Product
#         if not self.has_products:
#             return Product.objects.none()

#         cond_range = self.condition.range
#         if cond_range.includes_all_products:
#             queryset = Product.objects.filter(active=True)
#         else:
#             queryset = cond_range.all_products()
#         return queryset.filter(is_discountable=True)#.exclude(structure=Product.CHILD)


# class Benefit(models.Model):
#     range = models.ForeignKey(
#         'offer.Range',
#         blank=True,
#         null=True,
#         on_delete=models.CASCADE,
#         verbose_name=_("Range"))

#     PERCENTAGE, FIXED, MULTIBUY = (
#         0, 1, 2)
#     TYPE_CHOICES = (
#         (PERCENTAGE, _("Discount is a percentage off of the product's value")),
#         (FIXED, _("Discount is a fixed amount off of the product's value")),
#         (MULTIBUY, _("Discount is to give the cheapest product for free")),)
#     type = models.PositiveSmallIntegerField(
#         _("Type"), choices=TYPE_CHOICES, default=FIXED)
#     value = models.DecimalField(
#         _("Value"), decimal_places=2, max_digits=12, default=D('0.00'))
#     max_affected_items = models.PositiveIntegerField(
#         _("Max Affected Items"), blank=True, null=True,
#         help_text=_("Set this to prevent the discount consuming all items "
#                     "within the range that are in the cart."))
#     proxy_class = models.CharField(
#         _("Custom class"), max_length=255, blank=True, null=True)

#     class Meta:
#         app_label = 'offer'
#         verbose_name = _("Benefit")
#         verbose_name_plural = _("Benefits")

#     def proxy(self):
#         from oscar.apps.offer import benefits

#         klassmap = {
#             self.PERCENTAGE: benefits.PercentageDiscountBenefit,
#             self.FIXED: benefits.AbsoluteDiscountBenefit,
#             self.MULTIBUY: benefits.MultibuyDiscountBenefit,
#         }
#         # Short-circuit logic if current class is already a proxy class.
#         if self.__class__ in klassmap.values():
#             return self

#         field_dict = dict(self.__dict__)
#         for field in list(field_dict.keys()):
#             if field.startswith('_'):
#                 del field_dict[field]

#         if self.proxy_class:
#             klass = utils.load_proxy(self.proxy_class)
#             # Short-circuit again.
#             if self.__class__ == klass:
#                 return self
#             return klass(**field_dict)

#         if self.type in klassmap:
#             return klassmap[self.type](**field_dict)
#         raise RuntimeError("Unrecognised benefit type (%s)" % self.type)

#     def __str__(self):
#         return self.name

#     @property
#     def name(self):
#         """
#         A plaintext description of the benefit. Every proxy class has to
#         implement it.

#         This is used in the dropdowns within the offer dashboard.
#         """
#         return self.proxy().name

#     @property
#     def description(self):
#         """
#         A description of the benefit.
#         Defaults to the name. May contain HTML.
#         """
#         return self.name

#     def apply(self, basket, condition, offer):
#         return results.ZERO_DISCOUNT

#     def apply_deferred(self, basket, order, application):
#         return None

#     def clean(self):
#         if not self.type:
#             return
#         method_name = 'clean_%s' % self.type.lower().replace(' ', '_')
#         if hasattr(self, method_name):
#             getattr(self, method_name)()

#     def clean_multibuy(self):
#         if not self.range:
#             raise exceptions.ValidationError(
#                 _("Multibuy benefits require a product range"))
#         if self.value:
#             raise exceptions.ValidationError(
#                 _("Multibuy benefits don't require a value"))
#         if self.max_affected_items:
#             raise exceptions.ValidationError(
#                 _("Multibuy benefits don't require a 'max affected items' "
#                   "attribute"))

#     def clean_percentage(self):
#         if not self.range:
#             raise exceptions.ValidationError(
#                 _("Percentage benefits require a product range"))
#         if not self.value:
#             raise exceptions.ValidationError(
#                 _("Percentage discount benefits require a value"))
#         if self.value > 100:
#             raise exceptions.ValidationError(
#                 _("Percentage discount cannot be greater than 100"))

#     def clean_fixed_price(self):
#         if self.range:
#             raise exceptions.ValidationError(
#                 _("No range should be selected as the condition range will "
#                   "be used instead."))

#     def clean_absolute(self):
#         if not self.range:
#             raise exceptions.ValidationError(
#                 _("Fixed discount benefits require a product range"))
#         if not self.value:
#             raise exceptions.ValidationError(
#                 _("Fixed discount benefits require a value"))

#     def round(self, amount):
#         """
#         Apply rounding to discount amount
#         """
#         return amount.quantize(D('.01'), ROUND_DOWN)

#     def _effective_max_affected_items(self):
#         """
#         Return the maximum number of items that can have a discount applied
#         during the application of this benefit
#         """
#         return self.max_affected_items if self.max_affected_items else 10

#     def can_apply_benefit(self, line):
#         """
#         Determines whether the benefit can be applied to a given basket line
#         """
#         return line.stockrecord and line.product.is_discountable

#     def get_applicable_lines(self, offer, basket, range=None):
#         """
#         Return the basket lines that are available to be discounted

#         :basket: The basket
#         :range: The range of products to use for filtering.  The fixed-price
#                 benefit ignores its range and uses the condition range
#         """
#         if range is None:
#             range = self.range
#         line_tuples = []
#         for line in basket.all_lines():
#             product = line.product

#             if (not range.contains(product) or
#                     not self.can_apply_benefit(line)):
#                 continue

#             price = utils.unit_price(offer, line)
#             if not price:
#                 # Avoid zero price products
#                 continue
#             if line.quantity_without_discount == 0:
#                 continue
#             line_tuples.append((price, line))

#         # We sort lines to be cheapest first to ensure consistent applications
#         return sorted(line_tuples, key=operator.itemgetter(0))

#     def shipping_discount(self, charge):
#         return D('0.00')


# class Condition(models.Model):
#     """
#     A condition for an offer to be applied. You can either specify a custom
#     proxy class, or need to specify a type, range and value.
#     """
#     COUNT, VALUE, COVERAGE = (0, 1, 2)
#     TYPE_CHOICES = (
#         (COUNT, _("Depends on number of items in cart that are in "
#                   "condition range")),
#         (VALUE, _("Depends on value of items in cart that are in "
#                   "condition range")),
#         (COVERAGE, _("Needs to contain a set number of DISTINCT items "
#                      "from the condition range")))
#     range = models.ForeignKey(
#         'offer.Range',
#         blank=True,
#         null=True,
#         on_delete=models.CASCADE,
#         verbose_name=_("Range"))
#     type = models.PositiveSmallIntegerField(
#         _('Type'), choices=TYPE_CHOICES, default=VALUE)
#     value = models.DecimalField(
#         _('Value'), decimal_places=2, max_digits=12, default=D('0.00'))

#     proxy_class = models.CharField(
#         _("Custom class"), max_length=255, blank=True, null=True)

#     class Meta:
#         abstract = True
#         app_label = 'offer'
#         verbose_name = _("Condition")
#         verbose_name_plural = _("Conditions")

#     def proxy(self):
#         """
#         Return the proxy model
#         """
#         from . import conditions

#         klassmap = {
#             self.COUNT: conditions.CountCondition,
#             self.VALUE: conditions.ValueCondition,
#             self.COVERAGE: conditions.CoverageCondition
#         }
#         # Short-circuit logic if current class is already a proxy class.
#         if self.__class__ in klassmap.values():
#             return self

#         field_dict = dict(self.__dict__)
#         for field in list(field_dict.keys()):
#             if field.startswith('_'):
#                 del field_dict[field]

#         if self.proxy_class:
#             klass = utils.load_proxy(self.proxy_class)
#             # Short-circuit again.
#             if self.__class__ == klass:
#                 return self
#             return klass(**field_dict)
#         if self.type in klassmap:
#             return klassmap[self.type](**field_dict)
#         raise RuntimeError("Unrecognised condition type (%s)" % self.type)

#     def __str__(self):
#         return self.name

#     @property
#     def name(self):
#         """
#         A plaintext description of the condition. Every proxy class has to
#         implement it.

#         This is used in the dropdowns within the offer dashboard.
#         """
#         return self.proxy().name

#     @property
#     def description(self):
#         """
#         A description of the condition.
#         Defaults to the name. May contain HTML.
#         """
#         return self.name

#     def consume_items(self, offer, cart, affected_lines):
#         pass

#     def is_satisfied(self, offer, cart):
#         """
#         Determines whether a given basket meets this condition.  This is
#         stubbed in this top-class object.  The subclassing proxies are
#         responsible for implementing it correctly.
#         """
#         return False

#     def is_partially_satisfied(self, offer, cart):
#         """
#         Determine if the basket partially meets the condition.  This is useful
#         for up-selling messages to entice customers to buy something more in
#         order to qualify for an offer.
#         """
#         return False

#     def get_upsell_message(self, offer, cart):
#         return None

#     def can_apply_condition(self, line):
#         """
#         Determines whether the condition can be applied to a given basket line
#         """
#         product = line.product
#         return (self.range.contains_product(product) and product.get_is_discountable())

#     def get_applicable_lines(self, offer, cart, most_expensive_first=True):
#         """
#         Return line data for the lines that can be consumed by this condition
#         """
#         line_tuples = []
#         for line in cart.all_lines():
#             if not self.can_apply_condition(line):
#                 continue

#             price = utils.unit_price(offer, line)
#             if not price:
#                 continue
#             line_tuples.append((price, line))
#         key = operator.itemgetter(0)
#         if most_expensive_first:
#             return sorted(line_tuples, reverse=True, key=key)
#         return sorted(line_tuples, key=key)

    
# class Range(AbstractAutoDate, AbstractSEO):
#     """
#     Represents a range of products that can be used within an offer.

#     Ranges only support adding parent or stand-alone products. Offers will
#     consider child products automatically.
#     """
#     name = models.CharField(
#         _("Name"), max_length=128, unique=True,
#         help_text=_("This is displayed on website if made public"))
#     slug = models.CharField(
#         _('Slug'), unique=True,
#         max_length=100, help_text=_('Unique slug'))
#     description = models.TextField(blank=True)

#     # Whether this range is public
#     is_public = models.BooleanField(
#         _('Is public?'), default=False,
#         help_text=_("Public ranges have a customer-facing page"))

#     includes_all_products = models.BooleanField(
#         _('Includes all products?'), default=False)

#     included_products = models.ManyToManyField(
#         'shop.Product', related_name='includes', blank=True,
#         verbose_name=_("Included Products"), through='offer.RangeProduct')
#     excluded_products = models.ManyToManyField(
#         'shop.Product', related_name='excludes', blank=True,
#         verbose_name=_("Excluded Products"))
#     included_categories = models.ManyToManyField(
#         'shop.Category', related_name='includes', blank=True,
#         verbose_name=_("Included Categories"))

#     proxy_class = models.CharField(
#         _("Custom class"), max_length=255, blank=True, null=True)

#     date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)

#     __included_product_ids = None
#     __excluded_product_ids = None
#     __class_ids = None
#     __category_ids = None

#     objects = models.Manager()
#     browsable = BrowsableRangeManager()

#     class Meta:
#         abstract = True
#         app_label = 'offer'
#         verbose_name = _("Range")
#         verbose_name_plural = _("Ranges")

#     def __str__(self):
#         return self.name

#     @cached_property
#     def proxy(self):
#         if self.proxy_class:
#             return utils.load_proxy(self.proxy_class)()

#     def add_product(self, product, display_order=None):
#         """ Add product to the range

#         When adding product that is already in the range, prevent re-adding it.
#         If display_order is specified, update it.

#         Default display_order for a new product in the range is 0; this puts
#         the product at the top of the list.
#         """

#         initial_order = display_order or 0
#         from .models import RangeProduct
#         relation, __ = RangeProduct.objects.get_or_create(
#             range=self, product=product,
#             defaults={'display_order': initial_order})

#         if (display_order is not None and
#                 relation.display_order != display_order):
#             relation.display_order = display_order
#             relation.save()

#         # Remove product from excluded products if it was removed earlier and
#         # re-added again, thus it returns back to the range product list.
#         if product.id in self._excluded_product_ids():
#             self.excluded_products.remove(product)
#             self.invalidate_cached_ids()

#     def remove_product(self, product):
#         """
#         Remove product from range. To save on queries, this function does not
#         check if the product is in fact in the range.
#         """
#         from .models import RangeProduct
#         RangeProduct.objects.filter(range=self, product=product).delete()
#         # Making sure product will be excluded from range products list by adding to
#         # respective field. Otherwise, it could be included as a product from included
#         # category or etc.
#         self.excluded_products.add(product)
#         # Invalidating cached property value with list of IDs of already excluded products.
#         self.invalidate_cached_ids()

#     def contains_product(self, product):  # noqa (too complex (12))
#         """
#         Check whether the passed product is part of this range.
#         """

#         # Delegate to a proxy class if one is provided
#         if self.proxy:
#             return self.proxy.contains_product(product)

#         excluded_product_ids = self._excluded_product_ids()
#         if product.id in excluded_product_ids:
#             return False
#         if self.includes_all_products:
#             return True
#         included_product_ids = self._included_product_ids()
#         # If the product's parent is in the range, the child is automatically included as well
#         if product.is_child and product.parent.id in included_product_ids:
#             return True
#         if product.id in included_product_ids:
#             return True
#         # test_categories = self.included_categories.all()
#         # if test_categories:
#         #     for category in product.get_categories().all():
#         #         for test_category in test_categories:
#         #             if category == test_category \
#         #                     or category.is_descendant_of(test_category):
#         #                 return True
#         return False

#     # Shorter alias
#     contains = contains_product

#     def __get_pks_and_child_pks(self, queryset):
#         """
#         Expects a product queryset; gets the primary keys of the passed
#         products and their children.

#         Verbose, but database and memory friendly.
#         """
#         # # One query to get parent and children; [(4, None), (5, 10), (5, 11)]
#         # pk_tuples_iterable = queryset.values_list('pk', 'children__pk')
#         # # Flatten list without unpacking; [4, None, 5, 10, 5, 11]
#         # flat_iterable = itertools.chain.from_iterable(pk_tuples_iterable)
#         # # Ensure uniqueness and remove None; {4, 5, 10, 11}
#         # return set(flat_iterable) - {None}

#     def _included_product_ids(self):
#         if not self.id:
#             return []
#         if self.__included_product_ids is None:
#             self.__included_product_ids = self.__get_pks_and_child_pks(
#                 self.included_products)
#         return self.__included_product_ids

#     def _excluded_product_ids(self):
#         if not self.id:
#             return []
#         if self.__excluded_product_ids is None:
#             self.__excluded_product_ids = self.__get_pks_and_child_pks(
#                 self.excluded_products)
#         return self.__excluded_product_ids

#     def _class_ids(self):
#         if self.__class_ids is None:
#             self.__class_ids = self.classes.values_list('pk', flat=True)
#         return self.__class_ids

#     def _category_ids(self):
#         # if self.__category_ids is None:
#         #     category_ids_list = list(
#         #         self.included_categories.values_list('pk', flat=True))
#         #     for category in self.included_categories.all():
#         #         children_ids = category.get_descendants().values_list(
#         #             'pk', flat=True)
#         #         category_ids_list.extend(list(children_ids))

#         #     self.__category_ids = category_ids_list

#         # return self.__category_ids

#     def invalidate_cached_ids(self):
#         self.__category_ids = None
#         self.__included_product_ids = None
#         self.__excluded_product_ids = None

#     def num_products(self):
#         # Delegate to a proxy class if one is provided
#         if self.proxy:
#             return self.proxy.num_products()
#         if self.includes_all_products:
#             return None
#         return self.all_products().count()

#     def all_products(self):
#         """
#         Return a queryset containing all the products in the range

#         This includes included_products plus the products contained in the
#         included classes and categories, minus the products in
#         excluded_products.
#         """
#         if self.proxy:
#             return self.proxy.all_products()

#         from shop.models import Product
#         if self.includes_all_products:
#             # Filter out child products
#             return Product.browsable.all()

#         return Product.objects.filter(
#             Q(id__in=self._included_product_ids()) |
#             Q(product_class_id__in=self._class_ids()) |
#             Q(productcategory__category_id__in=self._category_ids())
#         ).exclude(id__in=self._excluded_product_ids()).distinct()

#     @property
#     def is_editable(self):
#         """
#         Test whether this range can be edited in the dashboard.
#         """
#         return not self.proxy_class

#     @property
#     def is_reorderable(self):
#         """
#         Test whether products for the range can be re-ordered.
#         """
#         return len(self._class_ids()) == 0 and len(self._category_ids()) == 0


# class RangeProduct(models.Model):
#     """
#     Allow ordering products inside ranges
#     Exists to allow customising.
#     """
#     range = models.ForeignKey('offer.Range', on_delete=models.CASCADE)
#     product = models.ForeignKey('catalogue.Product', on_delete=models.CASCADE)
#     display_order = models.IntegerField(default=0)

#     class Meta:
#         app_label = 'offer'
#         unique_together = ('range', 'product')
