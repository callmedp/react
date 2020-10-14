
# Constant Value For University Page

UNIVERSITY_PAGE = 4
UNIVERSITY_COURSE = 5
PAGECHOICES = (
	(0, '--Select Page--'),
	(1, 'Homepage'),
	(2, 'Roundone'),
	(3, 'Course Catalogue'),
    (6, 'Skill Page'),
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


TOPTRENDING_FA_MAPPING = {
  'Administration / Front Office / Secretary'       : 'Operations',
  'Architecture / Interior Design'                  : 'IT',
  'Customer Service / Back Office Operations'       : 'Operations',
  'Education / Training / Language'                 : 'IT',
  'Engineering Design / Construction'               : 'IT',
  'Environment / Health / Safety'                   : 'Sales & Marketing',
  'Finance / Accounts / Investment Banking'         : 'Banking & Finance',
  'Graphic Design / Web Design / Copywriting'       : 'IT',
  'HR'                                              : 'Human Resource',
  'HR / Recruitment'                                : 'Human Resource',
  'Hotel / Restaurant'                              : 'Sales & Marketing',
  'IT - Hardware / Networking / Telecom Engineering': 'IT',
  'IT - Software'                                   : 'IT',
  'Journalism / Content / Writing'                  : 'IT',
  'Legal / Company Secretary'                       : 'Law',
  'Management Consulting / Strategy / EA'           : 'Sales & Marketing',
  'Marketing / Advertising / MR / PR / Events'      : 'Sales & Marketing',
  'Medical / Healthcare'                            : 'Sales & Marketing',
  'Oil & Gas Engineering / Mining / Geology'        : 'Sales & Marketing',
  'Production / Maintenance / Service'              : 'Operations',
  'Quality / Testing (QA-QC)'                       : 'IT',
  'R&D / Product Design'                            : 'IT',
  'Real Estate'                                     : 'Sales & Marketing',
  'Retail / Export-Import / Trading'                : 'Banking & Finance',
  'SBU Head / CEO / Director / Entrepreneur'        : 'IT',
  'Sales / BD'                                      : 'Sales & Marketing',
  'Security / Detective Services'                   : 'Law',
  'Statistics / Analytics / Acturial Science'       : 'Operations',
  'Supply Chain / Purchase / Inventory'             : 'Operations',
  'TV / Film / Radio / Entertainment'               : 'Sales & Marketing',
  'other'                                           : 'IT'
  }



FA_TO_CAT_MAPPING = {
'Administration / Front Office / Secretary': 19,
 'Architecture / Interior Design': 22,
 'Customer Service / Back Office Operations': 19,
 'Education / Training / Language': 22,
 'Engineering Design / Construction': 22,
 'Environment / Health / Safety': 17,
 'Finance / Accounts / Investment Banking': 20,
 'Graphic Design / Web Design / Copywriting': 22,
 'HR': 25,
 'HR / Recruitment': 25,
 'Hotel / Restaurant': 17,
 'IT - Hardware / Networking / Telecom Engineering': 22,
 'IT - Software': 22,
 'Journalism / Content / Writing': 22,
 'Legal / Company Secretary': 23,
 'Management Consulting / Strategy / EA': 17,
 'Marketing / Advertising / MR / PR / Events': 17,
 'Medical / Healthcare': 17,
 'Oil & Gas Engineering / Mining / Geology': 17,
 'Production / Maintenance / Service': 19,
 'Quality / Testing (QA-QC)': 22,
 'R&D / Product Design': 22,
 'Real Estate': 17,
 'Retail / Export-Import / Trading': 20,
 'SBU Head / CEO / Director / Entrepreneur': 22,
 'Sales / BD': 17,
 'Security / Detective Services': 23,
 'Statistics / Analytics / Acturial Science': 19,
 'Supply Chain / Purchase / Inventory': 19,
 'TV / Film / Radio / Entertainment': 17,
 'other': 22


}
