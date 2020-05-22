# python imports

# django imports

# local imports

# inter app imports

# third party imports

STATUS_CHOICES = (
    (0, "Open - currently active but no owner"),  # EDITABLE
    (1, "Merged - merged in other cart"),
    (2, "Saved - currently active but with owner"),  # EDITABLE
    (3, "Express - currently active"),
    (4, "Frozen - the cart cannot be modified"),
    (5, "Closed - order has been made"),
    (6, "Archive - cart need to be archived"),
)

# handling cart for resume shine and shine learning.
SITE_STATUS = (
    (0, "Shine Learning"),
    (1, "Resume Shine")
)

COUNTRY_CHOICES = (
    ()
)
