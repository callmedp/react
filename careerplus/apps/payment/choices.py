STATUS_CHOICES = (
    (0, "Unpaid"),
    (1, "Paid"),
    (2, "Failure"),
    (3, "Aborted"),
    (4, "Invalid"),
    (5, "Cancel"),
    (6, "Refunded"),
)

SITE_CHOICES = (
    (0, "Shinelearning"),
    (1, "Cpcrm"),
)


PAYMENT_MODE = (
    (0, 'Not Paid'),
    (1, 'Cash'),
    (2, 'Citrus Pay'),
    (3, 'EMI'),
    (4, 'Cheque or Draft'),
    (5, 'CC-Avenue'),
    (6, 'Mobikwik'),
    (7, 'CC-Avenue-International'),
    (8, 'Debit Card'),
    (9, 'Credit Card'),
    (10, 'Net Banking'),
    (11, 'Paid Free'),
    (12, "EPAYLATER"),
    (13, "PAYU")
)
