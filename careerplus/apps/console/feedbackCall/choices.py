FEEDBACK_STATUS = ((1,"Pending"),
                    (2,"Assigned"),
                    (3,"Closed"))

FEEDBACK_RESOLUTION_CHOICES = ((1, "Shared the service details"),
                            (2, "Shared the login details"),
                            (3, "Shared the drafts"),
                            (4, "Swapping of the services"),
                            (5, "Complimentary service"),
                            (6, "Educate about the services"))


FEEDBACK_PARENT_CATEGORY_CHOICES = ((1, "Connected"),
                            (2, "Not Connected"))

FEEDBACK_CATEGORY_CHOICES_ID_1 =((101, "Service Utilized"),
                                  (102, "Not Utilized"),
                                  (103, "In process"),
                                  (104, "Annoyed"),
                                  (105, "Call Back"))

FEEDBACK_CATEGORY_CHOICES_ID_2 =((201, "Not Connected"),)

FEEDBACK_CATEGORY_CHOICES = FEEDBACK_CATEGORY_CHOICES_ID_1 + FEEDBACK_CATEGORY_CHOICES_ID_2