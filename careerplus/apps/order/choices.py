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
    (46, 'Linkedin Approved'),
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

    # flow4 161 - 180
    

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
    # (25, 'Sent Flow1 Service Closed Email'),
    (26, 'Sent Reminder Draft1 Email'),
    (27, 'Sent Reminder Draft2 Email'),
    (28, 'Sent Flow1 Allocated Writer Email'),

    # flow3 :41 - 60
    (41, 'Sent Resume Critique Pending Resume Email'),
    (42, 'Sent Resume Critique Allocated To Writer Email'),
    (42, 'Sent Resume Critique Closed Email'),

    # flow4 :61 - 70
    (61, 'Sent International Profile Pending Resume Email'),
    (62, 'Sent International profile updated Email'),
    (63, 'Sent International profile Writer Assignment Email'),

    # flow5 :71 - 80
    (71, 'Sent Feature Profile Pending Resume Email'),
    (72, 'Sent Feature profile Updated Email'),

    # flow7 :91 - 100
    (91, 'Sent Resume Booster Pending Resume Email'),
    (92, 'Sent Resume Booster consultant/Recruiter Email'),
    (93, 'Sent Resume Booster Candidate Email'),
    
    # linkedin flow 8:101-120
    (101, 'Sent Allocated To Writer Email For Linkedin'),
    (102, 'Sent Linkedin First Draft Email'),
    (103, 'Sent Linkedin Second Draft Email'),
    (104, 'Sent Linkedin Final Draft Email'),
    # (105, 'Sent Linkedin Service Closed Email'),
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

    # flow10 :131 - 140
    (131, 'Sent Pending Studymate Test Email'),

    # flow12 :141 - 150
    (141, 'Sent Flow12 Pending Resume Email'),
    (142, 'Sent Flow12 First Draft Email'),
    (143, 'Sent Flow12 Second Draft Email'),
    (144, 'Sent Flow12 Final Draft Email'),

    # flow13 :151 - 160
    (151, 'Sent Flow13 Pending Resume Email'),
    (152, 'Sent Flow13 First Draft Email'),
    (153, 'Sent Flow13 Second Draft Email'),
    (154, 'Sent Flow13 Final Draft Email'),   
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

    # flow1 :21 - 40
    (21, 'Sent Flow1 Pending Resume Sms'),
    (22, 'Sent First Draft Sms'),
    (23, 'Sent Second Draft Sms'),
    (24, 'Sent Final Draft Sms'),
    (25, 'Sent Reminder Draft1 Email'),
    (26, 'Sent Reminder Draft2 Email'),

    # flow3 :41 - 60
    (41, 'Sent Resume Critique Pending Resume Sms'),
    (42, 'Sent Resume Critique Closed Sms'),

    # flow4 :61 - 70
    (61, 'Sent International Profile Pending Resume Sms'),
    
    # flow5 :71 - 80
    (71, 'Sent Feature Profile Pending Resume Sms'),

    # flow7 :91 - 100
    (91, 'Sent Resume Booster Pending Resume Sms'),
    (92, 'Sent Resume Booster consultant/Recruiter Sms'),
    (93, 'Sent Resume Booster Candidate Sms'),
    
    # linkedin flow 8:101-120
    (101, 'Sent Allocated To Writer Sms For Linkedin'),
    (102, 'Sent Linkedin First Draft Sms'),
    (103, 'Sent Linkedin Second Draft Sms'),
    (104, 'Sent Linkedin Final Draft Sms'),
    # (105, 'Sent Linkedin Service Closed Email'),
    (106, 'Sent Linkedin Draft1 Reminder Sms'),
    (107, 'Sent Linkedin Draft2 Reminder Sms'),
    (108, 'Sent Pending Counselling Form Email'),
    
    # flow9 :121 - 130
    (121, 'Sent RoundOne Incomplete Profile Sms'),

    # flow10 :131 - 140
    (131, 'Sent Pending Studymate Test Sms'),

    # flow12 :141 - 150
    (141, 'Sent Flow12 Pending Resume Sms'),
    (142, 'Sent Flow12 First Draft Sms'),
    (143, 'Sent Flow12 Second Draft Sms'),
    (144, 'Sent Flow12 Final Draft Sms'),

    # flow13 :151 - 160
    (151, 'Sent Flow13 Pending Resume Sms'),
    (152, 'Sent Flow13 First Draft Sms'),
    (153, 'Sent Flow13 Second Draft Sms'),
    (154, 'Sent Flow13 Final Draft Sms'),   
)