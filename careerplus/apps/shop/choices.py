from django.utils.translation import ugettext_lazy as _

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
    (1, 'Flow 1'),
    (2, 'Flow 2'),
    (3, 'Flow 3'),
    (4, 'Flow 4'),
    (5, 'Flow 5'),
    (6, 'Flow 6'),
    (7, 'Flow 7'),
    (8, 'Flow 8'),
    (9, 'Flow 9'),
    (10, 'Flow 10'),
    (11, 'Flow 11'),
    (12, 'Flow 12'),
    (13, 'Flow 13'),)

EXP_CHOICES = (
    (0, 'Default'),
    (1, '0-1 years'),
    (2, '1-4 years'),
    (3, '4-8 years'),
    (4, '8-15 years'),)


COURSE_TYPE_CHOICES = (
    (0, 'Default'),
    (1, 'Basic'),
    (2, 'Intermediate'),
    (3, 'Expert'),)


MODE_CHOICES = (
    (0, 'Default'),
    (1, 'Online'),
    (2, 'Classroom'),
    (3, 'Online + Classroom'),)


BG_COLOR = { 0: "#c8b98d", 1: "#cfbabd", 2: "#75dac2", 3: "#d2db86",
    4: "#a69cba", 5: "#8cb3f6", 6: "#9ac7e5", 7: "#ad9c7f",
    8: "#80d7ff", 9: "#a48e96", 10: "#b4e4fc", 11: "#d7ccc8",
    12: "#a3e77d", 13: "#ebdcc9", 14: "#9fdbd6", 15: "#a19f9c",
    16: "#deae9e", 17: "#73a4d4", 18: "#cba5bf", 19: "#9099c6",
    20: "#d9bee7", 21: "#cddb3a", 22: "#81c783", 23: "#afbec6",
    24: "#cdac98", 25: "#c5cbe9", 26: "#d5d5d5", 27: "#e39b71"
}
BG_CHOICES = tuple(BG_COLOR.items())
