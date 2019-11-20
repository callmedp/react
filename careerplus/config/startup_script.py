#python imports

#django imports

#local imports

#inter app imports

#third party imports

def apply_patch():
    from .package_override.celery.patch import patch_create_request_class,patch_default
    from .package_override.rest_framework.patch import patch_drf_paginator

    patch_create_request_class()
    patch_default()
    patch_drf_paginator()
