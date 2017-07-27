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
    (2, 'Resume upload is pending'),
    (3, 'Resume Uploded'),
    (4, 'Closed'),
    (5, 'Service is under progress'),
    (6, 'Services has been processed'),
    (10, 'On Hold by Vendor'),
    (11, 'Archived'),
    (12, 'Unhold by Vendor'),

    # flow1, flow3, flow12, flow13, and flow 5 status 21 - 40
    (21, 'Upload Draft'),
    (22, 'Draft Uploaded'),
    (23, 'Pending Approval'),
    (24, 'Approved'),
    (25, 'Rejected By Admin'),
    (26, 'Rejected By Candidate'),
    (27, 'Service has been processed and Document is finalized'),

    # for linkedin flow8 41 - 60
    (43, 'Linkedin Draft Create'),
    (44, 'Linkedin Draft Created'),
    (45, 'Linkedin Pending Approval'),
    (46, 'Linkedin Approved'),
    (47, 'Linkedin Rejected By Admin'),
    (48, 'Linkedi Rejected By Candidate'),
    (49, 'Couselling form is pending'),

    # flow7 61 - 80
    (61, 'Service will be initiated once resume is finalized'),
    (62, 'Resume Boosted'),

    # flow6 81 - 100
    (81, 'Pending Varification Reports'),
    (82, 'Service is initiated'),

    # flow10 101 - 120
    (101, 'To start learning , it is mandatory to take this test'),

    # flow 3 121 - 141
    (121, 'Service has been processed and Final document is ready'),

    # flow9 141 - 160
    (141, 'Your profile to be shared with interviewer is pending'),
    (142, 'Round one is not expired'),
    (143, 'Round one is expired'),

)

OI_USER_STATUS = (
    # common status 1 - 20
    (0, 'Default'),
    (1, 'Assigned'),
    (2, 'Resume upload is pending'),
    (3, 'Resume Uploded'),
    (4, 'Closed'),
    (5, 'Service is under progress'),
    (6, 'Services has been processed'),
    (10, 'Service is initiate'),
    (11, 'Archived'),
    (12, 'Service is initiated'),


    # flow1, flow12, flow13, flow3, and flow 5 status 21 - 40
    (21, 'Upload Draft'),
    (22, 'Draft Uploaded'),
    (23, 'Pending Approval'),
    (24, 'Document uploaded'),
    (25, 'Rejected By Admin'),
    (26, 'Modifications requested'),
    (27, 'Service has been processed and Document is finalized'),

    # for linkedin flow8 41 - 60
    (43, 'Linkedin Draft Create'),
    (44, 'Linkedin Draft Created'),
    (45, 'Linkedin Pending Approval'),
    (46, 'Linkedin Approved'),
    (47, 'Linkedin Rejected By Admin'),
    (48, 'Linkedi Rejected By Candidate'),
    (49, 'Couselling form is pending'),

    # flow7 61 - 80
    (61, 'Service will be initiated once resume is finalized'),  # flow 4 and flow 5
    (62, 'Services has been processed'),

    # flow6 81 - 100
    (81, 'Service is under progress'),
    (82, 'Service is initiated'),

    # flow10 101 - 120
    (101, 'To start learning , it is mandatory to take this test'),

    # flow3 121 - 140
    (121, 'Service has been processed and Final document is ready'),

    # flow9 141 - 160
    (141, 'Your profile to be shared with interviewer is pending'),
    (142, 'Service is under progress'),
    (143, 'Service has been expired'),

)

COUNSELLING_FORM_STATUS = (
    (41, 'Counselling Form Not Submitted'),
    (42, 'Counselling Form Submitted'),
)
