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
    (1, 'Assigned'),
    (2, 'Resume Not Uploaded'),
    (3, 'Upload Draft'),
    (4, 'Draft Uploaded'),
    (5, 'Pending Approval'),
    (6, 'Approved'),
    (7, 'Rejected By Admin'),
    (8, 'Rejected By Candidate'),
    (9, 'Closed'),
    (10, 'Resume Uploded'),

)