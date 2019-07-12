FEEDBACK_STATUS = ((1,"Pending"),
                    (2,"Assigned"),
                    (3,"Closed"))

FEEDBACK_RESOLUTION_CHOICES = ((1, "Shared the service details"),
                            (2, "Shared the login details"),
                            (3, "Shared the drafts"),
                            (4, "Swapping of the services"),
                            (5, "Complimentary service"),
                            (6, "Educate about the services"))


FEEDBACK_PARENT_CATEGORY_CHOICES = ((1, "Satisfied"),
                            (2, "unsatisfied"),
                            (3, "Displeased"),
                            (4, "Pending"))

FEEDBACK_CATEGORY_CHOICES_ID_1 =((101, "Rating"),
                                    (102, "Referral"),
                                    (103, "Shared Feedback"))

FEEDBACK_CATEGORY_CHOICES_ID_2 =((201, "Unaware of the services"),
                                    (202, "Login details not received"),
                                    (203, "Draft not received"),
                                    (204, "No relevancy"))

FEEDBACK_CATEGORY_CHOICES_ID_3 =((301, "100% job guarantee"),
                                    (302, "Up-selling"),
                                    (303, "Job&Interview guarantee"))

FEEDBACK_CATEGORY_CHOICES_ID_4 =((401, "Call back scheduled"),
                                    (402, "Not Responded"))

FEEDBACK_CATEGORY_CHOICES = FEEDBACK_CATEGORY_CHOICES_ID_1 + FEEDBACK_CATEGORY_CHOICES_ID_2 + FEEDBACK_CATEGORY_CHOICES_ID_3 + FEEDBACK_CATEGORY_CHOICES_ID_4