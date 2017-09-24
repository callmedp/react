from geolocation.models import Country


def get_country_obj(country_code2):
    try:
        country_objs = Country.objects.filter(code2=country_code2)
        country_obj = country_objs[0]
    except:
        country_obj = Country.objects.get(phone='91')
    return country_obj


def set_session_country(country_obj, request):
    session_country = request.session.get('country_code2', None)
    if session_country and country_obj.code2 == session_country:
        pass
    else:
        request.session['country_code2'] = country_obj.code2
        
