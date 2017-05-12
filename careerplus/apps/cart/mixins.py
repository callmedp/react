from .models import Cart, LineItem


class CartMixin(object):
    def mergeCart(self, fromcart, tocart):
        from_items = fromcart.lineitems.all().select_related('product')
        to_items = tocart.lineitems.all().values_list('product__pk', flat=True)
        for item in from_items:
            if item.product.pk not in to_items:
                LineItem.objects.create(cart=tocart, product=item.product)
            item.delete()
        fromcart.status = 1
        fromcart.save()

    def updateCart(self, cart_obj, product):
    	flag = 0  # already exist in cart
    	cartitems = cart_obj.lineitems.all().values_list('product', flat=True)
    	if product.pk not in cartitems:
    		LineItem.objects.create(cart=cart_obj, product=product)
    		flag = 1   # added to cart
    	return flag

    def getCartObject(self, request):
        candidate_id = request.session.get('candidate_id')
        sessionid = request.COOKIES.get('sessionid')
        cart_users = Cart.objects.filter(owner_id=candidate_id, status=2)
        cart_sessions = Cart.objects.filter(session_id=sessionid, status=0)
        cart_user, cart_session = None, None
        if cart_users:
            cart_user = cart_users[0]
        if cart_sessions:
            cart_session = cart_sessions[0]

        if cart_user and cart_session and (cart_user != cart_session):
            self.mergeCart(cart_session, cart_user)

        if cart_user:
            return cart_user
        elif cart_session:
            cart_session.owner_id = candidate_id
            cart_session.save()
            return cart_user
