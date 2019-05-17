# python imports
import logging
from collections import OrderedDict
from django.utils import timezone

# inter-app imports
from partner.models import (
    ParsedAssesmentData, Certificate, UserCertificate, Assesment,
    UserCertificateOperations, Vendor)
from django.db import IntegrityError
from emailers.tasks import send_email_task
from emailers.sms import SendSMS
from core.api_mixin import (
    ShineCandidateDetail, ShineToken, ShineCertificateUpdate
)
from emailers.utils import get_featured_profile_data_for_candidate
from core.api_mixin import FeatureProfileUpdate
from order.models import OrderItem
'''
Pull Type.

{
    "status": "success",
    "code": 200,
    "data": {
        "certificates": [
            {
                "certificateName": "AMCAT Certified in C",
                "skillValidated": "C",
                "licenseNumber": "10017408486910-6",
                "amcatID": 10017408486910,
                "certificationDate": "2013-04-04 00:00:00",
                "validTill": "2014-04-04"
            },
            {
                "certificateName": "AMCAT Certified in Ms office",
                "skillValidated": "Ms office",
                "licenseNumber": "10017408486910-1",
                "amcatID": 10017408486910,
                "certificationDate": "2013-04-04 00:00:00",
                "validTill": "2014-04-04"
            },
            {
                "certificateName": "AMCAT Certified in Communication",
                "skillValidated": "Communication",
                "licenseNumber": "103541972-2",
                "amcatID": 103541972,
                "certificationDate": "2007-11-13 00:00:00",
                "validTill": "2008-11-13"
            },
            {
                "certificateName": "AMCAT Certified in Leadership Skills",
                "skillValidated": "Leadership Skills",
                "licenseNumber": "10014234777181-14",
                "amcatID": 10014234777181,
                "certificationDate": "2012-07-25 00:00:00",
                "validTill": "2013-07-25"
            }
            ],
            "scores": [
            {
                "overallScore": "NA",
                "testAttemptDate": "2007-11-13",
                "amcatID": "103541972",
                "modules": {
                    "5": {
                        "modulenames": "Computer Programming",
                        "mscores": 295,
                        "maxScores": 900
                    },
                    "693": {
                        "modulenames": "Basic computer literacy",
                        "mscores": 435,
                        "maxScores": 900
                        },
                    "972": {
                        "modulenames": "Effective Communication",
                        "mscores": 495,
                        "maxScores": 900
                    },
                    "2760": {
                        "modulenames": "WriteX",
                        "mscores": 475,
                        "maxScores": 900
                    }
                }
            },
            {
                "overallScore": "NA",
                "testAttemptDate": "2013-09-28",
                "amcatID": "10018648902011",
                "modules": {
                    "1": {
                        "modulenames": "English",
                        "mscores": 450,
                        "maxScores": 900
                    },
                    "5": {
                        "modulenames": "Computer Programming",
                        "mscores": 535,
                        "maxScores": 900
                    }
                }
            }
        ]
    },
"message": null
}
'''

'''
(PUSH TYPE)
DEMO DATA (AMCAT):-

{

  "result": {

    "amcatID": "10011930591215",

    "assessmentName": 1556099337@myamcat.com,

    "candidateName": "Raj Singh",

    "candidateEmailID": "s@gmail.com",

    "status": "",

    "reportURL": [

      {

        "name": "Candidate Proficiency Report",

        "url": "https%3A%2F%2Fcorpmis.aspiringminds.in%2FgenerateReports.php%3Fdata%3DYvxRSzV7xzokU5g9NBTMkRGO7LzG8gxGPTZcGIlEcG7PdOl1HPcHaNo%252FvlsN77fnbvWaD5bUZa%252BOt22%252FBMhArHH42XG%252FozvQgNh3Zsw8wfyxk6KPy4lnri8dyKNClklf"

      }

    ],

    "scores": {

      "English Comprehension": "605",

      "Quantitative Ability (Advanced)": "735",

      "Basic IT Applications": "765",

      "Computer Programming": "0",

      "Logical Ability": "0",

      "Mechanical Engineering": "0",

      "Civil Engineering": "0",

      "C++ Programming": "0",

      "Core Java (Entry Level)": "0",

      "SQL": "0",

      "UNIX": "0"

    },

    "certificates": [

      {

        "certificateName": "AMCAT Certified in C",

        "licenseNumber": "333070-10011930591215-6",

        "amcatID": 10011930591215,

        "validTill": "2012-08-26"

      },

      {

        "certificateName": "AMCAT Certified in Basic Computer Knowledge",

        "licenseNumber": "333070-10011930591215-20",

        "amcatID": 10011930591215,

        "validTill": "2012-08-26"

      },

      {

        "certificateName": "AMCAT Certified in MS office",

        "licenseNumber": "333070-10011930591215-1",

        "amcatID": 10011930591215,

        "validTill": "2012-08-26"

      }

    ]

  }

}
'''


''' 1 ---> denotes string
    2 ---> denotes list
    3 ---> denotes dictionary
    4 ---> denotes dictionary with multiple values as key, value
    5 ---> denotes list of dictionary
'''

# PUSH TYPE
MAPPING_VALUES_TO_DATA_KEY_1 = {
    'amcat': {
        'assesment': {
            'candidate_email': '1|candidateEmailID',
            'assesment_name': '1|assessmentName',
        },
        'certificate': {
            'certificate': '6|certificates',
        },
        'user_certificate': {
            'candidate_name': '1|candidateName',
            'candidate_email': '1|candidateEmailID',
            'certificate_file_url': '3|certificates:1|url',
            'order_item_id': '1|shineLearningOrderID'
        },
        'score': {
            'score': '4|scores',
        },
        'report': {
            'report': '5|reportURL'
        }
    }
}

# PULL-TYPE
MAPPING_VALUES_TO_DATA_KEY_2 = {

    'amcat': {
        'certificate': {
            'certificate': '6|certificates',
        },
    }
}

MAPPING_VALUES_TO_DATA_KEY = {
    0: MAPPING_VALUES_TO_DATA_KEY_1,
    1: MAPPING_VALUES_TO_DATA_KEY_2
}

# Marks
MAPPING_SCORE_TYPE_VENDOR = {
    'amcat': 1,
}

# Max_Score
MAPPING_VENDOR_MAX_SCORE = {
    'amcat': 1000,
}


MULTIPLE_VALUES_1 = {
    'amcat': {
        'score': ['subject', 'score_obtained'],
        'report': ['name', 'url'],
        'certificate': {
            'name': 'certificateName',
            'vendor_certificate_id': 'licenseNumber'
        },
    }
}

MULTIPLE_VALUES_2 = {
    'amcat': {
        'certificate': {
            'name': 'certificateName',
            'skill': 'skillValidated',
            'vendor_certificate_id': 'amcatID',
            'active_from': 'certificationDate',
            'expiry': 'validTill',
            'licenseNumber': 'licenseNumber'
        }
    }
}

ADDITONAL_OPERATIONS_1 = {
    'amcat': []
}

ADDITONAL_OPERATIONS_2 = {
    'amcat': ['attach_score_to_certificates']
}

ADDITONAL_OPERATIONS_MAPPING = {
    0: ADDITONAL_OPERATIONS_1,
    1: ADDITONAL_OPERATIONS_2
}

MULTIPLE_VALUES_MAPPING = {
    0: MULTIPLE_VALUES_1,
    1: MULTIPLE_VALUES_2
}


class CertiticateParser:

    def __init__(self, parse_type=0):
        self.parse_type = parse_type
        self.MAPPING_VALUES_TO_DATA_KEY = MAPPING_VALUES_TO_DATA_KEY.get(parse_type)
        self.MULTIPLE_VALUES = MULTIPLE_VALUES_MAPPING.get(parse_type)
        self.ADDITONAL_OPERATIONS = ADDITONAL_OPERATIONS_MAPPING.get(parse_type)

    def get_value_from_dict_using_key(self, data, name_key):
        if isinstance(data, dict):
            all_keys = data.keys()
            if name_key not in all_keys:
                for key in all_keys:
                    if isinstance(data[key], dict):
                        return self.get_value_from_dict_using_key(data[key], name_key)
            else:
                return data[name_key]


    def get_score_type_choices_as_per_vendor(self, vendor):
        return MAPPING_SCORE_TYPE_VENDOR.get(vendor, 1)


    def get_max_score_as_per_vendor(self, vendor):
        return MAPPING_VENDOR_MAX_SCORE.get(vendor, 100)


    def get_key_for_field(self, vendor_type, key, field):
        return self.MAPPING_VALUES_TO_DATA_KEY[vendor_type][key][field]


    def get_plain_key_value_pair(self, data, actual_data_key):
        '''
        expecting data as == { actual_data_key :value1}
        after parsing returns 'value1'

        '''
        return self.get_value_from_dict_using_key(data, actual_data_key)


    def get_list_values_as_comma_seperated_string(self, data, actual_data_key):
        '''
        expecting data as == { actual_data_key :[val1, val2, val3]}

        after parsing returns 'val1, val2, val3'
        '''
        value = self.get_value_from_dict_using_key(data, actual_data_key)
        return ','.join(value)


    def get_value_of_key_of_certain_dictionary(self, data, actual_data_key, value=None):
        '''
        expecting data as == { temp_key :{actual_data_key: value1}}

        after parsing returns 'value1'
        '''
        temp_key = value.split(':')[-2].split('|')[1]
        new_data = self.get_value_from_dict_using_key(data, temp_key)
        actual_data_key = value.split(':')[-1].split('|')[1]
        value = self.get_value_from_dict_using_key(new_data, actual_data_key)
        return value


    def get_list_of_list_of_dictionary_with_key_value_pair(self, data, actual_data_key):
        '''
        expecting data as == { actual_data_key :{key1: value1, key2: value2}}

        after parsing returns [[key1, value1],[key2, value2]]
        '''
        data = self.get_value_from_dict_using_key(data, actual_data_key)
        return data.items()


    def get_list_of_list_of_list_of_dictionary(self, data, actual_data_key):
        '''
        expecting data as{actual_data_key :[{key1: value1, key2: value2}, {key3: value3, key4: value4}]}

        after parsing returns [[value1, value2],[value3, value4]]
        '''
        value = self.get_value_from_dict_using_key(data, actual_data_key)
        k = []
        for val in value:
            val = OrderedDict(sorted(val.items(), key=lambda t: t[0]))
            k.append(list(val.values()))
        return k

    def get_list_of_dictionary(self, data, actual_data_key):
        '''
        expecting data as{actual_data_key :[{key1: value1, key2: value2}, {key3: value3, key4: value4}]}

        after parsing returns [{key1: value1, key2: value2}, {key3: value3, key4: value4}]}
        '''
        value = self.get_value_from_dict_using_key(data, actual_data_key)
        return value


    def get_actual_value(self, data, value):
        temp = value.split(':')
        if len(temp) == 0:
            return None
        data_type = value[0]
        actual_data_key = value.split(':')[-1].split('|')[1]
        if data_type == '1':
            return self.get_plain_key_value_pair(data, actual_data_key)
        elif data_type == '2':
            return self.get_list_values_as_comma_seperated_string(data, actual_data_key)
        elif data_type == '3':
            return self.get_value_of_key_of_certain_dictionary(data, actual_data_key, value) 
        elif data_type == '4':
            return self.get_list_of_list_of_dictionary_with_key_value_pair(data, actual_data_key)
        elif data_type == '5':
            return self.get_list_of_list_of_list_of_dictionary(data, actual_data_key)
        elif data_type == '6':
            return self.get_list_of_dictionary(data, actual_data_key)


    def save_parsed_data(self, parse_data, vendor):
        vendor_key = vendor
        vendor_field = 'vendor_text'
        certificate = None
        user_certificate = None

        try:
            vendor = Vendor.objects.get(name=vendor_key)
            vendor_field = 'vendor_provider'
        except Vendor.DoesNotExist:
            pass

        report = []

        # Make report string from report model
        for rep in parse_data.reports:
            report.append(rep.name + ":" + rep.url)

        report = ','.join(report)

        assesmemnt_data = parse_data.assesment.__dict__
        assesmemnt_data = {key: val for key, val in assesmemnt_data.items() \
                           if key in dict(self.MAPPING_VALUES_TO_DATA_KEY[vendor_key]['assesment']).keys()}

        if vendor_field == 'vendor_text':
                assesmemnt_data['vendor_text'] = vendor
        assesment, created = Assesment.objects.get_or_create(
            **assesmemnt_data
        )
        setattr(assesment, vendor_field, vendor)

        # Save assesment data
        assesment.report = report
        setattr(assesment, vendor_field, vendor)
        assesment.save()
        # Handling for scores, create only if assesment is newly created
        if created:
            for scor in parse_data.scores:
                if assesment:
                    scor.assesment = assesment
                    scor.score_type = self.get_score_type_choices_as_per_vendor(vendor_key)
                    # if not present and not percent
                    if not getattr(scor, 'max_score', None) and scor.score_type != 3:
                        scor.max_score = self.get_max_score_as_per_vendor(vendor_key)
                    # if not present and score is percent
                    if not getattr(scor, 'max_score', None) and scor.score_type == 3:
                        scor.max_score = '100'
                scor.save()

        for certificate in parse_data.certificates:
            # manage certiticate data
            certificate_data = certificate.__dict__

            certificate_data = {key: val for key, val in certificate_data.items() \
                                if key in dict(self.MULTIPLE_VALUES[vendor_key]['certificate']).keys()}

            if vendor_field == 'vendor_text':
                certificate_data['vendor_text'] = vendor

            certificate, created = Certificate.objects.get_or_create(
                **certificate_data
            )
            setattr(certificate, vendor_field, vendor)

            try:
                certificate.save()
            except IntegrityError:
                pass

            candidate_email = parse_data.assesment.candidate_email

            # Fetch candidate id and store it in assesment and user certificate
            user_certificate = parse_data.user_certificate

            if candidate_email:
                candidate_id = ShineCandidateDetail().get_shine_id(email=candidate_email)

                if candidate_id:
                    user_certificate.candidate_id = candidate_id
                    assesment.candidate_id = candidate_id
                    assesment.save()

            # save user certificate data
            user_certificate_data = parse_data.user_certificate.__dict__
            user_certificate_data = {key: val for key, val in user_certificate_data.items() \
                                     if key in dict(self.MAPPING_VALUES_TO_DATA_KEY[vendor_key]['user_certificate']).keys()}
            user_certificate_data['certificate'] = certificate
            if assesment:
                user_certificate_data['assesment'] = assesment
            user_certificate, created = UserCertificate.objects.get_or_create(
                **user_certificate_data
            )
        return (certificate, user_certificate)



    def update_certificate_on_shine(self, user_certificate):
        headers = ShineToken().get_api_headers()
        shineid = ShineCandidateDetail().get_shine_id(
            email=user_certificate.candidate_email, headers=headers)
        if shineid:
            post_data = {
                'certification_name': user_certificate.certificate.name,
                'certification_year': user_certificate.year
            }
            flag, jsonrsp = ShineCertificateUpdate().update_shine_certificate_data(
                candidate_id=shineid, data=post_data, headers=headers
            )
            if flag:
                logging.getLogger('inf_log').error("Certificate %s for Candidate Id %s" % (str(user_certificate.certificate.name), str(user_certificate.candidate_id)))
                last_op_type = user_certificate.status
                user_certificate.status = 1
                user_certificate.save()
                UserCertificateOperations.objects.create(
                    user_certificate=user_certificate,
                    op_type=1,
                    last_op_type=last_op_type)
                return True
        return False

    def parse_data(self, data):
        try:
            vendor_key = data['vendor']
            parse_data = ParsedAssesmentData()
            all_keys_for_parsed_data = self.MAPPING_VALUES_TO_DATA_KEY[vendor_key].keys()

            for key in all_keys_for_parsed_data:
                fields = dict(self.MAPPING_VALUES_TO_DATA_KEY[vendor_key][key]).keys()

                for field in fields:
                    value = self.get_actual_value(data, self.get_key_for_field(vendor_key, key, field))
                    if field in self.MULTIPLE_VALUES[vendor_key].keys():
                        multiple_fields =self.MULTIPLE_VALUES[vendor_key][field]

                        for val in value:
                            data_instance = getattr(parse_data, key).__class__()
                            if isinstance(multiple_fields, list):
                                for index, field in enumerate(multiple_fields):
                                    setattr(data_instance, multiple_fields[index], val[index])
                            elif isinstance(multiple_fields, dict):
                                for k, value in multiple_fields.items():
                                    setattr(data_instance, k, val[value])
                            parse_data.__dict__[key + 's'].append(data_instance)
                    else:
                        setattr(getattr(parse_data, key), field, value)

            additional_operations = self.ADDITONAL_OPERATIONS[vendor_key]

            # additonal operation to be done on parsed data as per vendor type and parse type
            for operation in additional_operations:
                parse_data = getattr(self, operation)(parse_data, data)

            return parse_data
        except Exception as e:
            logging.getLogger('error_log').error("%s Exception occured for data:- %s - " % (str(e), str(data)))
            return None


    def attach_score_to_certificates(self, parsed_data, data):
        all_scores = self.get_list_of_dictionary(data, 'scores')
        for certificate in parsed_data.certificates:
            current_certificate_id = certificate.vendor_certificate_id
            for score in all_scores:
                if str(current_certificate_id) == str(score['amcatID']):
                    overallScore = score.get('overallScore', None)
                    if overallScore != 'NA':
                        setattr(certificate, 'overallScore', int(overallScore))
                    else:
                        setattr(certificate, 'overallScore', None)
                    break
                else:
                    setattr(certificate, 'overallScore', None)
        return parsed_data

    def update_order_and_badge_user(self, parsed_data, vendor):
        email = parsed_data.user_certificate.candidate_email
        orderitem_id = parsed_data.user_certificate.order_item_id
        oi = OrderItem.objects.filter(id=orderitem_id)
        if oi:
            candidate_id = oi.order.candidate_id
            data = get_featured_profile_data_for_candidate(
                candidate_id=candidate_id, curr_order_item=oi, feature=True)
            flag = FeatureProfileUpdate().update_feature_profile(
                candidate_id=candidate_id, data=data)
            if flag:
                logging.getLogger('info_log').info(
                    'Badging After parsing data is done for OrderItem  %s is %s' % (str(oi.id), str(data))
                )
                last_oi_status = oi.oi_status
                oi.oi_status = 4
                oi.closed_on = timezone.now()
                oi.last_oi_status = 6
                oi.save()
                oi.orderitemoperation_set.create(
                    oi_status=6,
                    last_oi_status=last_oi_status,
                    assigned_to=oi.assigned_to)
                oi.orderitemoperation_set.create(
                    oi_status=oi.oi_status,
                    last_oi_status=oi.last_oi_status,
                    assigned_to=oi.assigned_to)

                # Send mail and sms with subject line as Your Profile updated
                try:
                    mail_type = "BADGING_DONE_MAIL"

                    email_sets = list(
                        oi.emailorderitemoperation_set.all().values_list(
                            'email_oi_status', flat=True).distinct())
                    to_emails = [oi.order.get_email()]
                    data = {}
                    data.update({
                        "subject": 'Your Featured Profile Is Updated',
                        "username": oi.order.first_name,
                        "product_timeline": oi.product.get_duration_in_day(),
                    })

                    if 72 not in email_sets:
                        send_email_task.delay(
                            to_emails, mail_type, data,
                            status=72, oi=oi.pk)
                    SendSMS().send(sms_type=mail_type, data=data)
                    return True
                except Exception as e:
                        logging.getLogger('error_log').error('Bading After pasrsing data failed, Error: %s'.format(str(e)))
                        return False
