# from decimal import Decimal as D

# from django.utils.translation import ugettext_lazy as _

# from . import conditions, results, utils
# from .models import Benefit


# __all__ = [
#     'PercentageDiscountBenefit', 'AbsoluteDiscountBenefit',
#     'MultibuyDiscountBenefit',
# ]


# def apply_discount(line, discount, quantity):
#     """
#     Apply a given discount to the passed cart
#     """
#     line.discount(discount, quantity, incl_tax=False)


# class PercentageDiscountBenefit(Benefit):
#     """
#     An offer benefit that gives a percentage discount
#     """
#     _description = _("%(value)s%% discount on %(range)s")

#     @property
#     def name(self):
#         return self._description % {
#             'value': self.value,
#             'range': self.range.name}

#     @property
#     def description(self):
#         return self._description % {
#             'value': self.value,
#             'range': utils.range_anchor(self.range)}

#     class Meta:
#         app_label = 'offer'
#         proxy = True
#         verbose_name = _("Percentage discount benefit")
#         verbose_name_plural = _("Percentage discount benefits")

#     def apply(self, cart, condition, offer, discount_percent=None,
#               max_total_discount=None):
#         if discount_percent is None:
#             discount_percent = self.value

#         discount_amount_available = max_total_discount

#         line_tuples = self.get_applicable_lines(offer, cart)
#         discount_percent = min(discount_percent, D('100.0'))
#         discount = D('0.00')
#         affected_items = 0
#         max_affected_items = self._effective_max_affected_items()
#         affected_lines = []
#         for price, line in line_tuples:
#             if affected_items >= max_affected_items:
#                 break
#             if discount_amount_available == 0:
#                 break

#             quantity_affected = min(line.quantity_without_discount,
#                                     max_affected_items - affected_items)
#             line_discount = self.round(discount_percent / D('100.0') * price
#                                        * int(quantity_affected))

#             if discount_amount_available is not None:
#                 line_discount = min(line_discount, discount_amount_available)
#                 discount_amount_available -= line_discount

#             apply_discount(line, line_discount, quantity_affected)

#             affected_lines.append((line, line_discount, quantity_affected))
#             affected_items += quantity_affected
#             discount += line_discount

#         if discount > 0:
#             condition.consume_items(offer, cart, affected_lines)
#         return results.CartDiscount(discount)


# class AbsoluteDiscountBenefit(Benefit):
#     """
#     An offer benefit that gives an absolute discount
#     """
#     _description = _("%(value)s discount on %(range)s")

#     @property
#     def name(self):
#         return self._description % {
#             'value': self.value,
#             'range': self.range.name.lower()}

#     @property
#     def description(self):
#         return self._description % {
#             'value': self.value,
#             'range': utils.range_anchor(self.range)}

#     class Meta:
#         app_label = 'offer'
#         proxy = True
#         verbose_name = _("Absolute discount benefit")
#         verbose_name_plural = _("Absolute discount benefits")

#     def apply(self, cart, condition, offer, discount_amount=None,
#               max_total_discount=None):
#         if discount_amount is None:
#             discount_amount = self.value

#         # Fetch cart lines that are in the range and available to be used in
#         # an offer.
#         line_tuples = self.get_applicable_lines(offer, cart)

#         # Determine which lines can have the discount applied to them
#         max_affected_items = self._effective_max_affected_items()
#         num_affected_items = 0
#         affected_items_total = D('0.00')
#         lines_to_discount = []
#         for price, line in line_tuples:
#             if num_affected_items >= max_affected_items:
#                 break
#             qty = min(line.quantity_without_discount,
#                       max_affected_items - num_affected_items)
#             lines_to_discount.append((line, price, qty))
#             num_affected_items += qty
#             affected_items_total += qty * price

#         # Ensure we don't try to apply a discount larger than the total of the
#         # matching items.
#         discount = min(discount_amount, affected_items_total)
#         if max_total_discount is not None:
#             discount = min(discount, max_total_discount)

#         if discount == 0:
#             return results.ZERO_DISCOUNT

#         # Apply discount equally amongst them
#         affected_lines = []
#         applied_discount = D('0.00')
#         for i, (line, price, qty) in enumerate(lines_to_discount):
#             if i == len(lines_to_discount) - 1:
#                 # If last line, then take the delta as the discount to ensure
#                 # the total discount is correct and doesn't mismatch due to
#                 # rounding.
#                 line_discount = discount - applied_discount
#             else:
#                 # Calculate a weighted discount for the line
#                 line_discount = self.round(
#                     ((price * qty) / affected_items_total) * discount)
#             apply_discount(line, line_discount, qty)
#             affected_lines.append((line, line_discount, qty))
#             applied_discount += line_discount

#         condition.consume_items(offer, cart, affected_lines)

#         return results.CartDiscount(discount)


# class MultibuyDiscountBenefit(Benefit):
#     _description = _("Cheapest product from %(range)s is free")

#     @property
#     def name(self):
#         return self._description % {
#             'range': self.range.name.lower()}

#     @property
#     def description(self):
#         return self._description % {
#             'range': utils.range_anchor(self.range)}

#     class Meta:
#         app_label = 'offer'
#         proxy = True
#         verbose_name = _("Multibuy discount benefit")
#         verbose_name_plural = _("Multibuy discount benefits")

#     def apply(self, cart, condition, offer):
#         line_tuples = self.get_applicable_lines(offer, cart)
#         if not line_tuples:
#             return results.ZERO_DISCOUNT

#         # Cheapest line gives free product
#         discount, line = line_tuples[0]
#         apply_discount(line, discount, 1)

#         affected_lines = [(line, discount, 1)]
#         condition.consume_items(offer, cart, affected_lines)

#         return results.CartDiscount(discount)

