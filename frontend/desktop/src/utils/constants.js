import { resumeShineSiteDomain, siteDomain } from './domains';

const freeResourcesList = [
    { 
        name: 'Resume Formats', 
        url: `${resumeShineSiteDomain}/cms/resume-format/1/`, 
        id: 'resume_formats',
        sideNavType: 'freeResources',
        children: [
            { name: 'Freshers', url: `${resumeShineSiteDomain}/cms/resume-format/freshers-2/2/` },
            { name: 'Banking Freshers', url: `${resumeShineSiteDomain}/cms/resume-format/banking-freshers/4/` },
            { name: 'Experienced Professional', url: `${resumeShineSiteDomain}/cms/resume-format/experienced-professionals/6/` },
            { name: 'Engineers', url: `${resumeShineSiteDomain}/cms/resume-format/engineers-2/20/` },
            { name: 'IT', url: `${resumeShineSiteDomain}/cms/resume-format/it/53/`},
            { name: 'View all', url:`${resumeShineSiteDomain}/cms/resume-format/1/`},
        ]
    },
    {
        name: 'Resignation Letter Formats',
        url: `${resumeShineSiteDomain}/cms/resignation-letter-formats-samples/3/`, 
        id:'resignation_formats',
        sideNavType: 'freeResources',
        children:[
            { name: 'With Notice Period', url: `${resumeShineSiteDomain}/cms/resignation-letter-formats-samples/notice-period/5/` },
            { name: 'Personal Reasons', url: `${resumeShineSiteDomain}/cms/resignation-letter-formats-samples/personal-reasons/15/` },
            { name: 'Higher Studies', url: `${resumeShineSiteDomain}/cms/resignation-letter-formats-samples/higher-studies-or-going-abroad/49/` },
            { name: 'Without Notice Period', url: `${resumeShineSiteDomain}/cms/resignation-letter-formats-samples/without-notice-period/17/` },
            { name: 'Family Illness', url: `${resumeShineSiteDomain}/cms/resignation-letter-formats-samples/family-illness/18/`},
            { name: 'View all', url:`${resumeShineSiteDomain}/cms/resignation-letter-formats-samples/3/`}
        ]
    },
    { 
        name: 'Cover Letter Formats', 
        url: `${resumeShineSiteDomain}/cms/cover-letter-format/7/`, 
        id: 'cover_letter',
        sideNavType: 'freeResources',
        children: [
            { name: 'Freshers', url: `${resumeShineSiteDomain}/cms/cover-letter-format/freshers/8/` },
            { name: 'Engineers', url: `${resumeShineSiteDomain}/cms/cover-letter-format/engineers/9/` },
            { name: 'View all', url:`${resumeShineSiteDomain}/cms/cover-letter-format/7/`}
        ]
    },
    { 
        name: 'Resume Templates', 
        url: `${resumeShineSiteDomain}/cms/resume-samples-and-templates/50/`, 
        id: 'resume_templates',
        sideNavType: 'freeResources',
        children: [
            { name: 'Pharma', url: `${resumeShineSiteDomain}/cms/resume-samples-and-templates/pharma/34/` },
            { name: 'Freshers', url: `${resumeShineSiteDomain}/cms/resume-samples-and-templates/freshers-3/55/` },
            { name: 'View all', url:`${resumeShineSiteDomain}/cms/resume-samples-and-templates/50/`}
        ]
    }, 
    { 
        name: 'LinkedIn Summary Example', 
        url:`${resumeShineSiteDomain}/cms/linkedin-summary-examples/43/`, 
        id: 'linkedin_summary',
        sideNavType: 'freeResources',
        children: [
            { name: 'HR Professionals', url: `${resumeShineSiteDomain}/cms/linkedin-summary-examples/hr-professional/36/` },
            { name: 'View all', url:`${resumeShineSiteDomain}/cms/linkedin-summary-examples/43/`}
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
            { name: 'Digital Marketing', url: `${siteDomain}/courses/sales-and-marketing/digital-marketing/32/` },
            { name: 'Sales', url: `${siteDomain}/courses/sales-and-marketing/sales/18/` },
            { name: 'Retail', url: `${siteDomain}/courses/sales-and-marketing/retail/35/` },
            { name: 'Product Management', url: `${siteDomain}/courses/sales-and-marketing/product-marketing/24/` },
            { name: 'Service Management', url: `${siteDomain}/courses/sales-and-marketing/service-marketing/30/`},
        ]
    },
    {
        name: 'Operation Management',
        url: `${siteDomain}/courses/operation-management/19/`, 
        id:'operation_management',
        sideNavType: 'allCourses',
        children:[
            { name: 'Six Sigma', url: `${siteDomain}/courses/operation-management/six-sigma/193/` },
            { name: 'Project Management', url: `${siteDomain}/courses/operation-management/project-management/123/` },
            { name: 'Logistic and Supply Chain', url: `${siteDomain}/courses/operation-management/logistics-and-supply-chain/135/` },
            { name: 'Service Quality', url: `${siteDomain}/courses/operation-management/service-quality/316/` },
            { name: 'Production', url: `${siteDomain}/courses/operation-management/production/39/`},
            { name: 'Customer Care', url:`${siteDomain}/courses/operation-management/customer-care/37/`}
        ]
    },
    { 
        name: 'Banking & Finance', 
        url: `${siteDomain}/courses/banking-and-finance/20/`, 
        id: 'banking_finance',
        sideNavType: 'allCourses',
        children: [
            { name: 'Advanced Accounting', url: `${siteDomain}/courses/banking-finance/advanced-accounting/114/` },
            { name: 'Banking', url: `${siteDomain}/courses/banking-finance/banking/113/` },
            { name: 'Risk Management', url:`${siteDomain}/courses/banking-finance/risk-management/95/`},
            { name: 'Stock Market Training', url: `${siteDomain}/courses/banking-finance/stock-trading/94/` },
            { name: 'Financial Resporting and Management', url: `${siteDomain}/courses/banking-finance/financial-reporting-and-management/103/` },
            { name: 'Commercial Operation', url:`${siteDomain}/courses/banking-finance/commercial-operation/112/`},
            { name: 'Investment Banking', url:`${siteDomain}/courses/banking-finance/investment-banking/100/`},
            { name: 'GST', url: `${siteDomain}/courses/banking-finance/gst-2/507/` },
        ]
    },
    { 
        name: 'Information Technology', 
        url: `${siteDomain}/courses/it-information-technology/22/`, 
        id: 'informaton_technology',
        sideNavType: 'allCourses',
        children: [
            { name: 'Big Data', url: `${siteDomain}/courses/it-information-technology/big-data/84/` },
            { name: 'Project Management', url: `${siteDomain}/courses/operation-management/project-management/123/` },
            { name: 'IT Software', url:`${siteDomain}/courses/it-information-technology/it-software/53/`},
            { name: 'Graphic Design', url: `${siteDomain}/courses/it-information-technology/graphic-design/54/` },
            { name: 'Cloud Computing', url: `${siteDomain}/courses/it-information-technology/cloud-computing/82/` },
            { name: 'MS Skills', url:`${siteDomain}/courses/it-information-technology/ms-skills/98/`},
            { name: 'IT Language', url: `${siteDomain}/courses/it-information-technology/it-language/80/` },
            { name: 'Blockchain', url: `${siteDomain}/courses/it-information-technology/blockchain/496/` },
            { name: 'Data Science', url:`${siteDomain}/courses/it-information-technology/data-science/497/`}
        ]
    }, 
    { 
        name: 'Human Resources', 
        url:`${siteDomain}/courses/hr-human-resource/25/`, 
        id: 'human_resources',
        sideNavType: 'allCourses',
        children: [
            { name: 'Talent Aquisition', url: `${siteDomain}/courses/hr-human-resource/talent-acquisition/93/` },
            { name: 'Organisational Structure', url:`${siteDomain}/courses/hr-human-resource/organizational-structure/97/`},
            { name: 'Training & Development', url: `${siteDomain}/courses/hr-human-resource/training-and-development/91/` },
            { name: 'Compensation', url:`${siteDomain}/courses/hr-human-resource/compensation-2/110/`}
        ]
    },
    { 
        name: 'Management', 
        url:`${siteDomain}/courses/management/27/`, 
        id: 'management',
        sideNavType: 'allCourses',
        children: [
            { name: 'General Management', url: `${siteDomain}/courses/management/general-management/102/` },
            { name: 'Business Analyst', url: `${siteDomain}/courses/management/business-analyst/58/` },
            { name: 'Corporate Governance', url:`${siteDomain}/courses/management/corporate-governance/59/`},
        ]
    },
    { 
        name: 'Mass Communication', 
        url: `${siteDomain}/courses/mass-communication/29/`, 
        id: 'mass_communication',
        sideNavType: 'allCourses',
        children: [
            { name: 'Content', url: `${siteDomain}/courses/mass-communication/content/46/` },
            { name: 'Public Relations', url: `${siteDomain}/courses/mass-communication/public-relations/96/` },
            { name: 'Editor', url:`${siteDomain}/courses/mass-communication/editor/106/`},
            { name: 'journalism', url:`${siteDomain}/courses/mass-communication/journalism/99/`}
        ]
    },
    { 
        name: 'Personal Development', 
        url: `${siteDomain}/courses/personal-development/21/`, 
        id: 'personal_development',
        sideNavType: 'allCourses',
        children: [
            { name: 'Language Learning', url: `${siteDomain}/courses/personal-development/language-learning/40/` },
            { name: 'Leadership', url: `${siteDomain}/courses/personal-development/leadership/41/` },
            { name: 'Personal Development', url:`${siteDomain}/courses/personal-development/personality-development/42/`},
            { name: 'Interview Preparation', url:`${siteDomain}/courses/personal-development/interview-preparation/38/`},
            { name: 'Communication Development', url:`${siteDomain}/courses/personal-development/communication-development/36/`}
        ]
    },
    { 
        name: 'Law', 
        url: `${siteDomain}/courses/law/23/`, 
        id: 'law',
        sideNavType: 'allCourses',
        children: [
            { name: 'Cyber Law', url: `${siteDomain}/courses/law/cyber-law/107/` },
            { name: 'Criminal Law', url: `${siteDomain}/courses/law/criminal-law/108/` },
            { name: 'Company Law', url:`${siteDomain}/courses/law/company-law/111/`}
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
    { name : 'Digital Marketing', url: '/courses/sales-and-marketing/digital-marketing/32/' },
    { name: 'Six Sigma', url: '/courses/operation-management/six-sigma/193/' },
    { name: 'Project Management', url: '/courses/operation-management/project-management/123/' },
    { name: 'Big Data', url: '/courses/it-information-technology/big-data/84/'},
    { name: 'IT Software', url: '/courses/it-information-technology/it-software/53/' },
    { name: 'Data Science', url: '/courses/it-information-technology/data-science/497/' },
    { name: 'Cloud Computing', url: '/courses/it-information-technology/cloud-computing/82/'}
] 

export {
    freeResourcesList,
    jobAssistanceList,
    categoryList,
    navSkillList
}