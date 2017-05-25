from decimal import Decimal as D


class OfferApplications(object):
    """
    A collection of offer applications and the discounts that they give.

    Each offer application is stored as a dict which has fields for:

    * The offer that led to the successful application
    * The result instance
    * The number of times the offer was successfully applied
    """
    def __init__(self):
        self.applications = {}

    def __iter__(self):
        return self.applications.values().__iter__()

    def __len__(self):
        return len(self.applications)

    def add(self, offer, result):
        if offer.id not in self.applications:
            self.applications[offer.id] = {
                'offer': offer,
                'result': result,
                'name': offer.name,
                'description': result.description,
                'coupon': offer.get_coupon(),
                'freq': 0,
                'discount': D('0.00')}
        self.applications[offer.id]['discount'] += result.discount
        self.applications[offer.id]['freq'] += 1

    @property
    def offer_discounts(self):
        """
        Return cart discounts from offers (but not coupon offers)
        """
        discounts = []
        for application in self.applications.values():
            if not application['coupon'] and application['discount'] > 0:
                discounts.append(application)
        return discounts

    @property
    def coupon_discounts(self):
        """
        Return cart discounts from coupons.
        """
        discounts = []
        for application in self.applications.values():
            if application['coupon'] and application['discount'] > 0:
                discounts.append(application)
        return discounts

    @property
    def grouped_coupon_discounts(self):
        """
        Return coupon discounts aggregated up to the coupon level.

        This is different to the coupon_discounts property as a coupon can
        have multiple offers associated with it.
        """
        coupon_discounts = {}
        for application in self.coupon_discounts:
            coupon = application['coupon']
            if coupon.code not in coupon_discounts:
                coupon_discounts[coupon.code] = {
                    'coupon': coupon,
                    'discount': application['discount'],
                }
            else:
                coupon_discounts[coupon.code] += application.discount
        return coupon_discounts.values()

    @property
    def post_order_actions(self):
        """
        Return successful offer applications which didn't lead to a discount
        """
        applications = []
        for application in self.applications.values():
            if application['result'].affects_post_order:
                applications.append(application)
        return applications

    @property
    def offers(self):
        """
        Return a dict of offers that were successfully applied
        """
        return dict([(a['offer'].id, a['offer']) for a in
                     self.applications.values()])


class ApplicationResult(object):
    is_final = is_successful = False
    # Cart discount
    discount = D('0.00')
    description = None

    # Offer applications can affect 3 distinct things
    # (a) Give a discount off the Cart total
    # (b) Trigger a post-order action
    CART, POST_ORDER = 0, 1
    affects = None

    @property
    def affects_cart(self):
        return self.affects == self.CART

    @property
    def affects_post_order(self):
        return self.affects == self.POST_ORDER


class CartDiscount(ApplicationResult):
    """
    For when an offer application leads to a simple discount off the cart's
    total
    """
    affects = ApplicationResult.CART

    def __init__(self, amount):
        self.discount = amount

    @property
    def is_successful(self):
        return self.discount > 0

    def __str__(self):
        return '<Cart discount of %s>' % self.discount

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.discount)


# Helper global as returning zero discount is quite common
ZERO_DISCOUNT = CartDiscount(D('0.00'))


class PostOrderAction(ApplicationResult):
    """
    For when an offer condition is met but the benefit is deferred until after
    the order has been placed.  Eg buy 2 books and get 100 loyalty points.
    """
    is_final = is_successful = True
    affects = ApplicationResult.POST_ORDER

    def __init__(self, description):
        self.description = description
