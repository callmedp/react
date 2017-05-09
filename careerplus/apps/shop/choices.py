from django.utils.translation import ugettext_lazy as _

RELATION_CHOICES = (
    (0, 'Default'),
    (1, 'UpSell'),
    (2, 'Recommendation'),
    (3, 'CrossSell'),)

ATTRIBUTE_CHOICES = (
    (0, _("Text")),
    (1, _("Integer")),
    (2, _("True / False")),
    (3, _("Float")),
    (4, _("Rich Text")),
    (5, _("Date")),
    (6, _("Option")),
    (7, _("Entity")),
    (8, _("File")),
    (9, _("Image")),)

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

PRODUCT_CHOICES = (
    (0, 'Simple'),
    (1, 'Configurable'),
    (2, 'Combo'),
    (3, 'Virtual/Services'),
    (4, 'Bundle'),
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
    (12, 'Flow 12'),)

EXP_CHOICES = (
    (0, 'Default'),
    (1, 'Exp 1-4 Yrs'),
    (2, 'Exp 1-4 Yrs'),
    (3, 'Flow 3'),
    (4, 'Flow 4'),
    (5, 'Flow 5'),
    (6, 'Flow 6'),
    (7, 'Flow 7'),
    (8, 'Flow 8'),
    (9, 'Flow 9'),
    (10, 'Flow 10'),
    (11, 'Flow 11'),
    (12, 'Flow 12'),)


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
