STATUS_CHOICES = (
    (0, "Open - currently active but no owner"),  #EDITABLE
    (1, "Merged - merged in other cart"),
    (2, "Saved - currently active but with owner"),  #EDITABLE
    (3, "Submitted - gone for payment after checkout"),
    (4, "Frozen - the cart cannot be modified"),
    (5, "Closed - order has been made"),
    (6, "Archive - cart need to be archived"),
)
