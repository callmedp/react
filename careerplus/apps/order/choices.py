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
    (2, 'Citrus Pay'),
    (3, 'EMI'),
    (4, 'Cheque or Draft'),
    (5, 'CC-Avenue'),
    (6, 'Mobikwik'),
    (7, 'CC-Avenue-International'),
    (8, 'Debit Card'),
    (9, 'Credit Card'),
    (10, 'Net Banking'),)


OI_OPS_STATUS = (
    # common status 1 - 20
    (0, 'Default'),
    (1, 'Assigned'),
    (2, 'Resume upload is pending'),
    (3, 'Resume Uploaded'),
    (4, 'Closed'),
    (5, 'Service is under progress'),
    (6, 'Service has been processed'),
    (10, 'On Hold by Vendor'),
    (11, 'Archived'),
    (12, 'Unhold by Vendor'),
    (13, 'Shine Resume'),

    # flow1, flow3, flow12, flow13, and flow 5 status 21 - 40
    (21, 'Upload Draft'),
    (22, 'Draft Uploaded'),
    (23, 'Pending Approval'),
    (24, 'Approved'),
    (25, 'Rejected By Admin'),
    (26, 'Rejected By Candidate'),
    (27, 'Service has been processed and Document is finalized'),  # user Accept the draft flow 8 too
    (28, 'Feature profile initiated'),
    (29, 'Feature profile expired'),
    (30, 'Feature profile updated'),

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

    # refund flow 161 - 180
    (161, 'Refund initiated'),
    (162, 'Refund under progress'),
    (163, 'Refunded'),
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
    (13, 'Shine Resume'),


    # flow1, flow12, flow13, flow3, and flow 5 status 21 - 40
    (21, 'Upload Draft'),
    (22, 'Draft Uploaded'),
    (23, 'Pending Approval'),
    (24, 'Document uploaded'),
    (25, 'Rejected By Admin'),
    (26, 'Modifications requested'),
    (27, 'Service has been processed and Document is finalized'),
    (28, 'Feature profile initiated'),
    (29, 'Feature profile expired'),
    (30, 'Feature profile updated'),

    # for linkedin flow8 41 - 60
    (43, 'Linkedin Draft Create'),
    (44, 'Linkedin Draft Created'),
    (45, 'Linkedin Pending Approval'),
    (46, 'Document is Ready'),
    (47, 'Linkedin Rejected By Admin'),
    (48, 'Modifications requested'),
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

    # refund flow 161 - 180
    (161, 'Refund initiated'),
    (162, 'Refund under progress'),
    (163, 'Refunded'),

)

OI_LINKEDIN_FLOW_STATUS = (
    (0, 'default'),
    (41, 'Counselling Form Not Submitted'),
    (42, 'Counselling Form Submitted'),
    (50, 'Draft 1 Send'),
    (51, 'Linked In Tip 1'),
    (52, 'Linked In Tip 2'),
    (53, 'Linked In Tip 3'),
    (54, 'Linked In Tip 4'),
    (55, 'Linked In Tip 5'),
    (56, 'Linked In Tip 6'),
)

OI_EMAIL_STATUS = (
    # common status for sending email 1-20
    (0, 'default'),
    (1, 'Sent Payment Pending Email'),
    (2, 'Sent Pending Item Email'),
    (3, 'Sent Process Mailers'),
    (4, 'Sent Welcome Email'),
    (5, 'Sent Forgot Email'),
    (6, 'Sent Feedback Email'),
    (7, 'Sent Feedback Coupon Email'),
    (8, 'Sent Payment Realisation Email'),

    # flow 1, 8, 3, 4:21-40
    (21, 'Sent Service Closed Email'),
    (22, 'Sent Draft Reminder Email'),
    (23, 'Sent Service Closed Email'),
    (24, 'Sent International Profile Updated Email'),
)


REFUND_MODE = (
    ('select', 'Select Refund Mode'),
    ('neft', 'NEFT'),
    ('cheque', 'CHEQUE'),
    ('dd', 'DD'),
)

TYPE_REFUND = (
    ('select', 'Select Refund Type'),
    ('full', 'Full Refund'),
    ('partial', 'Partial Refund'),
)

REFUND_OPS_STATUS = (
    (0, "Default"),
    (1, "Ops Head Approval"),
    (2, "Ops Head Rejected"),
    (3, "Business Head Approval"),
    (4, "Business Head Rejected"),
    (5, "Dept. Head Approval"),
    (6, "Dept. Head Rejected"),
    (7, "Finance Approval"),
    (8, "Refund Approved"),  # show in finance queue to refund
    (9, "Refund Initiate"),
    (10, "Refund under progress"),
    (11, "Refunded"),
    (12, "Request Updated"),
    (13, "Cancel Request"),
)