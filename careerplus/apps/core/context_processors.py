import datetime

from django.conf import settings

from cart.mixins import CartMixin
from cart.models import Subscription
import logging


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
    except Exception as e:
        logging.getLogger('error_log').error('unable to get candidate id' % str(e))
        roundone_user = None

    console_user = request.user
    writer_invoice = False
    try:
        if console_user and hasattr(console_user, 'userprofile') and \
                console_user.userprofile and console_user.userprofile.invoice_date:
            today_date = datetime.datetime.now().date()
            invoice_date = today_date.replace(day=1)
            invoice_date = invoice_date - datetime.timedelta(days=1)
            userprofile = console_user.userprofile
            if userprofile.user_invoice and userprofile.invoice_date.month==invoice_date.month and userprofile.invoice_date.year==invoice_date.year:
                writer_invoice = True

    except Exception as e:
        logging.getLogger('error_log').error('writer invoice is not reachable %s'%str(e))
        pass

    context.update({
        "SITE_DOMAIN": settings.SITE_DOMAIN,
        "MOBILE_SITE_DOMAIN": settings.MOBILE_SITE_DOMAIN,
        "SITE_PROTOCOL": settings.SITE_PROTOCOL,
        "cart_count": cart_count,
        "PRODUCT_GROUP_LIST": settings.PRODUCT_GROUP_LIST,
        "VENDOR_GROUP_LIST": settings.VENDOR_GROUP_LIST,
        "OPERATION_GROUP_LIST": settings.OPERATION_GROUP_LIST,
        "SEO_GROUP_LIST": settings.SEO_GROUP_LIST,
        "BLOGGER_GROUP_LIST": settings.BLOGGER_GROUP_LIST,
        "LEARNING_BLOGGER": settings.LEARNING_BLOGGER,
        "TALENT_BLOGGER": settings.TALENT_BLOGGER,
        "WRITING_GROUP_LIST": settings.WRITING_GROUP_LIST,
        "REFUND_GROUP_LIST": settings.REFUND_GROUP_LIST,
        "OPS_GROUP_LIST": settings.OPS_GROUP_LIST,
        "OPS_HEAD_GROUP_LIST": settings.OPS_HEAD_GROUP_LIST,
        "BUSINESS_HEAD_GROUP_LIST": settings.BUSINESS_HEAD_GROUP_LIST,
        "DEPARTMENT_HEAD_GROUP_LIST": settings.DEPARTMENT_HEAD_GROUP_LIST,
        "FINANCE_GROUP_LIST": settings.FINANCE_GROUP_LIST,
        "USER_QUERY_GROUP_LIST": settings.USER_QUERY_GROUP_LIST,
        "CMS_GROUP_LIST": settings.CMS_GROUP_LIST,
        "SKILL_GROUP_LIST": settings.SKILL_GROUP_LIST,
        "COURSE_GROUP_LIST": settings.COURSE_GROUP_LIST,
        "SERVICE_GROUP_LIST": settings.SERVICE_GROUP_LIST,
        "MARKETING_GROUP_LIST": settings.MARKETING_GROUP_LIST,
        "roundone_user": roundone_user,
        "IS_LIVE": settings.IS_LIVE,
        "writer_invoice": writer_invoice,
        "WELCOMECALL_GROUP_LIST": settings.WELCOMECALL_GROUP_LIST,
        "ggn_contact_full": settings.GGN_CONTACT_FULL,
        "ggn_contact": settings.GGN_CONTACT,
    })
    return context
