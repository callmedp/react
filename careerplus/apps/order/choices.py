CANCELLED = 5
OI_CANCELLED = 14
STATUS_CHOICES = (
    (0, "Unpaid"),
    (1, "Paid"),
    (2, "InProcess"),
    (3, "Closed"),
    (4, "Archive"),
    (CANCELLED, "Cancelled"),
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
    (11, "PayLater"))


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
    (OI_CANCELLED, 'Cancelled'),

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
    (42, 'Counselling Form Submitted'),
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
    (81, 'Pending Verification Reports'),
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
    (164, 'Replaced'),

    # extra operation 181 - 190
    (181, "Waiting for input")
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
    (24, 'Document is ready'),
    (25, 'Rejected By Admin'),
    (26, 'Modifications requested'),
    (27, 'Service has been processed and Document is finalized'),
    (28, 'Feature profile initiated'),
    (29, 'Feature profile expired'),
    (30, 'Feature profile updated'),

    # for linkedin flow8 41 - 60
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
    (164, 'Replaced'),
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
    (2, 'Sent Process Mailers'),
    (3, 'Sent Welcome Email'),
    (4, 'Sent Forgot Email'),
    (5, 'Sent Feedback Email'),
    (6, 'Sent Feedback Coupon Email'),
    (7, 'Sent Payment Realisation Email'),
    (8, 'Sent Cart Drop Out Mailer'),
    (9, 'Sent Closer Mailer'),

    # flow1 :21 - 40
    (21, 'Sent Flow1 Pending Resume Email'),
    (22, 'Sent First Draft Email'),
    (23, 'Sent Second Draft Email'),
    (24, 'Sent Final Draft Email'),
    (25, 'Sent Flow1 Process Mailer'),
    (26, 'Sent Reminder Draft1 Email'),
    (27, 'Sent Reminder Draft2 Email'),
    (28, 'Sent Flow1 Allocated Writer Email'),

    # flow3 :41 - 60
    (41, 'Sent Resume Critique Pending Resume Email'),
    (42, 'Sent Resume Critique Allocated To Writer Email'),
    (43, 'Sent Resume Critique Closed Email'),
    (44, 'Sent Resume Critique Process Mailer'),

    # flow4 :61 - 70
    (61, 'Sent International Profile Pending Resume Email'),
    (62, 'Sent International profile updated Email'),
    (63, 'Sent International profile Writer Assignment Email'),
    (64, 'Sent International profile Process Mailer'),

    # flow5 :71 - 80
    (71, 'Sent Feature Profile Pending Resume Email'),
    (72, 'Sent Feature profile Updated Email'),
    (74, 'Sent Feature profile Process Mailer'),

    # flow7 :91 - 100
    (91, 'Sent Resume Booster Pending Resume Email'),
    (92, 'Sent Resume Booster consultant/Recruiter Email'),
    (93, 'Sent Resume Booster Candidate Email'),
    (94, 'Sent Resume Booster Candidate Process Mailer'),

    # linkedin flow 8:101-120
    (101, 'Sent Allocated To Writer Email For Linkedin'),
    (102, 'Sent Linkedin First Draft Email'),
    (103, 'Sent Linkedin Second Draft Email'),
    (104, 'Sent Linkedin Final Draft Email'),
    (105, 'Sent Linkedin Process Mailer'),
    (106, 'Sent Linkedin Draft1 Reminder Email'),
    (107, 'Sent Linkedin Draft2 Reminder Email'),
    (108, 'Sent Pending Counselling Form Email'),
    (109, 'Sent Linked In Tip 1'),
    (110, 'Sent Linked In Tip 2'),
    (111, 'Sent Linked In Tip 3'),
    (112, 'Sent Linked In Tip 4'),
    (113, 'Sent Linked In Tip 5'),
    (114, 'Sent Linked In Tip 6'),

    # flow9 :121 - 130
    (121, 'Sent RoundOne Incomplete Profile Email'),
    (122, 'Sent RoundOne Process Mailer'),

    # flow10 :131 - 140
    (131, 'Sent Pending Studymate Test Email'),
    (132, 'Sent Studymate Process Mailer'),

    # flow12 :141 - 150
    (141, 'Sent Flow12 Pending Resume Email'),
    (142, 'Sent Flow12 First Draft Email'),
    (143, 'Sent Flow12 Second Draft Email'),
    (144, 'Sent Flow12 Final Draft Email'),
    (145, 'Sent Flow12 Process Mailer'),
    (146, 'Sent Flow12 Assignment Mailer'),

    # flow13 :151 - 160
    (151, 'Sent Flow13 Pending Resume Email'),
    (152, 'Sent Flow13 First Draft Email'),
    (153, 'Sent Flow13 Second Draft Email'),
    (154, 'Sent Flow13 Final Draft Email'),
    (155, 'Sent Flow13 Process Mailer'),
    (156, 'Sent Flow13 Assignment Mailer'),

    # flow2 :161 - 170
    (161, 'Sent Flow2 Process Mailer'),

    # flow6 :171 - 180
    (171, 'Sent Flow6 Process Mailer'),

    # cashback wallet status: 181 - 190
    (181, ''),

    # flow14 :191 - 200
    (191, 'Sent Flow14 Process Mailer'),
    (192, 'Sent Flow14 Service Initiation Mailer'),
)

OI_SMS_STATUS = (
    # common status for sending sms 1-20
    (0, 'default'),
    (1, 'Sent Offline Payment Sms'),
    (2, 'Sent Online Payment Sms'),
    # this closer sms for flow1 and flow 8.
    (3, 'Sent Resume Auto Closer Sms'),
    # this closer sms for flow 2,6 and 10.
    (4, 'Sent Closer Sms'),
    (5, 'Sent Sms For Paid Order day1'),
    (6, 'Sent Sms For Paid Order day2'),

    # flow1 :21 - 40
    (21, 'Sent Flow1 Pending Resume Sms'),
    (22, 'Sent First Draft Sms'),
    (23, 'Sent Second Draft Sms'),
    (24, 'Sent Final Draft Sms'),
    (25, 'Sent Reminder Draft1 Sms'),
    (26, 'Sent Reminder Draft2 Sms'),
    (27, 'Sent Flow1 Online Payment Sms'),

    # flow3 :41 - 60
    (41, 'Sent Resume Critique Pending Resume Sms'),
    (42, 'Sent Resume Critique Closed Sms'),
    (43, 'Sent Flow3 Online Payment Sms'),

    # flow4 :61 - 70
    (61, 'Sent International Profile Pending Resume Sms'),
    (62, 'Sent Flow4 Online Payment Sms'),
    
    # flow5 :71 - 80
    (71, 'Sent Feature Profile Pending Resume Sms'),
    (72, 'Sent Flow5 Online Payment Sms'),

    # flow7 :91 - 100
    (91, 'Sent Resume Booster Pending Resume Sms'),
    (92, 'Sent Resume Booster consultant/Recruiter Sms'),
    (93, 'Sent Resume Booster Candidate Sms'),
    (94, 'Sent Flow7 Online Payment Sms'),
    
    # linkedin flow 8:101-120
    (101, 'Sent Allocated To Writer Sms For Linkedin'),
    (102, 'Sent Linkedin First Draft Sms'),
    (103, 'Sent Linkedin Second Draft Sms'),
    (104, 'Sent Linkedin Final Draft Sms'),
    (105, 'Sent Flow8 Online Payment Sms'),
    (106, 'Sent Linkedin Draft1 Reminder Sms'),
    (107, 'Sent Linkedin Draft2 Reminder Sms'),
    (108, 'Sent Pending Counselling Form Sms'),
    
    # flow9 :121 - 130
    (121, 'Sent RoundOne Incomplete Profile Sms'),
    (122, 'Sent Flow9 Online Payment Sms'),

    # flow10 :131 - 140
    (131, 'Sent Pending Studymate Test Sms'),
    (132, 'Sent Flow10 Online Payment Sms'),
    (133, 'Sent Flow10 Service Initiation Sms'),

    # flow12 :141 - 150
    (141, 'Sent Flow12 Pending Resume Sms'),
    (142, 'Sent Flow12 First Draft Sms'),
    (143, 'Sent Flow12 Second Draft Sms'),
    (144, 'Sent Flow12 Final Draft Sms'),
    (145, 'Sent Flow12 Online Payment Sms'),

    # flow13 :151 - 160
    (151, 'Sent Flow13 Pending Resume Sms'),
    (152, 'Sent Flow13 First Draft Sms'),
    (153, 'Sent Flow13 Second Draft Sms'),
    (154, 'Sent Flow13 Final Draft Sms'),
    (155, 'Sent Flow13 Online Payment Sms'),

    # flow2 :161 - 170
    (161, 'Sent Flow2 Process Sms'),
    (162, 'Sent Flow2 Service Initiation Sms'),

    # flow6 :171 - 180
    (171, 'Sent Flow6 Process Sms'),
    (172, 'Sent Flow6 Service Initiation Sms'),


    # flow14 :191 - 200
    (191, 'Sent Flow14 Process Sms'),
    (192, 'Sent Flow14 Service Initiation Sms'),
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

WC_CATEGORY = (
    # 21 - 40
    (21, 'Process Order'),
    (22, 'Service Issue'),
    (23, 'Call Back')
)

WC_SUB_CATEGORY1 = (
    # 41 - 60
    (41, 'No Issue'),
    (42, 'Order Processed After Final Reminder'),
)

WC_SUB_CATEGORY2 = (
    # 61 - 80
    (62, 'On Hold'),
    (63, 'Process order'),
    (64, 'Refund'),
    (65, 'Replacement Order'),
)

WC_SUB_CAT2 = (
    (61, 'Service Issue'),
)

WC_SUB_CATEGORY3 = (
    # 81 - 100
    (81, 'No answer'),
    (82, 'Not reachable'),
    (83, 'User is busy'),
)


WC_SUB_CATEGORY = WC_SUB_CATEGORY1 + WC_SUB_CATEGORY2 + WC_SUB_CATEGORY3 + WC_SUB_CAT2

WC_FLOW_STATUS = (
    # 0-20
    (0, 'Default'),
    (1, 'Assigned'),
    (2, 'Re Allocated'),

    # 21 - 40

    # 41 - 60
    (41, 'No Issue'),
    (42, 'Order Processed After Final Reminder'),

    # 61 - 80
    (61, 'Service Issue'),
    (62, 'On Hold'),
    (63, 'Process order'),
    (64, 'Refund'),
    (65, 'Replacement Order'),

    # 81 - 100
    (81, 'No answer'),
    (82, 'Not reachable'),
    (83, 'User is busy'),
)


SMS_DRAFT_OI_MAPPING = {
    1:'102',
    2: '103',
    3: '104',

}

BOOSTER_RECRUITER_TYPE = (
    (0, 'Resume Booster India'),
    (1, 'Resume Booster International'),
)
