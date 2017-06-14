STATUS_CHOICES = (
    (0, "Unpaid"),
    (1, "Paid"),
    (2, "InProcess"),
    (3, "Closed"),
    (4, "Archive"),
)

SITE_CHOICES = (
    (0, "Shinelearning"),
    (1, "Cpcrm"),
)


PAYMENT_MODE = (
    (0, 'Not Paid'),
    (1, 'Cash'),
    # (2, 'Citrus Pay'),
    (3, 'EMI'),
    (4, 'Cheque or Draft'),
    (5, 'CC-Avenue'),
    (6, 'Mobikwik'),
    (7, 'CC-Avenue-International'),
    (8, 'Debit Card'),
    (9, 'Credit Card'),
    (10, 'Net Banking'),
    (11, 'Emi'),)

OI_OPS_STATUS = (
    # for flow 1 - 29
    (0, 'Default'),
    (1, 'Welcome Call Pending'),
    (2, 'Welcome Call Done'),
    (3, 'Assigned'),
    (4, 'Resume Uploaded Pending'),
    (5, 'Approval Required'),
    (6, 'Rejected By Admin'),
    (7, 'Rejected By Candidate'),
    (8, 'Closed'),

)