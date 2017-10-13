from decimal import Decimal

RELATION_CHOICES = (
    (0, 'Default'),
    (1, 'UpSell'),
    (2, 'Recommendation'),
    (3, 'CrossSell'),)

SERVICE_CHOICES = (
    (0, 'Default'),
    (1, 'Writing Services'),
    (2, 'Job Assistance Services'),
    (3, 'Courses'),
    (4, 'Other Services'),)

CATEGORY_CHOICES = (
    (0, 'Default'),
    (1, 'Level 1'),
    (2, 'Level 2'),
    (3, 'Level 3'),
    (4, 'Level 4'),)

PRODUCT_VENDOR_CHOICES = (
    (0, 'Standalone/Simple'),
    (1, 'Variation-Parent'),)


PRODUCT_CHOICES = PRODUCT_VENDOR_CHOICES + ((2, 'Variation-Child'),
    (3, 'Combo'),
    (4, 'No-Direct-Sell/Virtual'),
    (5, 'Downloadable'),)

FLOW_CHOICES = (
    (0, 'Default'),
    (1, 'Resume Writing India'),  # flow1
    (2, 'Courses'),  # flow2
    (3, 'Resume Critique'),  # flow3
    (4, 'International Profile Update'),  # flow4
    (5, 'Featured Profile'),  # flow5
    (6, 'IDfy Assessment'),  # flow6
    (7, 'Resume Booster'),  # flow7
    (8, 'Linkedin'),  # flow8
    (9, 'Round One'),  # flow9
    (10, 'StudyMate'),  # flow 10
    (11, 'TSSC'),  # flow 11
    (12, 'Country Specific Resume'),  # flow 12
    (13, 'Executive Bio,Portfolio,Visual Resume,Cover Letter,Second Regular Resume'),  # flow 13
)

BG_COLOR = {0: "#c8b98d", 1: "#cfbabd", 2: "#75dac2", 3: "#d2db86",
    4: "#a69cba", 5: "#8cb3f6", 6: "#9ac7e5", 7: "#ad9c7f",
    8: "#80d7ff", 9: "#a48e96", 10: "#b4e4fc", 11: "#d7ccc8",
    12: "#a3e77d", 13: "#ebdcc9", 14: "#9fdbd6", 15: "#a19f9c",
    16: "#deae9e", 17: "#73a4d4", 18: "#cba5bf", 19: "#9099c6",
    20: "#d9bee7", 21: "#cddb3a", 22: "#81c783", 23: "#afbec6",
    24: "#cdac98", 25: "#c5cbe9", 26: "#d5d5d5", 27: "#e39b71"
}
BG_CHOICES = tuple(BG_COLOR.items())


DURATION_DICT = {
    'D0': '0-1 month',
    'D1': '1- 3 month',
    'D2': '3-6 month',
    'D3': '9 months',
    'D4': '9-12 months',
    'D5': '1 -2 years',
    'D6': '2 -3 years',
    'D7': '3+ years',
}


def convert_to_month(days=0):
    if days:
        months = int(days)//30
        if 0 <= months <= 1:
            return 'D0'
        elif 1 < months <= 3:
            return 'D1'
        elif 3 < months <= 6:
            return 'D2'
        elif 6 < months <= 9:
            return 'D3'
        elif 9 < months <= 12:
            return 'D4'
        elif 12 < months <= 24:
            return 'D5'
        elif 24 < months <= 36:
            return 'D6'
        elif 36 < months:
            return 'D7'
    return 'D0'


C_ATTR_DICT = {
    'SM': 'study_mode',
    'DD': 'duration_day',
    'CERT': 'certification',
    'CL': 'course_level',
    'CT': 'course_type',
    'CD': 'course_doc',
    'CI': 'course_im',
}

R_ATTR_DICT = {
    'EXP': 'experience_writing',
}

S_ATTR_DICT = {
    'EXP': 'experience_service',
    'FD': 'feature_duration',
    'SD': 'service_doc',
    'SI': 'service_im',
}

STUDY_MODE = dict((
    ('ON', 'Online'),
    ('OF', 'Offline'),
    ('IL', 'Instructor Led'),
    ('BL', 'Blended'),
    ('CA', 'Classroom'),
    ('CF', 'Certifications'),
    ('DL', 'Distance Learning'),
    ))

EXP_DICT = dict((
    ('FR', '0-1 years'),
    ('FP', '1-4 years'),
    ('SP', '4-8 years'),
    ('EP', '8-15 years'),
    ('DP', '15+ years')))

COURSE_TYPE_DICT = dict((
    ('BS', 'Basic'),
    ('BD', 'Basic + More Deliverable'),))


def convert_inr(price=Decimal(0)):
    if price:
        if Decimal(0) <= price <= Decimal(1000):
            return '1'
        elif Decimal(1000) < price <= Decimal(5000):
            return '2'
        elif Decimal(5000) < price <= Decimal(10000):
            return '3'
        elif Decimal(10000) < price <= Decimal(25000):
            return '4'
        elif Decimal(25000) < price:
            return '5'
    return '0'


def convert_usd(price=Decimal(0)):
    if price:
        if Decimal(0) <= price <= Decimal(20):
            return '1'
        elif Decimal(20) < price <= Decimal(100):
            return '2'
        elif Decimal(100) < price <= Decimal(200):
            return '3'
        elif Decimal(200) < price <= Decimal(500):
            return '4'
        elif Decimal(500) < price:
            return '5'
    return '0'


def convert_aed(price=Decimal(0)):
    if price:
        if Decimal(0) <= price <= Decimal(50):
            return '1'
        elif Decimal(50) < price <= Decimal(100):
            return '2'
        elif Decimal(100) < price <= Decimal(200):
            return '3'
        elif Decimal(200) < price <= Decimal(500):
            return '4'
        elif Decimal(500) < price:
            return '5'
    return '0'


def convert_gbp(price=Decimal(0)):
    if price:
        if Decimal(0) <= price <= Decimal(15):
            return '1'
        elif Decimal(15) < price <= Decimal(60):
            return '2'
        elif Decimal(60) < price <= Decimal(120):
            return '3'
        elif Decimal(120) < price <= Decimal(360):
            return '4'
        elif Decimal(360) < price:
            return '5'
    return '0'


SEARCH_OPTIONS = [
    'Business Analyst Certification',
    'AML KYC Compliance Officer',
    'Accounting Fundamentals',
    'Accounting Fundamentals with GetCertGo Certification',
    'Advanced Certificate Program in Business Analytics',
    'Agile Practitioner - PMI ACP and Scrum Master Aligned',
    'Australia',
    'Behavioural Event Interviewing',
    'Budgeting Essentials',
    'Budgeting Essentials with GetCertGo Certification',
    'Business Accountant',
    'Business Communication Specialist',
    'Business Law Analyst',
    'Business Law Essentials',
    'Canada',
    'Certifed Search Engine Marketing Professional Course',
    'Certificate in Cross Cultural Communication',
    'Certificate in Cross-Functional Teams Management',
    'Certificate in Derivatives Fundamentals ',
    'Certificate in Derivatives Market Strategies',
    'Certificate in E-mail Skills',
    'Certificate in International Trade and Foreign Exchange',
    'Certificate in Predictive Analytics',
    'Certificate in Statistics and Probability',
    'Certified Advanced Management Skills Professional',
    'Certified Biopharmaceutical Professional',
    'Certified Blogging and Content Marketing Professional',
    'Certified Business Analytics Professional',
    'Certified Business Intelligence Professional',
    'Certified Business Strategy Execution Professional',
    'Certified Compensation and Benefits Manager',
    'Certified Consumer Behavior Analyst',
    'Certified Corporate Governance Professional',
    'Certified Corporate Strategy Professional',
    'Certified Digital Marketing Professional',
    'Certified Digital Marketing Professional (CDMP) Course',
    'Certified Distribution Manager',
    'Certified Email Marketing Master Course',
    'Certified Email Marketing Professional Course',
    'Certified Environmentalist',
    'Certified Export Import (Foreign Trade) Professional',
    'Certified Facility Manager',
    'Certified Financial Ratio Analysis Professional',
    'Certified Financial Risk management Professional',
    'Certified GAAP Professional',
    'Certified Guitar Basics Professional',
    'Certified HR Mergers and Acquisition Professional',
    'Certified International Marketing Analyst',
    'Certified Kaizen Professional',
    'Certified Management Skills Professional',
    'Certified Manager for Quality and Organizational Excellence',
    'Certified Market Research Analyst',
    'Certified Marketing Planning Manager',
    'Certified Material Management Professional',
    'Certified Mobile Marketing Master (CMMM) Course',
    'Certified Multichannel Retail Professional',
    'Certified Music Professional',
    'Certified Organizational Change Professional',
    'Certified Organizational Priorities Management Professional',
    'Certified Personal Beauty Professional',
    'Certified Planning and Scheduling Manager',
    'Certified Search Engine Optimization Master Course',
    'Certified Service Quality Manager',
    'Certified Six Sigma Black Belt Master',
    'Certified Six Sigma Green Belt Master',
    'Certified Smart Cities Professional',
    'Certified Smartphone Photography Professional',
    'Certified Social Media Marketing Professional',
    'Certified TOGAF Professional',
    'Certified Treasury Markets professional',
    'Certified Viral Marketing Professional',
    'Certified Waste Management Professional',
    'Clean Energy Management',
    'Commercial Banking',
    'Commodities Trading',
    'Company Law',
    'Compensation and Benefits Management',
    'Competition Law Analyst',
    'Competitive Marketing Strategies',
    'Consumer Law',
    'Contract Law Analyst',
    'Corporate Law Analyst',
    'Corporate Social Responsibility Professional',
    'Cost Accounting',
    'Cover Letter',
    'Credit Risk Management Training Course',
    'Customer Focus',
    'Customer Service Fundamentals',
    'Cyber Law Analyst',
    'Digital Marketing Master Training Course',
    'Education Verification Service',
    'Education and Experience Verification Service',
    'Electronics Design Associate',
    'Employment Verification Service',
    'Engineering Design',
    'English Language Course',
    'English for Interview Skills',
    'Englishmate: For a better Career',
    'Environment Law Analyst',
    'Equity Research Analyst',
    'Essential Selling Skills',
    'Executive Program in Valuation and Risk Models',
    'Featured Profile',
    'Fellowship in 2D Echocardiography (Apollo Hospitals)',
    'Finance and Accounting Essentials for Non Financial Professionals',
    'Finance and Accounting Essentials for Non-financial professionals with Getcertgo Certification',
    'Financial Services Marketing Professional',
    'Financial Valuation Analyst',
    'Fitness Trainer',
    'Fitness Trainer - - International',
    'Fixed Income Analyst',
    'Freshers',
    'Frontline Call Center Skills',
    'Fundamentals of Lean for Business Organizations',
    'Fundamentals of Securities and Derivatives',
    'Futures and Options Trading',
    'HR management',
    'Hong Kong',
    'HongKong',
    'Human Rights Law',
    'IFRS',
    'IT Project Management Essentials',
    'Inbound Call Center Management',
    'India',
    'Intellectual Property Rights and Legal Manager',
    'Interior Designer',
    'International Logistics Management',
    'International Logistics Management Professional',
    'International Trade',
    'Inventory Management',
    'Job Interview Coaching by Sarabjeet Sachar',
    'Labour Law Analyst',
    'Leadership Essentials',
    'Lean Manufacturing',
    'Lean Six Sigma Black Belt GC',
    'Lean Six Sigma Green Belt GC',
    'Lean Six sigma Black Belt',
    'Librarian',
    'Lightroom Professional',
    'Logistics & Supply chain management',
    'Management Essentials',
    'Manager of Quality/Organizational Excellence',
    'Manufacturing Technology Management',
    'Marketing Essentials',
    'Masterclass in Advanced Excel for Accounting Wizards',
    'Media Law Analyst',
    'Mid Level Experienced Professional',
    'Middle East',
    'Organization and HR Function',
    'Organizational Behavior',
    'PMI Agile Certified Practitioner ACP',
    'PMI Certified Associate in Project Management CAPM',
    'PMI Project Management Professional PMP',
    'PMP',
    'PRINCE2',
    'Payroll Management',
    'Performance Appraisal Management',
    'Photography Professional',
    'Photoshop Professional',
    'Post Graduate Program in Business Analytics',
    'Practitioners Approach to Digital Marketing',
    'Production Planning and Control',
    'Production and Operations Management',
    'Professional Certificate Program in Business Analytics',
    'Professional in Human Resources',
    'Project Management',
    'Project Management for Non project Managers',
    'Purchase Manager',
    'Purchasing and Material Management',
    'Purchasing and Vendor Management Essentials',
    'Real Estate Consultant',
    'Recruitment and Retention Strategies with GetCertGo Certification',
    'Recruitment and selection/Talent Acquisition management',
    'Restaurant Management',
    'Resume Booster',
    'Resume Critique',
    'SAP Business Objects Business Intelligence',
    'SAP Business Suite 7 for End Users',
    'Sales Foundations',
    'Sales Negotiations',
    'Salesforce',
    'Search Engine Optimisation',
    'Senior Level Experienced Professional',
    'Singapore',
    'Six Sigma Black Belt',
    'Six Sigma Black Belt with GetCertGo Certification',
    'Six Sigma Green Belt',
    'Six Sigma Green Belt GC',
    'Six Sigma Green Belt with GetCertGo Certification',
    'Social Media Certification (CSMMP)',
    'SpamAssasin Professional',
    'Stock Investing',
    'Stocks and Derivatives',
    'Strategic Account Sales Skills',
    'Strategic Brand Management',
    'Strategic Guide Investment Industry and Investor',
    'Supply Chain Management',
    'Talent Acquisition Management',
    'Textile Designer',
    'Thailand',
    'The Voice of Leadership',
    'The role of HR as a Business Partner',
    'Thinking Like a CFO',
    'Total Quality Management',
    'Trademark Law Analyst',
    'Training and development Management',
    'Ultimate Guide to Demand and Supply Analysis',
    'United Kingdom',
    'United States',
    'Video Professional',
    'Vskills Certified Advertising Manager',
    'Vskills Certified Brand Manager',
    'Vskills Certified Business Accountant',
    'Vskills Certified Campaign Manager',
    'Vskills Certified Clean Energy Professional',
    'Vskills Certified Commodity Trader',
    'Vskills Certified Corporate Finance Analyst',
    'Vskills Certified Cost Accountant',
    'Vskills Certified Credit Risk Manager',
    'Vskills Certified Criminal Procedure Code Analyst',
    'Vskills Certified Cyber Law Analyst',
    'Vskills Certified Debt Recovery Agent',
    'Vskills Certified Equity Research Analyst',
    'Vskills Certified Event Management Professional',
    'Vskills Certified Financial Valuation Analyst',
    'Vskills Certified Foreign Exchange Professional',
    'Vskills Certified Futures Trader',
    'Vskills Certified HR Staffing Manager',
    'Vskills Certified Hedge Fund Manager',
    'Vskills Certified Human Resources Manager ',
    'Vskills Certified Marketing Manager',
    'Vskills Certified Merchandiser',
    'Vskills Certified Merger and Acquisition Analyst',
    'Vskills Certified Mutual Funds Advisor',
    'Vskills Certified NGO Manager',
    'Vskills Certified Negotiation Manager',
    'Vskills Certified Options Trader',
    'Vskills Certified Performance Appraisal Manager',
    'Vskills Certified Performance Manager',
    'Vskills Certified Portfolio Manager',
    'Vskills Certified Project Finance Analyst',
    'Vskills Certified Retail Management Professional',
    'Vskills Certified Sales Manager',
    'Vskills Certified Services Marketing Manager',
    'Vskills Certified Telesales Executive',
    'Vskills Certified Treasury Market Professional',
    'Vskills Certified Warehouse Manager',
    'Vskills Certified Wealth Manager',
    'Warehouse Management',
    'Wedding Photography Professional',
    'Workplace Conflict Management'
]