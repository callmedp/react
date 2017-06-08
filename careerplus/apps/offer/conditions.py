from decimal import Decimal as D
from decimal import ROUND_UP

from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from . import utils

from .models import Condition

__all__ = [
    'CountCondition', 'CoverageCondition', 'ValueCondition'
]


class CountCondition(Condition):
    """
    An offer condition dependent on the NUMBER of matching items from the
    cart.
    """
    _description = _("cart includes %(count)d item(s) from %(range)s")

    @property
    def name(self):
        return self._description % {
            'count': self.value,
            'range': six.text_type(self.range).lower()}

    @property
    def description(self):
        return self._description % {
            'count': self.value,
            'range': utils.range_anchor(self.range)}

    class Meta:
        app_label = 'offer'
        proxy = True
        verbose_name = _("Count condition")
        verbose_name_plural = _("Count conditions")

    def is_satisfied(self, offer, cart):
        """
        Determines whether a given cart meets this condition
        """
        num_matches = 0
        for line in cart.all_lines():
            if (self.can_apply_condition(line)
                    and line.quantity_without_discount > 0):
                num_matches += line.quantity_without_discount
            if num_matches >= self.value:
                return True
        return False

    def _get_num_matches(self, cart):
        if hasattr(self, '_num_matches'):
            return getattr(self, '_num_matches')
        num_matches = 0
        for line in cart.all_lines():
            if (self.can_apply_condition(line)
                    and line.quantity_without_discount > 0):
                num_matches += line.quantity_without_discount
        self._num_matches = num_matches
        return num_matches

    def is_partially_satisfied(self, offer, cart):
        num_matches = self._get_num_matches(cart)
        return 0 < num_matches < self.value

    def get_upsell_message(self, offer, cart):
        num_matches = self._get_num_matches(cart)
        delta = self.value - num_matches
        return ungettext('Buy %(delta)d more product from %(range)s',
                         'Buy %(delta)d more products from %(range)s', delta) \
            % {'delta': delta, 'range': self.range}

    def consume_items(self, offer, cart, affected_lines):
        """
        Marks items within the cart lines as consumed so they
        can't be reused in other offers.

        :cart: The cart
        :affected_lines: The lines that have been affected by the discount.
                         This should be list of tuples (line, discount, qty)
        """
        # We need to count how many items have already been consumed as part of
        # applying the benefit, so we don't consume too many items.
        num_consumed = 0
        for line, __, quantity in affected_lines:
            num_consumed += quantity
        to_consume = max(0, self.value - num_consumed)
        if to_consume == 0:
            return

        for __, line in self.get_applicable_lines(offer, cart,
                                                  most_expensive_first=True):
            quantity_to_consume = min(line.quantity_without_discount,
                                      to_consume)
            line.consume(quantity_to_consume)
            to_consume -= quantity_to_consume
            if to_consume == 0:
                break


class CoverageCondition(Condition):
    """
    An offer condition dependent on the number of DISTINCT matching items from
    the cart.
    """
    _description = _("cart includes %(count)d distinct item(s) from"
                     " %(range)s")

    @property
    def name(self):
        return self._description % {
            'count': self.value,
            'range': six.text_type(self.range).lower()}

    @property
    def description(self):
        return self._description % {
            'count': self.value,
            'range': utils.range_anchor(self.range)}

    class Meta:
        app_label = 'offer'
        proxy = True
        verbose_name = _("Coverage Condition")
        verbose_name_plural = _("Coverage Conditions")

    def is_satisfied(self, offer, cart):
        """
        Determines whether a given cart meets this condition
        """
        covered_ids = []
        for line in cart.all_lines():
            if not line.is_available_for_discount:
                continue
            product = line.product
            if (self.can_apply_condition(line) and product.id not in
                    covered_ids):
                covered_ids.append(product.id)
            if len(covered_ids) >= self.value:
                return True
        return False

    def _get_num_covered_products(self, cart):
        covered_ids = []
        for line in cart.all_lines():
            if not line.is_available_for_discount:
                continue
            product = line.product
            if (self.can_apply_condition(line) and product.id not in
                    covered_ids):
                covered_ids.append(product.id)
        return len(covered_ids)

    def get_upsell_message(self, offer, cart):
        delta = self.value - self._get_num_covered_products(cart)
        return ungettext('Buy %(delta)d more product from %(range)s',
                         'Buy %(delta)d more products from %(range)s', delta) \
            % {'delta': delta, 'range': self.range}

    def is_partially_satisfied(self, offer, cart):
        return 0 < self._get_num_covered_products(cart) < self.value

    def consume_items(self, offer, cart, affected_lines):
        """
        Marks items within the cart lines as consumed so they
        can't be reused in other offers.
        """
        # Determine products that have already been consumed by applying the
        # benefit
        consumed_products = []
        for line, __, quantity in affected_lines:
            consumed_products.append(line.product)

        to_consume = max(0, self.value - len(consumed_products))
        if to_consume == 0:
            return

        for line in cart.all_lines():
            product = line.product
            if not self.can_apply_condition(line):
                continue
            if product in consumed_products:
                continue
            if not line.is_available_for_discount:
                continue
            # Only consume a quantity of 1 from each line
            line.consume(1)
            consumed_products.append(product)
            to_consume -= 1
            if to_consume == 0:
                break

    def get_value_of_satisfying_items(self, offer, cart):
        covered_ids = []
        value = D('0.00')
        for line in cart.all_lines():
            if (self.can_apply_condition(line) and line.product.id not in
                    covered_ids):
                covered_ids.append(line.product.id)
                value += utils.unit_price(offer, line)
            if len(covered_ids) >= self.value:
                return value
        return value


class ValueCondition(Condition):
    """
    An offer condition dependent on the VALUE of matching items from the
    cart.
    """
    _description = _("cart includes %(amount)s from %(range)s")

    @property
    def name(self):
        return self._description % {
            'amount': self.value,
            'range': six.text_type(self.range).lower()}

    @property
    def description(self):
        return self._description % {
            'amount': self.value,
            'range': utils.range_anchor(self.range)}

    class Meta:
        app_label = 'offer'
        proxy = True
        verbose_name = _("Value condition")
        verbose_name_plural = _("Value conditions")

    def is_satisfied(self, offer, cart):
        """
        Determine whether a given cart meets this condition
        """
        value_of_matches = D('0.00')
        for line in cart.all_lines():
            if (self.can_apply_condition(line) and
                    line.quantity_without_discount > 0):
                price = utils.unit_price(offer, line)
                value_of_matches += price * int(line.quantity_without_discount)
            if value_of_matches >= self.value:
                return True
        return False

    def _get_value_of_matches(self, offer, cart):
        if hasattr(self, '_value_of_matches'):
            return getattr(self, '_value_of_matches')
        value_of_matches = D('0.00')
        for line in cart.all_lines():
            if (self.can_apply_condition(line) and
                    line.quantity_without_discount > 0):
                price = utils.unit_price(offer, line)
                value_of_matches += price * int(line.quantity_without_discount)
        self._value_of_matches = value_of_matches
        return value_of_matches

    def is_partially_satisfied(self, offer, cart):
        value_of_matches = self._get_value_of_matches(offer, cart)
        return D('0.00') < value_of_matches < self.value

    def get_upsell_message(self, offer, cart):
        value_of_matches = self._get_value_of_matches(offer, cart)
        return _('Spend %(value)s more from %(range)s') % {
            'value': self.value - value_of_matches,
            'range': self.range}

    def consume_items(self, offer, cart, affected_lines):
        """
        Marks items within the cart lines as consumed so they
        can't be reused in other offers.

        We allow lines to be passed in as sometimes we want them sorted
        in a specific order.
        """
        # Determine value of items already consumed as part of discount
        value_consumed = D('0.00')
        for line, __, qty in affected_lines:
            price = utils.unit_price(offer, line)
            value_consumed += price * qty

        to_consume = max(0, self.value - value_consumed)
        if to_consume == 0:
            return

        for price, line in self.get_applicable_lines(
                offer, cart, most_expensive_first=True):
            quantity_to_consume = min(
                line.quantity_without_discount,
                (to_consume / price).quantize(D(1), ROUND_UP))
            line.consume(quantity_to_consume)
            to_consume -= price * quantity_to_consume
            if to_consume <= 0:
                break
