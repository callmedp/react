import { resumeShineSiteDomain, siteDomain } from './domains';


const freeResourcesList = [
    { 
        name: 'Resume Formats', 
        url: `${resumeShineSiteDomain}/cms/resume-format/1/`, 
        id: 'resume_formats',
        sideNavType: 'freeResources',
        children: [
            { name: 'Freshers', url: `${resumeShineSiteDomain}/cms/resume-format/freshers-2/2/`, id:'freshers' },
            { name: 'Banking Freshers', url: `${resumeShineSiteDomain}/cms/resume-format/banking-freshers/4/`, id:'banking_freshers' },
            { name: 'Experienced Professional', url: `${resumeShineSiteDomain}/cms/resume-format/experienced-professionals/6/`, id:'experienced_professionals' },
            { name: 'Engineers', url: `${resumeShineSiteDomain}/cms/resume-format/engineers-2/20/`, id:'engineers' },
            { name: 'IT', url: `${resumeShineSiteDomain}/cms/resume-format/it/53/`, id:'it'},
            { name: 'View all', url:`${resumeShineSiteDomain}/cms/resume-format/1/`, id:'view_all'},
        ]
    },
    {
        name: 'Resignation Letter Formats',
        url: `${resumeShineSiteDomain}/cms/resignation-letter-formats-samples/3/`, 
        id:'resignation_formats',
        sideNavType: 'freeResources',
        children:[
            { name: 'With Notice Period', url: `${resumeShineSiteDomain}/cms/resignation-letter-formats-samples/notice-period/5/`, id:'with_notice_period' },
            { name: 'Personal Reasons', url: `${resumeShineSiteDomain}/cms/resignation-letter-formats-samples/personal-reasons/15/`, id:'personal_reasons' },
            { name: 'Higher Studies', url: `${resumeShineSiteDomain}/cms/resignation-letter-formats-samples/higher-studies-or-going-abroad/49/`, id:'higher_studies' },
            { name: 'Without Notice Period', url: `${resumeShineSiteDomain}/cms/resignation-letter-formats-samples/without-notice-period/17/`, id:'without_notice_period' },
            { name: 'Family Illness', url: `${resumeShineSiteDomain}/cms/resignation-letter-formats-samples/family-illness/18/`, id:'family_illness'},
            { name: 'View all', url:`${resumeShineSiteDomain}/cms/resignation-letter-formats-samples/3/`, id:'view_all'}
        ]
    },
    { 
        name: 'Cover Letter Formats', 
        url: `${resumeShineSiteDomain}/cms/cover-letter-format/7/`, 
        id: 'cover_letter',
        sideNavType: 'freeResources',
        children: [
            { name: 'Freshers', url: `${resumeShineSiteDomain}/cms/cover-letter-format/freshers/8/`, id:'freshers' },
            { name: 'Engineers', url: `${resumeShineSiteDomain}/cms/cover-letter-format/engineers/9/`, id:'engineers' },
            { name: 'View all', url:`${resumeShineSiteDomain}/cms/cover-letter-format/7/`, id:'view_all'}
        ]
    },
    { 
        name: 'Resume Templates', 
        url: `${resumeShineSiteDomain}/cms/resume-samples-and-templates/50/`, 
        id: 'resume_templates',
        sideNavType: 'freeResources',
        children: [
            { name: 'Pharma', url: `${resumeShineSiteDomain}/cms/resume-samples-and-templates/pharma/34/`, id:'pharma' },
            { name: 'Freshers', url: `${resumeShineSiteDomain}/cms/resume-samples-and-templates/freshers-3/55/`, id:'freshers' },
            { name: 'View all', url:`${resumeShineSiteDomain}/cms/resume-samples-and-templates/50/`, id:'view_all'}
        ]
    }, 
    { 
        name: 'LinkedIn Summary Example', 
        url:`${resumeShineSiteDomain}/cms/linkedin-summary-examples/43/`, 
        id: 'linkedin_summary',
        sideNavType: 'freeResources',
        children: [
            { name: 'HR Professionals', url: `${resumeShineSiteDomain}/cms/linkedin-summary-examples/hr-professional/36/`, id:'hr_professional' },
            { name: 'View all', url:`${resumeShineSiteDomain}/cms/linkedin-summary-examples/43/`, id:'view_all'}
        ]
    },
    { 
        name: 'Relieving Letter', 
        url:`${resumeShineSiteDomain}/cms/relieving-letter-format/58/`, 
        id: 'relieving_letter',
        sideNavType: 'freeResources',
        children: []
    },
]
 

const jobAssistanceList = [
    { name: 'Resume Writing', url: `${resumeShineSiteDomain}`, id: 'resume_writing'},
    { name: 'International Resume', url: `${resumeShineSiteDomain}/product/entry-level-freshers-4/2553/`, id: 'international_resume' },
    { name: 'Visual Resume', url: `${resumeShineSiteDomain}/product/entry-level-freshers/2052/`, id: 'visual_resume' },
    { name: 'Jobs On The Move',  url: `${resumeShineSiteDomain}/product/jobs-on-the-move-3/3411/`, id: 'jobs_move' },
    { name: 'LinkedIn Profile', url: `${resumeShineSiteDomain}/product/linkedin-profile-writing/fresher-level/1925/`, id: 'linkedin_profile' },
    { name: 'Featured Profile', url: `${resumeShineSiteDomain}/product/featured-profile-10/1939/`, id: 'featured_profile' },
    { name: 'Application Highlighter', url: `${resumeShineSiteDomain}/product/application-highlighter-3/4117/`, id: 'application_highlighter' },
    { name: 'Resume Score Checker', url: `${resumeShineSiteDomain}/resume-score-checker/`, id: 'score_checker' },
]

const categoryList = [
    { 
        name: 'Sales And Marketing', 
        url: `${siteDomain}/courses/sales-and-marketing/17/`, 
        id: 'sales_marketing',
        sideNavType: 'allCourses',
        children: [
            { name: 'Digital Marketing', url: `/courses/sales-and-marketing/digital-marketing/32/`, id:'digital_marketing', sideNavType: 'courses' },
            { name: 'Sales', url: `/courses/sales-and-marketing/sales/18/`, id:'sales', sideNavType: 'courses' },
            { name: 'Retail', url: `/courses/sales-and-marketing/retail/35/`, id:'retail', sideNavType: 'courses' },
            { name: 'Product Management', url: `/courses/sales-and-marketing/product-marketing/24/`, id:'product_management', sideNavType: 'courses' },
            { name: 'Service Management', url: `/courses/sales-and-marketing/service-marketing/30/`, id:'service_management', sideNavType: 'courses'},
        ]
    },
    {
        name: 'Operation Management',
        url: `${siteDomain}/courses/operation-management/19/`,
        id:'operation_management',
        sideNavType: 'allCourses',
        children:[
            { name: 'Six Sigma', url: `/courses/operation-management/six-sigma/193/`, id:'six_sigma', sideNavType: 'courses' },
            { name: 'Project Management', url: `/courses/operation-management/project-management/123/`, id:'project_management', sideNavType: 'courses' },
            { name: 'Logistic and Supply Chain', url: `/courses/operation-management/logistics-and-supply-chain/135/`, id:'logistic_and_supply_chain', sideNavType: 'courses' },
            { name: 'Service Quality', url: `/courses/operation-management/service-quality/316/`, id:'service_quality', sideNavType: 'courses' },
            { name: 'Production', url: `/courses/operation-management/production/39/`, id:'production', sideNavType: 'courses'},
            { name: 'Customer Care', url:`/courses/operation-management/customer-care/37/`, id:'customer_care', sideNavType: 'courses'}
        ]
    },
    { 
        name: 'Banking & Finance', 
        url: `${siteDomain}/courses/banking-and-finance/20/`,
        id: 'banking_finance',
        sideNavType: 'allCourses',
        children: [
            { name: 'Advanced Accounting', url: `/courses/banking-finance/advanced-accounting/114/`, id:'advanced_accounting', sideNavType: 'courses'},
            { name: 'Banking', url: `/courses/banking-finance/banking/113/`, id:'banking', sideNavType: 'courses' },
            { name: 'Risk Management', url:`/courses/banking-finance/risk-management/95/`, id:'risk_management', sideNavType: 'courses'},
            { name: 'Stock Market Training', url: `/courses/banking-finance/stock-trading/94/`, id:'stock_market_training', sideNavType: 'courses' },
            { name: 'Financial Resporting and Management', url: `/courses/banking-finance/financial-reporting-and-management/103/`, id:'financial_reporting_and_management', sideNavType: 'courses' },
            { name: 'Commercial Operation', url:`/courses/banking-finance/commercial-operation/112/`, id:'commercial_operation', sideNavType: 'courses'},
            { name: 'Investment Banking', url:`/courses/banking-finance/investment-banking/100/`, id:'investment_banking', sideNavType: 'courses'},
            { name: 'GST', url: `/courses/banking-finance/gst-2/507/`, id:'gst', sideNavType: 'courses' },
        ]
    },
    { 
        name: 'Information Technology', 
        url: `${siteDomain}/courses/it-information-technology/22/`, 
        id: 'informaton_technology',
        sideNavType: 'allCourses',
        children: [
            { name: 'Big Data', url: `/courses/it-information-technology/big-data/84/`, id:'big_data', sideNavType: 'courses' },
            { name: 'Project Management', url: `/courses/operation-management/project-management/123/`, id:'project_management', sideNavType: 'courses' },
            { name: 'IT Software', url:`/courses/it-information-technology/it-software/53/`, id:'it_software', sideNavType: 'courses'},
            { name: 'Graphic Design', url: `/courses/it-information-technology/graphic-design/54/`, id:'graphic_design', sideNavType: 'courses' },
            { name: 'Cloud Computing', url: `/courses/it-information-technology/cloud-computing/82/`, id:'cloud_computing', sideNavType: 'courses' },
            { name: 'MS Skills', url:`/courses/it-information-technology/ms-skills/98/`, id:'ms_skills', sideNavType: 'courses'},
            { name: 'IT Language', url: `/courses/it-information-technology/it-language/80/`, id:'it_language', sideNavType: 'courses' },
            { name: 'Blockchain', url: `/courses/it-information-technology/blockchain/496/`, id:'blockchain', sideNavType: 'courses' },
            { name: 'Data Science', url:`/courses/it-information-technology/data-science/497/`, id:'data_science', sideNavType: 'courses'}
        ]
    }, 
    { 
        name: 'Human Resources', 
        url:`${siteDomain}/courses/hr-human-resource/25/`, 
        id: 'human_resources',
        sideNavType: 'allCourses',
        children: [
            { name: 'Talent Aquisition', url: `/courses/hr-human-resource/talent-acquisition/93/`, id:'talent_acquisition', sideNavType: 'courses' },
            { name: 'Organisational Structure', url:`/courses/hr-human-resource/organizational-structure/97/`, id:'organisational_structure', sideNavType: 'courses'},
            { name: 'Training & Development', url: `/courses/hr-human-resource/training-and-development/91/`, id:'training_and_development', sideNavType: 'courses' },
            { name: 'Compensation', url:`/courses/hr-human-resource/compensation-2/110/`, id:'compensation', sideNavType: 'courses'}
        ]
    },
    { 
        name: 'Management', 
        url:`${siteDomain}/courses/management/27/`, 
        id: 'management',
        sideNavType: 'allCourses',
        children: [
            { name: 'General Management', url: `/courses/management/general-management/102/`, id:'general_management', sideNavType: 'courses' },
            { name: 'Business Analyst', url: `/courses/management/business-analyst/58/`, id:'business_analyst', sideNavType: 'courses' },
            { name: 'Corporate Governance', url:`/courses/management/corporate-governance/59/`, id:'corporate_governance', sideNavType: 'courses'},
        ]
    },
    { 
        name: 'Mass Communication', 
        url: `${siteDomain}/courses/mass-communication/29/`, 
        id: 'mass_communication',
        sideNavType: 'allCourses',
        children: [
            { name: 'Content', url: `/courses/mass-communication/content/46/`, id:'content', sideNavType: 'courses' },
            { name: 'Public Relations', url: `/courses/mass-communication/public-relations/96/`, id:'public_relations', sideNavType: 'courses' },
            { name: 'Editor', url:`/courses/mass-communication/editor/106/`, id:'editor', sideNavType: 'courses'},
            { name: 'journalism', url:`/courses/mass-communication/journalism/99/`, id:'journalism', sideNavType: 'courses'}
        ]
    },
    { 
        name: 'Personal Development', 
        url: `${siteDomain}/courses/personal-development/21/`, 
        id: 'personal_development',
        sideNavType: 'allCourses',
        children: [
            { name: 'Language Learning', url: `/courses/personal-development/language-learning/40/`, id:'language_learning', sideNavType: 'courses' },
            { name: 'Leadership', url: `/courses/personal-development/leadership/41/`, id:'leadership', sideNavType: 'courses' },
            { name: 'Personal Development', url:`/courses/personal-development/personality-development/42/`, id:'personality_development', sideNavType: 'courses'},
            { name: 'Interview Preparation', url:`/courses/personal-development/interview-preparation/38/`, id:'interview_preparation', sideNavType: 'courses'},
            { name: 'Communication Development', url:`/courses/personal-development/communication-development/36/`,id:'communication_development', sideNavType: 'courses'}
        ]
    },
    { 
        name: 'Law', 
        url: `${siteDomain}/courses/law/23/`,
        id: 'law',
        sideNavType: 'allCourses',
        children: [
            { name: 'Cyber Law', url: `/courses/law/cyber-law/107/`, id:'cyber_law', sideNavType: 'courses' },
            { name: 'Criminal Law', url: `/courses/law/criminal-law/108/`, id:'criminal_law', sideNavType: 'courses' },
            { name: 'Company Law', url:`/courses/law/company-law/111/`, id:'company_law', sideNavType: 'courses'}
        ]
    },
    { 
        name: 'Course Catalogue', 
        url: `${siteDomain}/online-courses.html`, 
        id: 'course_catalogue',
        sideNavType: 'allCourses',
        children: []
    },
]


const navSkillList = [
    { name : 'Digital Marketing', url: '/courses/sales-and-marketing/digital-marketing/32/', id:'digital_marketing' },
    { name: 'Six Sigma', url: '/courses/operation-management/six-sigma/193/', id:'six_sigma' },
    { name: 'Project Management', url: '/courses/operation-management/project-management/123/', id:'project_management'},
    { name: 'Big Data', url: '/courses/it-information-technology/big-data/84/', id:'big_data'},
    { name: 'IT Software', url: '/courses/it-information-technology/it-software/53/', id:'it_software' },
    { name: 'Data Science', url: '/courses/it-information-technology/data-science/497/', id:'data_science' },
    { name: 'Cloud Computing', url: '/courses/it-information-technology/cloud-computing/82/', id:'cloud_computing'}
]

const contactData = {
    'contactNo' : '08047105151',
    'contactEmail' : 'resume@shine.com',
    'contactTimings' : '9:00am to 6:30pm (Mon - Sat)',
}



export {
    freeResourcesList,
    jobAssistanceList,
    categoryList,
    navSkillList,
    contactData
}