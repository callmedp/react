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
    # common status 1 - 20
    (0, 'Default'),
    (1, 'Assigned'),
    (2, 'Resume Not Uploaded'),
    (3, 'Resume Uploded'),
    (4, 'Closed'),

    # flow1 and flow3 21 - 40
    (21, 'Upload Draft'),
    (22, 'Draft Uploaded'),
    (23, 'Pending Approval'),
    (24, 'Approved'),
    (25, 'Rejected By Admin'),
    (26, 'Rejected By Candidate'),

    # flow8 41 - 60


    # flow7 61 - 80
    (61, "Will start once resume is made"),
    (62, "Resume Boosted"),

)