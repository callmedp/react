from partner.models import ParsedAssesmentData, Certificate, UserCertificate, Assesment
from core.api_mixin import ShineCandidateDetail
from collections import OrderedDict
from copy import deepcopy
'''
DEMO DATA :-

{
    "result": {
        "candidateName": "Mark Depp",
        "candidateEmailID": "user@mail.com",
        "amcatID": "12345678901234",
        "assessmentName": "Test name",
        "reportURL": [
            {
                "name": "Candidate Proficiency Report",
                "url":
                "https%3A%2F%2Fcorpmis.aspiringminds.in%2FgenerateReports.php%3Fdata%3DYvxRSzV7xzokU5g9NBTMkRGO"
            }
        ],
        "scores": {
            "Logical": "692",
            "english comprehension": "725",
            "mathematical": "815"
        },
        "scores": {
            ["Logical", "692"],
            ["english comprehension", "725"],
            ["mathematical", "815"]
        },
        "scores": {
            ["Logical", "692", "english comprehension", "725", "mathematical", "815"]
        },
        "scores": {
            ["Logical", "692", "english comprehension", "725", "mathematical", "815"]
        },
        "certificates": {
            "name": "AMCAT Certified Software Engineer - Product",
            "licenseNumber": "1302681-1",
            "url": "https://www.myamcat.com/linkedin-share?candidateID=1302681&jobsuitabilityID=1&src=2"
        },
        "certificates_name": "AMCAT Certified Software Engineer - Product",

        "certificate_url": "https://www.myamcat.com/linkedin-share?candidateID=1302681&jobsuitabilityID=1&src=2",

        "validated-skills": [
            "English comprehension",
            "Quantitative ability"
        ],
        "validated-skills": "English comprehension, Quantitative ability"
    }
}
'''


''' 1 ---> denotes string
    2 ---> denotes list
    3 ---> denotes dictionary
    4 ---> denotes dictionary with multiple values as key, value
    5 ---> denotes list of dictionary
'''
MAPPING_VALUES_TO_DATA_KEY = {
    'amcat': {
        'assesment': {
            'candidate_email': '1|candidateEmailID',
            'assesment_name': '1|assesment_name',
        },
        'certificate': {
            'name': '3|certificates:1|name',
            'skill': '2|validated-skills',
        },
        'user_certificate': {
            'candidate_name': '1|candidateName',
            'candidate_email': '1|candidateEmailID',
            'certificate_file_url': '3|certificates:1|url'
        },
        'score': {
            'score': '4|scores',
        },
        'report': {
            'report': '5|reportURL'
        }
    }
}

MULTIPLE_VALUES = {'score': ['subject', 'score_obtained'], 'report': ['name', 'url']}


def get_value_from_dict_using_key(data, name_key):
    if isinstance(data, dict):
        all_keys = data.keys()
        if name_key not in all_keys:
            for key in all_keys:
                if isinstance(data[key], dict):
                    return get_value_from_dict_using_key(data[key], name_key)
        else:
            return data[name_key]



def get_key_for_field(vendor_type, key, field):
    return MAPPING_VALUES_TO_DATA_KEY[vendor_type][key][field]


def get_plain_key_value_pair(data, actual_data_key):
    '''
    expecting data as == { actual_data_key :value1}
    after parsing returns 'value1'

    '''
    return get_value_from_dict_using_key(data, actual_data_key)


def get_list_values_as_comma_seperated_string(data, actual_data_key):
    '''
    expecting data as == { actual_data_key :[val1, val2, val3]}

    after parsing returns 'val1, val2, val3'
    '''
    value = get_value_from_dict_using_key(data, actual_data_key)
    return ','.join(value)


def get_value_of_key_of_certain_dictionary(data, actual_data_key, value=None):
    '''
    expecting data as == { temp_key :{actual_data_key: value1}}

    after parsing returns 'value1'
    '''
    temp_key = value.split(':')[-2].split('|')[1]
    new_data = get_value_from_dict_using_key(data, temp_key)
    actual_data_key = value.split(':')[-1].split('|')[1]
    value = get_value_from_dict_using_key(new_data, actual_data_key)
    return value


def get_list_of_list_of_dictionary_with_key_value_pair(data, actual_data_key):
    '''
    expecting data as == { actual_data_key :{key1: value1, key2: value2}}

    after parsing returns [[key1, value1],[key2, value2]]
    '''
    data = get_value_from_dict_using_key(data, actual_data_key)
    return data.items()


def get_list_of_list_of_list_of_dictionary(data, actual_data_key):
    '''
    expecting data as{actual_data_key :[{key1: value1, key2: value2}, {key3: value3, key4: value4}]}

    after parsing returns [[value1, value2],[value3, value4]]
    '''
    value = get_value_from_dict_using_key(data, actual_data_key)
    k = []
    for val in value:
        val = OrderedDict(sorted(val.items(), key=lambda t: t[0]))
        k.append(list(val.values()))
    return k


def get_actual_value(data, value):
    temp = value.split(':')
    if len(temp) == 0:
        return None
    data_type = value[0]
    actual_data_key = value.split(':')[-1].split('|')[1]
    if data_type == '1':
        return get_plain_key_value_pair(data, actual_data_key)
    elif data_type == '2':
        return get_list_values_as_comma_seperated_string(data, actual_data_key)
    elif data_type == '3':
        return get_value_of_key_of_certain_dictionary(data, actual_data_key, value) 
    elif data_type == '4':
        return get_list_of_list_of_dictionary_with_key_value_pair(data, actual_data_key)
    elif data_type == '5':
        return get_list_of_list_of_list_of_dictionary(data, actual_data_key)


def parse_data(data):
    vendor = data['vendor']
    vendor_field = 'vendor_text'
    from partner.models import Vendor
    try:
        vendor = Vendor.objects.get(name=vendor)
        vendor_field = 'vendor_provider'
    except Vendor.DoesNotExist:
        pass

    parse_data = ParsedAssesmentData()
    all_keys_for_parsed_data = MAPPING_VALUES_TO_DATA_KEY[vendor].keys()

    for key in all_keys_for_parsed_data:
        fields = dict(MAPPING_VALUES_TO_DATA_KEY[vendor][key]).keys()

        for field in fields:
            value = get_actual_value(data, get_key_for_field(vendor, key, field))

            if field in MULTIPLE_VALUES.keys():
                multiple_fields = MULTIPLE_VALUES[field]

                for val1, val2 in value:
                    data_instance = getattr(parse_data, key)
                    data_instance = data_instance()
                    setattr(data_instance, multiple_fields[0], val1)
                    setattr(data_instance, multiple_fields[1], val2)
                    parse_data.__dict__[key + 's'].append(data_instance)
            else:
                setattr(getattr(parse_data, key), field, value)

    # manage certiticate data
    certificate_data = parse_data.certificate.__dict__
    certificate_data = {key: val for key, val in certificate_data.items() \
                        if key in dict(MAPPING_VALUES_TO_DATA_KEY[vendor]['certificate']).keys()}

    certificate_data['vendor_text'] = vendor
    certificate, created = Certificate.objects.get_or_create(
        **certificate_data
    )
    setattr(certificate, vendor_field, vendor)
    certificate.save()

    candidate_email = parse_data.assesment.candidate_email
    report = []

    # Make report string from report model
    for rep in parse_data.reports:
        report.append(rep.name + ":" + rep.url)

    report = ','.join(report)

    # fetch candidate id and store it in assesment and user certificate
    user_certificate = parse_data.user_certificate
    assesment = parse_data.assesment

    if candidate_email:
        candidate_id = ShineCandidateDetail().get_shine_id(email=candidate_email)

        if candidate_id:
            user_certificate.candidate_id = candidate_id
            assesment.candidate_id = candidate_id

    # save user certificate data
    user_certificate_data = parse_data.user_certificate.__dict__
    user_certificate_data = {key: val for key, val in user_certificate_data.items() \
                             if key in dict(MAPPING_VALUES_TO_DATA_KEY[vendor]['user_certificate']).keys()}
    user_certificate_data['certificate'] = certificate
    user_certificate, created = UserCertificate.objects.get_or_create(
        **user_certificate_data
    )

    assesmemnt_data = parse_data.assesment.__dict__
    assesmemnt_data = {key: val for key, val in assesmemnt_data.items() \
                       if key in dict(MAPPING_VALUES_TO_DATA_KEY[vendor]['assesment']).keys()}

    assesment, created = Assesment.objects.get_or_create(
        **assesmemnt_data
    )

    # Save assesment data
    assesment.report = report
    if certificate:
        assesment.certificate = certificate
    setattr(certificate, vendor_field, vendor)
    assesment.save()

    # Handling for scores, create only if assesment is newly created
    if created:
        for scor in parse_data.scores:
            if assesment:
                scor.assesment = assesment
            scor.save()
