from rest_framework.response import Response
import datetime
from homepage.models import HomePageOffer
import pytz
from django.utils import timezone


def APIResponse(data=None, message=None, status=None, error=False):
    resp_json = {
        'message': message,
        'data': data,
        'status': status,
        'error': error
    }
    return Response(resp_json, status=status)

def get_home_offer_values():
    active_offer = HomePageOffer().get_active_offer()
    sticky_text = banner_text = offer_value = end_date = desktop_image = mobile_image = ""
    show = False
    fmt = "%d %b, %Y %H:%M:%S"
    if active_offer:
        end_local = active_offer.end_time
        start_local= active_offer.start_time
        utc_end = end_local.replace(tzinfo=pytz.UTC)
        end_date = utc_end.astimezone(timezone.get_current_timezone()).strftime(fmt)

        sticky_text = active_offer.sticky_text
        banner_text = active_offer.banner_text
        offer_value = active_offer.offer_value
        desktop_image = active_offer.desktop_image
        mobile_image = active_offer.mobile_image

        if (start_local.strftime(fmt) <= datetime.datetime.now(datetime.timezone.utc).strftime(fmt)):
            show = True
        else:
            show = False
    return end_date, sticky_text, banner_text, offer_value, desktop_image, mobile_image, show