
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

PAGENAME = (
    (1, 'Privacy Policy'),
    (2, 'Terms and Condition'),
    (3, 'Disclaimer')
)

PAGESLUG = {
    'privacy-policy':(1,'Privacy Policy'),
    'tnc':(2,'Terms and Condition'),
    'disclaimer':(3,'Disclaimer')
}