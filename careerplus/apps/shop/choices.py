from decimal import Decimal

RELATION_CHOICES = (
    (0, 'Default'),
    (1, 'UpSell'),
    (2, 'Recommendation'),
    (3, 'CrossSell'),)

SERVICE_CHOICES = (
    (0, 'Default'),
    (1, 'Writing Services'),
    (2, 'Job Assistance Services'),
    (3, 'Courses'),
    (4, 'Other Services'),)

CATEGORY_CHOICES = (
    (0, 'Default'),
    (1, 'Level 1'),
    (2, 'Level 2'),
    (3, 'Level 3'),
    (4, 'Level 4'),)

PRODUCT_VENDOR_CHOICES = (
    (0, 'Standalone/Simple'),
    (1, 'Variation-Parent'),)


PRODUCT_CHOICES = PRODUCT_VENDOR_CHOICES + ((2, 'Variation-Child'),
    (3, 'Combo'),
    (4, 'No-Direct-Sell/Virtual'),
    (5, 'Downloadable'),)

FLOW_CHOICES = (
    (0, 'Default'),
    (1, 'Resume Writing India'),  # flow1
    (2, 'Courses'),  # flow2
    (3, 'Resume Critique'),  # flow3
    (4, 'International Profile Update'),  # flow4
    (5, 'Featured Profile'),  # flow5
    (6, 'IDfy Assessment'),  # flow6
    (7, 'Resume Booster'),  # flow7
    (8, 'Linkedin'),  # flow8
    (9, 'Round One'),  # flow9
    (10, 'StudyMate'),  # flow 10
    (11, 'TSSC'),  # flow 11
    (12, 'Country Specific Resume'),  # flow 12
    (13, 'Executive Bio,Portfolio,Visual Resume,Cover Letter,Second Regular Resume'),  # flow 13
)

BG_COLOR = {0: "#c8b98d", 1: "#cfbabd", 2: "#75dac2", 3: "#d2db86",
    4: "#a69cba", 5: "#8cb3f6", 6: "#9ac7e5", 7: "#ad9c7f",
    8: "#80d7ff", 9: "#a48e96", 10: "#b4e4fc", 11: "#d7ccc8",
    12: "#a3e77d", 13: "#ebdcc9", 14: "#9fdbd6", 15: "#a19f9c",
    16: "#deae9e", 17: "#73a4d4", 18: "#cba5bf", 19: "#9099c6",
    20: "#d9bee7", 21: "#cddb3a", 22: "#81c783", 23: "#afbec6",
    24: "#cdac98", 25: "#c5cbe9", 26: "#d5d5d5", 27: "#e39b71"
}
BG_CHOICES = tuple(BG_COLOR.items())


DURATION_DICT = {
    'D0': '0-1 month',
    'D1': '1-3 months',
    'D2': '3-6 months',
    'D3': '9 months',
    'D4': '9-12 months',
    'D5': '1-2 years',
    'D6': '2-3 years',
    'D7': '3+ years',
}


def convert_to_month(days=0):
    if days:
        months = int(days)//30
        if 0 <= months <= 1:
            return 'D0'
        elif 1 < months <= 3:
            return 'D1'
        elif 3 < months <= 6:
            return 'D2'
        elif 6 < months <= 9:
            return 'D3'
        elif 9 < months <= 12:
            return 'D4'
        elif 12 < months <= 24:
            return 'D5'
        elif 24 < months <= 36:
            return 'D6'
        elif 36 < months:
            return 'D7'
    return 'D0'


C_ATTR_DICT = {
    'SM': 'study_mode',
    'DD': 'duration_day',
    'CERT': 'certification',
    'CL': 'course_level',
    'CT': 'course_type',
    'CD': 'course_doc',
    'CI': 'course_im',
}

R_ATTR_DICT = {
    'EXP': 'experience_writing',
}

S_ATTR_DICT = {
    'EXP': 'experience_service',
    'FD': 'feature_duration',
    'SD': 'service_doc',
    'SI': 'service_im',
}

##DO NOT CHANGE#
STUDY_MODE = dict((
    ('OL', 'Online'),
    ('OF', 'Offline'),
    ('IL', 'Instructor Led'),
    ('BL', 'Blended'),
    ('CA', 'Classroom'),
    ('CF', 'Certifications'),
    ('DL', 'Distance Learning'),
))

EXP_DICT = dict((
    ('FR', '0-1 years'),
    ('FP', '1-4 years'),
    ('SP', '4-8 years'),
    ('EP', '8-15 years'),
    ('DP', '15+ years')))

COURSE_TYPE_DICT = dict((
    ('BS', 'Basic'),
    ('BD', 'Basic + More Deliverable'),))


def convert_inr(price=Decimal(0)):
    if price:
        if Decimal(0) <= price <= Decimal(10000):
            return '1'
        elif Decimal(10000) < price <= Decimal(20000):
            return '2'
        elif Decimal(20000) < price <= Decimal(30000):
            return '3'
        elif Decimal(30000) < price <= Decimal(40000):
            return '4'
        elif Decimal(40000) < price:
            return '5'
    return '0'


def convert_usd(price=Decimal(0)):
    if price:
        if Decimal(0) <= price <= Decimal(20):
            return '1'
        elif Decimal(20) < price <= Decimal(100):
            return '2'
        elif Decimal(100) < price <= Decimal(200):
            return '3'
        elif Decimal(200) < price <= Decimal(500):
            return '4'
        elif Decimal(500) < price:
            return '5'
    return '0'


def convert_aed(price=Decimal(0)):
    if price:
        if Decimal(0) <= price <= Decimal(50):
            return '1'
        elif Decimal(50) < price <= Decimal(100):
            return '2'
        elif Decimal(100) < price <= Decimal(200):
            return '3'
        elif Decimal(200) < price <= Decimal(500):
            return '4'
        elif Decimal(500) < price:
            return '5'
    return '0'


def convert_gbp(price=Decimal(0)):
    if price:
        if Decimal(0) <= price <= Decimal(15):
            return '1'
        elif Decimal(15) < price <= Decimal(60):
            return '2'
        elif Decimal(60) < price <= Decimal(120):
            return '3'
        elif Decimal(120) < price <= Decimal(360):
            return '4'
        elif Decimal(360) < price:
            return '5'
    return '0'
