import string
COUPON_TYPES = (
    ('monetary', 'Money based coupon'),
    ('percentage', 'Percentage discount'),
    ('virtual_currency', 'Virtual currency'),
)
CODE_LENGTH = 12
CODE_CHARS = string.ascii_letters + string.digits
SEGMENTED_CODES = True
SEGMENT_LENGTH = 4
SEGMENT_SEPARATOR = "-"
