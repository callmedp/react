from decimal import Decimal
from typing import Tuple

FACULTY_DEFAULT = 0
FACULTY_TEACHER = 1
FACULTY_PRINCIPAL = 2

FACULTY_CHOICES = (
    (FACULTY_DEFAULT, '--Select Role--'),
    (FACULTY_TEACHER, 'Teacher'),
    (FACULTY_PRINCIPAL, 'Principal'),
)

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
    (4, 'Other Services'),
    (5, 'Assesment/Certification'))

SECTION_TYPE_CHOICES = (
    (1, 'features'),
    (2, 'why-choose-us'),
    (3, 'how-it-works'),
    (4, 'product-banner-widget')
)

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
    (14, 'University Courses'),
    (15, 'Resume Booster International'),
    (16, 'Assessment and Certifications'),
    (17, 'Resume Builder'),
    (18, 'Shine Premium'),
)

SUB_FLOWS = {
    5: (
        (501, "Featured Profile"),
        (502, "Jobs on the Move"),
        (503, "Priority Applicant")
    ),
    16: (
        (1601, "Free Test"),
        (1602, "Paid Test")
    ),
    2: (
        (200, "Default"),
        (201, "Certificate Product"),
    ),
    1: (
        (100, "Default"),
        (101, "Expert Assistance")
    ),
    17: (
        (1700, "Default"),
        (1701, "Subscription")
    ),
    18: (
        (1800, 'One Month'),
        (1801, 'Two Month'),
        (1802, 'Six Month')
    )
}

SUB_FLOW_CHOICES = ()

for key, value in list(SUB_FLOWS.items()):
    k = [(item[0], item[1]) for item in value]
    SUB_FLOW_CHOICES += tuple(k)

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

#


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
    return "D0"
#


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
    'FD': 'featured_duration',
    'SD': 'service_doc',
    'SI': 'service_im',
    'CP': 'can_be_paused',
    'LC': 'links_count',
    'SUB': 'subscription_days'
}

A_ATTR_DICT = {
    'AD': 'assesment_duration'
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


BENEFITS = {
    '1': ['Free featured profile', 'exe-icon-feat-profile', 'FREE featured profile worth Rs. 1440 for 1 month on Shine.com'],
    '2': ['Shine credits', 'exe-icon-shine-credit', '10% Shine credits redeemable on next purchase*'],
    '3': ['Global Education Providers', 'exe-icon-education-provider', 'Choose from a list of global providers as per your requirement.'],
    '4': ['Appear for exam – Get Certified', 'exe-icon-get-certified'],
    '5': ['Fill Online Application Form', 'exe-icon-online-application'],
    '6': ['Get Access to online learning management system', 'exe-icon-access-online'],
    # '7': ['Check eligibility before filling online application','exe-icon-check-eligible'],
    # '8': ['Complete online application form', 'exe-icon-complete-application'],
    # '9': ['Make Course Fee Payment', 'exe-icon-fee-payment'],
    # '10': ['Start your course', 'exe-icon-start-course']
}

APPLICATION_PROCESS = {
    '1': ['Place Order', 'exe-icon-place-order'],
    '2': ['Receive online access/study material from course material', 'exe-icon-study-material'],
    '3': ['Access the material and start learning', 'exe-icon-start-learning'],
    '4': ['Appear for exam – Get Certified', 'exe-icon-get-certified'],
    '5': ['Fill Online Application Form', 'exe-icon-online-application'],
    '6': ['Get Access to online learning management system', 'exe-icon-access-online'],
    # '7': ['Check eligibility before filling online application','exe-icon-check-eligible'],
    # '8': ['Complete online application form', 'exe-icon-complete-application'],
    # '9': ['Make Course Fee Payment', 'exe-icon-fee-payment'],
    # '10': ['Start your course', 'exe-icon-start-course']

}

APPLICATION_PROCESS_CHOICES = [(int(key), val[1], val[0])
                               for key, val in list(APPLICATION_PROCESS.items())]

BENEFITS_CHOICES = [(int(key), val[1], val[0])
                    for key, val in list(BENEFITS.items())]

CITY_CHOICES = (
    (0, 'Delhi'),
    (1, 'Mumbai'),
    (2, 'Pune'),
    (3, 'Hyderabad'),
    (4, 'Kolkata'),
    (5, 'Noida'),
    (6, 'Gurgaon'),
    (7, 'Chandigarh'),
    (8, 'Nagpur'),
    (9, 'Jaipur'),
    (10, 'Bangalore'),
    (11, 'Gurugram')
)

SHINE_FLOW_ACTION = (
    (1, 'Highlight'),
    (2, 'Booster')
)

LINK_STATUS_CHOICES = (
    (0, 'Save'),
    (2, 'Sent'),
)

NEO_LEVEL_OG_IMAGES = {
    'Starter': 'shinelearn/images/starter.jpg',
    'A1': 'shinelearn/images/A1.jpg',
    'A2': 'shinelearn/images/A2.jpg',
    'B1': 'shinelearn/images/B1.jpg',
    'B2': 'shinelearn/images/B2.jpg',
    'C1': 'shinelearn/images/C1.jpg',
    'C2': 'shinelearn/images/C2.jpg'

}

DAYS_CHOICES = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)

DAYS_CHOICES_DICT = dict(DAYS_CHOICES)

MANUAL_CHANGES_CHOICES = (
    (1, 'Update Pending Links Count'),
)

EDUCATION_CHOICES = (
    (0, "NA"),
    (101, "10+2 or Below"),
    (102, "B.A"),
    (103, "B.Arch"),
    (104, "B.B.A / B.M.S"),
    (105, "B.C.A"),
    (106, "B.Com"),
    (107, "B.Ed"),
    (108, "B.Pharma"),
    (109, "B.Sc"),
    (110, "B.Tech/B.E"),
    (111, "BDS"),
    (112, "BHM"),
    (113, "BVSC"),
    (114, "C.A"),
    (115, "C.F.A"),
    (116, "C.S"),
    (117, "Diploma"),
    (118, "ICWA / CMA"),
    (119, "Integrated PG"),
    (120, "LL.M"),
    (121, "LLB"),
    (122, "M.A"),
    (123, "M.C.A"),
    (124, "M.Com"),
    (125, "M.Ed"),
    (126, "M.Pharma"),
    (127, "M.Sc"),
    (128, "M.Tech"),
    (129, "MBA/PGDM"),
    (130, "MBBS"),
    (131, "MD/MS"),
    (132, "MDS"),
    (133, "MMH"),
    (134, "MPHIL"),
    (135, "MVSC"),
    (136, "Other"),
    (137, "PG Diploma"),
    (138, "Ph.D/Doctorate"),
    (139, "BHMS"),
    (140, "BAMS"),
    (141, "B.P.Ed"),
    (142, "BPT"),
    (143, "BUMS"),
    (144, "CA (Intermediate)"),
    (146, "M.P.Ed"),
)

SUB_HEADING_CHOICES = (
    (0, 'None'),
    (1, 'objective'),
    (2, 'who-should-learn'),
    (3, 'faq'),
    (4, 'features')
)

SUB_HEADING_CHOICE_ATTR_MAPPING_DESKTOP = (
    (1, 'class="objective__list" id="expand-list"'),
    (2, 'class="who-should-learn__list d-flex flex-wrap"'),
)

SUB_HEADING_CHOICE_ATTR_MAPPING_MOBILE = (
    (1, 'class="objective__list collapse" id="expand-list" aria-expanded="false"'),
    (2, 'class="bullet-custom tick"'),
)

# also added in choices.py of search to be used in filter tag
PRODUCT_TAG_CHOICES = (
    (0, 'None'),
    (1, 'Bestseller'),
    (2, 'Newly Added')

)
