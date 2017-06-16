from cart.mixins import CartMixin


def common_context_processor(request):
    context = {}
    cart_count = CartMixin().get_cart_count(request)
    context.update({
        "cart_count": cart_count,
    })
    return context
