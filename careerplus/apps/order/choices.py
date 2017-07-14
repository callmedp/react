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
    (10, 'On Hold by Vendor'),
    (11, 'Archived'),

    # flow1, flow3, and flow 5 status 21 - 40
    (21, 'Upload Draft'),
    (22, 'Draft Uploaded'),
    (23, 'Pending Approval'),
    (24, 'Approved'),
    (25, 'Rejected By Admin'),
    (26, 'Rejected By Candidate'),

    # for linkedin flow8 41 - 60
    (43, 'Linkedin Draft Create'),
    (44, 'Linkedin Draft Created'),
    (45, 'Linkedin Pending Approval'),
    (46, 'Linkedin Approved'),
    (47, 'Linkedin Rejected By Admin'),
    (48, 'Linkedi Rejected By Candidate'),

    # flow7 61 - 80
    (61, "Will start once resume is made"),
    (62, "Resume Boosted"),

)

COUNSELLING_FORM_STATUS = (
    (41, 'Counselling Form Not Submitted'),
    (42, 'Counselling Form Submitted'),
)
