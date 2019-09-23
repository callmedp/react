
# Constant Value For University Page

UNIVERSITY_PAGE = 4
UNIVERSITY_COURSE = 5
PAGECHOICES = (
	(0, '--Select Page--'),
	(1, 'Homepage'),
	(2, 'Roundone'),
	(3, 'Course Catalogue'),
	(UNIVERSITY_PAGE, 'University Page'),
	(UNIVERSITY_COURSE, 'University Course')
)

STATIC_PAGE_NAME_CHOICES = (
    (1, 'Privacy Policy'),
    (2, 'Terms and Condition'),
    (3, 'Disclaimer')
)

STATIC_SITE_ID_TO_SLUG_MAPPING = {
    1: 'privacy-policy',
    2: 'tnc',
    3: 'disclaimer'
}

STATIC_SITE_SLUG_TO_ID_MAPPING = {
    value: key for key, value in STATIC_SITE_ID_TO_SLUG_MAPPING.items()
}
