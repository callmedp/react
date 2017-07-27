import string
COUPON_TYPES = (
    ('money', 'Money based coupon'),
    ('percentage', 'Percentage discount'),
)
CODE_LENGTH = 8
CODE_CHARS = string.ascii_letters + string.digits
SEGMENTED_CODES = True
SEGMENT_LENGTH = 4
SEGMENT_SEPARATOR = "-"
