import string
COUPON_TYPES = (
    ('flat', 'Flat Discount'),
    ('percent', 'Percentage discount'),
)
CODE_LENGTH = 8
CODE_CHARS = string.ascii_letters + string.digits
SEGMENTED_CODES = True
SEGMENT_LENGTH = 4
SEGMENT_SEPARATOR = "-"

SITE_CHOICES = (
	(0, 'ALL SITE'),
	(1, 'Learning'),
	(2, 'CRM'),
	(3,'Resume Shine')
)


COUPON_SCOPE_CHOICES = (
	(0, "ALL"),
	(1, "PRODUCT"),
	(2, "SOURCE"),
)