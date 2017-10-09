from django.conf import settings
from cart.mixins import CartMixin
from cart.models import Subscription


def js_settings(request):
    js_vars = {}
    js_vars.update(
        {
            'MAIN_DOMAIN_PREFIX': settings.MAIN_DOMAIN_PREFIX,
            'MOBILE_LOGIN_URL': settings.MOBILE_LOGIN_URL,
            'CURRENT_FLAVOUR': request.flavour,
            'SHINE_SITE': settings.SHINE_SITE,
        }
    )
    vars_list = ["window['%s']=\"%s\"" % (variable, value) for variable, value in js_vars.items()]
    vars_text = ";".join(vars_list)
    if vars_text:
        vars_text = '<script type=\"text/javascript\">%s;</script>' % vars_text
    return {
        'JS_SETTINGS': vars_text
    }


def common_context_processor(request):
    context = {}
    cart_count = CartMixin().get_cart_count(request)
    try:
        candidate_id = request.session.get('candidate_id', None)
        roundone_user = Subscription.objects.filter(candidateid=candidate_id).exists()
    except:
        roundone_user = None
    context.update({
        "SITE_DOMAIN": settings.SITE_DOMAIN,
        "SITE_PROTOCOL": settings.SITE_PROTOCOL,
        "cart_count": cart_count,
        "PRODUCT_GROUP_LIST": settings.PRODUCT_GROUP_LIST,
        "VENDOR_GROUP_LIST": settings.VENDOR_GROUP_LIST,
        "OPERATION_GROUP_LIST": settings.OPERATION_GROUP_LIST,
        "SEO_GROUP_LIST": settings.SEO_GROUP_LIST,
        "WRITING_GROUP_LIST": settings.WRITING_GROUP_LIST,
        "REFUND_GROUP_LIST": settings.REFUND_GROUP_LIST,
        "OPS_GROUP_LIST": settings.OPS_GROUP_LIST,
        "OPS_HEAD_GROUP_LIST": settings.OPS_HEAD_GROUP_LIST,
        "BUSINESS_HEAD_GROUP_LIST": settings.BUSINESS_HEAD_GROUP_LIST,
        "DEPARTMENT_HEAD_GROUP_LIST": settings.DEPARTMENT_HEAD_GROUP_LIST,
        "FINANCE_GROUP_LIST": settings.FINANCE_GROUP_LIST,
        "roundone_user": roundone_user,
    })
    return context
