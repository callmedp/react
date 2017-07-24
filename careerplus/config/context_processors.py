from cart.mixins import CartMixin
from django.conf import settings

def common_context_processor(request):
    context = {}
    cart_count = CartMixin().get_cart_count(request)
    context.update({
        "cart_count": cart_count,
    	"PRODUCT_GROUP_LIST": settings.PRODUCT_GROUP_LIST,
    	"VENDOR_GROUP_LIST": settings.VENDOR_GROUP_LIST,
    	"OPERATION_GROUP_LIST": settings.OPERATION_GROUP_LIST,
    	"SEO_GROUP_LIST": settings.SEO_GROUP_LIST,
    	"WRITING_GROUP_LIST": settings.WRITING_GROUP_LIST
    })
    return context

