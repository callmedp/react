

FUNCTIONALAREA = [
    {u'pdesc': u'Sales & Marketing',
    u'pid': 1},
    {u'pdesc': u'Personality Development',
    u'pid': 2},
    {u'pdesc': u'IT - Software',
    u'pid': 3},
    {u'pdesc': u'Operation',
    u'pid': 4},
    {u'pdesc': u'Others',
    u'pid': 5},
    {u'pdesc': u'IT courses',
    u'pid': 6},
    {u'pdesc': u'Finance & Accounts',
    u'pid': 7},
    {u'pdesc': u'Legal courses',
    u'pid': 8},
    {u'pdesc': u'HR',
    u'pid': 9},
    {u'pdesc': u'Management',
    u'pid': 10},
    {u'pdesc': u'Media',
    u'pid': 11}
]

SKILL = [{u'pid': 1, u'pdesc': u'Sales'}, {u'pid': 2, u'pdesc': u'Customer Care'}, {u'pid': 3, u'pdesc': u'Product Marketing'}, {u'pid': 4, u'pdesc': u'Market Research & Planning'}, {u'pid': 5, u'pdesc': u'Event Marketing'}, {u'pid': 6, u'pdesc': u'Service Marketing'}, {u'pid': 7, u'pdesc': u'Digital Marketing'}, {u'pid': 8, u'pdesc': u'Relationship marketing'}, {u'pid': 9, u'pdesc': u'International Marketing'}, {u'pid': 10, u'pdesc': u'Retail'}, {u'pid': 11, u'pdesc': u'Communication Development'}, {u'pid': 12, u'pdesc': u'Language learning'}, {u'pid': 13, u'pdesc': u'Personal development'}, {u'pid': 14, u'pdesc': u'Interview'}, {u'pid': 15, u'pdesc': u'Production/Manufacturing'}, {u'pid': 16, u'pdesc': u'Product Quality'}, {u'pid': 17, u'pdesc': u'Service quality'}, {u'pid': 18, u'pdesc': u'Logistics and supply chain'}, {u'pid': 19, u'pdesc': u'Six Sigma'}, {u'pid': 20, u'pdesc': u'Project Management'}, {u'pid': 21, u'pdesc': u'Textile'}, {u'pid': 22, u'pdesc': u'Public safety'}, {u'pid': 23, u'pdesc': u'Real Estate'}, {u'pid': 24, u'pdesc': u'Hospitality'}, {u'pid': 25, u'pdesc': u'Energy'}, {u'pid': 26, u'pdesc': u'Medical course'}, {u'pid': 27, u'pdesc': u'Architecture'}, {u'pid': 28, u'pdesc': u'Librarian'}, {u'pid': 29, u'pdesc': u'Hardware'}, {u'pid': 30, u'pdesc': u'Exams prparational courses'}, {u'pid': 31, u'pdesc': u'Management'}, {u'pid': 32, u'pdesc': u'Development'}, {u'pid': 33, u'pdesc': u'Content'}, {u'pid': 34, u'pdesc': u'Web Analytics'}, {u'pid': 35, u'pdesc': u'SEO'}, {u'pid': 36, u'pdesc': u'Graphics'}, {u'pid': 37, u'pdesc': u'Design'}, {u'pid': 38, u'pdesc': u'IT software'}, {u'pid': 39, u'pdesc': u'IT support'}, {u'pid': 40, u'pdesc': u'Admin'}, {u'pid': 41, u'pdesc': u'IT development interface learning'}, {u'pid': 42, u'pdesc': u'Big Data'}, {u'pid': 43, u'pdesc': u'Data base development'}, {u'pid': 44, u'pdesc': u'Cloud computing'}, {u'pid': 45, u'pdesc': u'IT Quality & Testing'}, {u'pid': 46, u'pdesc': u'IT languages'}, {u'pid': 47, u'pdesc': u'IT strategist'}, {u'pid': 48, u'pdesc': u'Network & Security'}, {u'pid': 49, u'pdesc': u'Telecom & Networking'}, {u'pid': 50, u'pdesc': u'Electronic Designs'}, {u'pid': 51, u'pdesc': u'MS skills'}, {u'pid': 52, u'pdesc': u'Stock Market Trading'}, {u'pid': 53, u'pdesc': u'Financial Analyst'}, {u'pid': 54, u'pdesc': u'Financial Reporting and management'}, {u'pid': 55, u'pdesc': u'Advanced accounting'}, {u'pid': 56, u'pdesc': u'Investment Banking'}, {u'pid': 57, u'pdesc': u'Risk Mangement'}, {u'pid': 58, u'pdesc': u'Accounting Fundamental'}, {u'pid': 59, u'pdesc': u'Audit and Assurance'}, {u'pid': 60, u'pdesc': u'Banking'}, {u'pid': 61, u'pdesc': u'Commercial operation'}, {u'pid': 62, u'pdesc': u'Company Law'}, {u'pid': 63, u'pdesc': u'Criminal law'}, {u'pid': 64, u'pdesc': u'Cyber Law'}, {u'pid': 65, u'pdesc': u'Conflict Management'}, {u'pid': 66, u'pdesc': u'Training and Development'}, {u'pid': 67, u'pdesc': u'Talent & Acquisition'}, {u'pid': 68, u'pdesc': u'compensation'}, {u'pid': 69, u'pdesc': u'Organizational structure'}, {u'pid': 70, u'pdesc': u'Corporate governance'}, {u'pid': 71, u'pdesc': u'Strategic management'}, {u'pid': 72, u'pdesc': u'Decision Making Mangement'}, {u'pid': 73, u'pdesc': u'Analyst'}, {u'pid': 74, u'pdesc': u'Data Mining'}, {u'pid': 75, u'pdesc': u'General Managment'}, {u'pid': 76, u'pdesc': u'International Trade'}, {u'pid': 77, u'pdesc': u'Journalism'}, {u'pid': 78, u'pdesc': u'Editor'}, {u'pid': 79, u'pdesc': u'Public Relations'}]

AREA_WITH_LABEL = [('', 'Functional Area')] + [(area['pid'], area['pdesc']) for area in FUNCTIONALAREA]

SKILL_WITH_LABEL = [('', 'Key Skills')] + [(skill['pid'], skill['pdesc']) for skill in SKILL]

# FA Facets Grouping
FA_FACETS = {area['pid']: area['pdesc'] for area in FUNCTIONALAREA}

CL_FACETS = {
    'bg': 'Beginner',
    'im': 'Intermediate',
    'ad': 'Advanced'
}

CERT_FACETS = {
    'true': 'Required',
    0: 'Not Required'
}

DURATION_FACETS = {
    "d0": "0-1 month",
    "d1": "1-3 months",
    "d2": "3-6 months",
    "d3": "6-9 months",
    "d4": "9-12 months",
    "d5": "1-2 years",
    "d6": "2-3 years",
    "d7": "3+ years"
}

STUDY_FACETS = {
    "ol": "Online",
    "cl": "Classroom",
    "bl": "Blended"
}

PRICE_FACETS = {
    1: "0-10000",
    2: "10001-20000",
    3: "20001-30000",
    4: "30001-40000",
    5: "40000+"
}