from itertools import chain

from django.db.models import Q
from django.utils.timezone import now

from . import results
from .models import ConditionalOffer


class OfferApplicationError(Exception):
    pass


class Applicator(object):

    def apply(self, cart, user=None, request=None):
        """
        Apply all relevant offers to the given cart.

        The request is passed too as sometimes the available offers
        are dependent on the user (eg session-based offers).
        """
        offers = self.get_offers(cart, user, request)
        self.apply_offers(cart, offers)

    def apply_offers(self, cart, offers):
        applications = results.OfferApplications()
        for offer in offers:
            num_applications = 0
            # Keep applying the offer until either
            # (a) We reach the max number of applications for the offer.
            # (b) The benefit can't be applied successfully.
            while num_applications < offer.get_max_applications(cart.owner):
                result = offer.apply_benefit(cart)
                num_applications += 1
                if not result.is_successful:
                    break
                applications.add(offer, result)
                if result.is_final:
                    break

        # Store this list of discounts with the cart so it can be
        # rendered in templates
        cart.offer_applications = applications

    def get_offers(self, cart, user=None, request=None):
        """
        Return all offers to apply to the cart.

        This method should be subclassed and extended to provide more
        sophisticated behaviour.  For instance, you could load extra offers
        based on the session or the user type.
        """
        public_offers = self.get_public_offers()
        cart_offers = self.get_cart_offers(cart, user)
        user_offers = self.get_user_offers(user)
        session_offers = self.get_session_offers(request)

        return list(sorted(chain(
            session_offers, cart_offers, user_offers, public_offers),
            key=lambda o: o.priority, reverse=True))

    def get_public_offers(self):
        """
        Return public offers that are available to all users
        """
        cutoff = now()
        date_based = Q(
            Q(start_datetime__lte=cutoff),
            Q(end_datetime__gte=cutoff) | Q(end_datetime=None),
        )

        nondate_based = Q(start_datetime=None, end_datetime=None)

        qs = ConditionalOffer.objects.filter(
            date_based | nondate_based,
            offer_type=ConditionalOffer.PUBLIC,
            status=ConditionalOffer.OPEN)
        return qs.select_related('condition', 'benefit')

    def get_cart_offers(self, cart, user):
        """
        Return cart-linked offers such as those associated with a coupon
        code
        """
        offers = []
        if not cart.id or not user:
            return offers

        for coupon in cart.coupons.all():
            available_to_user, __ = coupon.is_available_to_user(user=user)
            if coupon.is_active() and available_to_user:
                cart_offers = coupon.offers.all()
                for offer in cart_offers:
                    offer.set_coupon(coupon)
                offers = list(chain(offers, cart_offers))
        return offers

    def get_user_offers(self, user):
        # UserType Offers like newly registered 
        return []

    def get_session_offers(self, request):
        # Incomplete Cart or Affiliate
        return []


