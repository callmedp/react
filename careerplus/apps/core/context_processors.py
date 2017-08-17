from django.conf import settings


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
