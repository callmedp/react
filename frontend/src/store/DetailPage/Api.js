import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'

const otherProvidersCourses = (data) => {
    // const url = `/api/v1/most-viewed-courses/?category_id=${data.categoryId}`;
    // return BaseApiService.get(`${siteDomain}${url}`);
    return {"message":"Most viewed Courses fetched","data":{"otherProvidersCourses":[{"id":1605,"name":"ITIL Foundation Service Management","about":"The training provided by Skillsoft aims at designing an administration architecture that incorporates IT as well as business necessities. The course helps the candidate to clear the assessment for the ITIL Foundation for IT Service Management certification.","url":"/course/operation-management/itil-foundation-service-management-2/pd-1605","imgUrl":"https://learning-media-staging-189607.storage.googleapis.com/l2/m/product_image/1605/1613453606_8410.png","imgAlt":"ITIL Foundation Service Management","title":"ITIL Foundation Service Management -  (INR 12399) - Shine Learning","slug":"itil-foundation-service-management-2","jobsAvailable":77937,"skillList":["Stock Management","SAP MM - Materials Management","Retailer Management","Resource Management","Material And Inventory Management","Operation Management","Supplier Management","Warehouse Management System","Spares Inventory Management","Logistics Tracking and Management","Sap Material Management","Customer and Supply Chain Management","Supply Management","Spare Vendor Management","Material Management","Store Management","Retail Management","Total Quality Management","Commodity Management","Sap Warehouse Management","Distribution Channel Management","Storage Management","Inventory and Material Management","IT Service Management","Treasury And Risk Management","Treasury Management","Export Management","Fund Management","Sap Data Service","Data Management","Clinical Data Management","Data Centre Management","Systems &  Server Management","Quality Management System","SAP QM - Quality Management","Quality Management","Service Marketing","Professional Management","Sun Server Management","Sap Project Management Module","Construction Project Management","Large Scale Project Management","Project Management","Financial and Management Accounting","JD Edwards - Financial Management","Enterprise Risk Management","Governance  Risk & Compliance Management","Risk Management","Market Risk Management","Workforce Management","Cil Management","Site Management","Coastal Management","Information Technology Management","Event Management","Fuel Management","Cost Management","Customer Life Cycle Management","Property Management and Investments","Disk Management","Cinema Management","Cash Management","Staff Management","Order Management & Tracking","Configuration Management","Enterprise Account Management","Facilities Management","Capacity Management","Line Management","Account Management","Commercial Management","Tender Management","Program Management","Contact Center Management","Revenue Cycle Management","Call Center Management","Budget Management","Cable Management","Management Consulting","Management Science","Transaction Management","Management By Objectives","Availability Management","Payroll Management","Revenue Management","Cient Management","Business Performance Management","Capital Management","Property Management","Chimney Management","Trade Management","Global Management Accounting","Conflict Management","Dependency Management","Time Management","General Management","Rotating Equipment Management","Remote Infrastructure Management","Engineering - Change Management","Meeting Management","Ar Management","Sap Quality Management","Health Safety Management","Service Management","Cooling Tower Management","Management Accounting","Branch Management","Information Management","Rail Management","Mall Management","Sap Spend Performance Management","Campaign Management","Admin Facilities Management","Marine Operations Management","Error Management","Crisis Management","Surgical Wards Management","Active Directory Management","Oncology Brand Management","Dialer Management","Derma Brand Management","MANPOWER MANAGEMENT AND GENERAL DOCUMENTATION","Innovation Management","Database Management","Energy Management","Enterprise Content Management","Strategy Management","Buffer Cache Management","Restaurant Management","It Asset Management","Senior Management","Brand Management","Workflow Management","Infrastructure Management","Vendor Development and Management","Liquidity Management","Sales Management","Bench Management","Interchange Management","Sap Isu And Device Management Or Dm","Supply Chain Management Research","Vehicle Management and Repairs","Software License Management","Investment Management and Strategies","Contract Management","Scope Management","Fraud Management","Process Safety Management","Multi-Channel Campaign Management","Business Process Management","Working Capital Management","Dealer Management","Franchisee Management","Career Management","Disaster Management","Offshore Fund Management","Issue Management","Bid Management","Cash Flow Management","Web Content Management","Field Management","Port Management","Cafeteria Management","Talent Management","Commercial Property Management","Vendor Management","Incident Management","Cruise Liner Management","Enterprise Asset Management","Forex Management","SAP PLM - Product Lifecycle Management","Test Management Tools","Consumable Management","Press Conference Management","Absence Management","Technology Management","Labour Management","Hospital Management","ACD Management","Academic Management","Contractor Management","Action Management","Management Buyouts","Environment Management","Noc Management","Airspace Management","Functional Management","Management Audit","Cargo Management","Trouble Management","Planning Management","Travel Management","Identity And Access Management","Category Management","Conferences Management","Release Management","Franchise Management","Water Management","Engineering Management","Chiller Management","Siebel Order Management","Novell Network Management","Fleet Management","Compensation Management","Safety Management","Management","Celebrity Management","Shift Management","EMS Management","Trouble Ticket Management","Rewards Management","Denial Management","Crew Management","Depot Management","Recovery Management","Liability Management","Human Capital Management","CMO management","JD Edwards - Customer Relationship Management","JD Edwards - Supply Management (Procurement)","Ceridian Payroll Service","Web Hosting Service","Receivable Management","Global Alliance Management","Oracle Order Management","Plant Management","Attrition Management","Customer Service Skills","It Service Delivery","Service Standards","Service Tax","Cabin Service","Service Agreements","Battery Service","Customer Service (Voice)","Service Delivery","E-Mail Hosting Service","Passenger Service","Car Service","Service Assurance","Service Delivery Models","Customer Service","Service Creation","Automobile Service","Field Service","Restaurant Customer Service","Customer Service (Non-Voice)","Service Orientation","Guest Service","Service Test","Foundation","ITIL V3"],"rating":4.5,"stars":["*","*","*","*","+"],"mode":null,"providerName":"skillsoft","price":12399.0,"tags":0,"highlights":["Globally Recognized Online Training Program","Online course Program"],"brochure":null,"u_courses_benefits":null,"u_desc":"<p><strong>ITIL&reg; Foundation Certificate</strong>&nbsp;is a 4 weeks online program provided by&nbsp;<strong>SkillSoft</strong>&nbsp;and is held by an external provider. This globally accepted qualification is the first step towards further advanced ITIL&reg; certification. This course will prepare you in clearing the assessment for the&nbsp;<strong>ITIL Foundation for IT Service Management</strong>&nbsp;certification. You'll need to appear for the exam separately.</p>\n<p>&nbsp;</p>\n<p>Mail to&nbsp;<strong>vinod@shine.com</strong>&nbsp;for a free demo request.</p>","duration":0,"type":"","label":"ITIL Foundation Service Management","level":""}]}}
}

const mainCourses = (id) => {
    const url = `/api/v1/shop/api/v1/get-product/?pid=${id}`;
    return BaseApiService.get(`${siteDomain}${url}`);


    // let data = {
    //     "product":"Lean Six Sigma Green Belt Test",
    //     "num_jobs_url":"https://www.shine.com/job-search/lean-six-sigma-green-belt-test-jobs",
    //     "breadcrumbs":[],
    //     "prd_img":"https://learning-media-staging-189607.storage.googleapis.com/l2/m/product_image/1/1608784815_5352.png",
    //     "prd_img_alt":"Lean Six Sigma Green Belt",
    //     "prd_img_bg":0,
    //     "prd_H1":"Lean Six Sigma Green Belt Test",
    //     "prd_about":"Test GreyCampus offers an online training and certification program on Lean Six Sigma Green Belt. Study with confidence as the course covers every topic in accordance with IASSC. Lean Six Sigma incorporates the most widely-used concepts and tools from both the Lean and Six Sigma bodies of knowledge along with DMAIC problem solving approach.",
    //     "prd_desc":"<ul>\n\t<li>Lean Best suited for candidates who wish to make a successful career in quality function of an organization. management, communication, adaptability, leadership, time management, ruby on rails, react, angular, vue, decision making, communication, mongodb, ruby on rails, decision making, who, six sigma, time management</li>\n</ul>\n\n<p>&nbsp;</p>",
    //     "prd_uget":"<ul>\n\t<li>Test GreyCampus offers an online training and certification program on Lean Six Sigma Green Belt.</li>\n\t<li>Study with confidence as the course covers every topic in accordance with IASSC.</li>\n\t<li>Lean Six Sigma incorporates the most widely-used concepts and tools from both the Lean and Six Sigma bodies of knowledge.</li>\n</ul>",
    //     "prd_rating":4.9,
    //     "prd_num_rating":1133,
    //     "prd_num_bought":20,
    //     "prd_num_jobs":555,
    //     "prd_vendor":"Career Plus",
    //     "prd_vendor_img":"https://learning-media-staging-189607.storage.googleapis.com/l2/m/vendor/1/1609910098_1141.png",
    //     "prd_rating_star":[
    //         "*",
    //         "*",
    //         "*",
    //         "*",
    //         "*"
    //     ],
    //     "prd_video":"www.youtube.com/embed/mWRsgZuwf_8?start=2",
    //     "start_price":500.0,
    //     "prd_service":"course",
    //     "prd_product":1,
    //     "prd_exp":"None",
    //     "chapter":true,
    //     "chapter_list": [
    //         {
    //             "heading":"Introduction to Digital Marketing",
    //             "content":"<p>Learning Objectives - In this module, you will learn about different aspects of Digital Marketing and how they come together in a cohesive and effective Digital Marketing plan.</p>\r\n\r\n<p>Topics - Introduction to Digital Marketing, The 4-Cs of Digital Marketing, Customer Persona, Comparing digital and offline marketing, Introduction to Google Analytics and Webmaster tools, Introduction to sales funnels.</p>\r\n\r\n<p>Handouts Common Ecommerce terminology Customer Persona template</p>",
    //             "ordering":1
    //         },
    //         {
    //             "heading":"SEO - Keyword Planning",
    //             "content":"<p>Learning Objectives - In this module, you will learn about different aspects of Digital Marketing and how they come together in a cohesive and effective Digital Marketing plan.</p>\r\n\r\n<p>Topics - Introduction to Digital Marketing, The 4-Cs of Digital Marketing, Customer Persona, Comparing digital and offline marketing, Introduction to Google Analytics and Webmaster tools, Introduction to sales funnels.</p>\r\n\r\n<p>Handouts Common Ecommerce terminology Customer Persona template</p>",
    //             "ordering":2
    //         }
    //     ],
    //     "faq":true,
    //     "faq_list":[
    //         {
    //             "question":"What do i expect?",
    //             "answer":"<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam egestas velit in tempus viverra. Ut sed lacus quis nulla sagittis vehicula. Nunc nec sollicitudin sapien, non iaculis nunc. Mauris luctus eleifend pellentesque. Pellentesque a ipsum nec mauris auctor iaculis. Pellentesque iaculis non odio a pharetra. Nulla facilisi. In hac habitasse platea dictumst. Donec consequat lobortis nisl et vehicula.</p>"
    //         },
    //         {
    //             "question":"What is Resume Writing?",
    //             "answer":"<p>Resume writing service gives you a high impact resume that highlights your strengths and achievements. We have resume writing experts who have extensive resume writing experience and have written almost 10,000 resumes.</p>\r\n\r\n<p>Resume writing for different levels:</p>\r\n\r\n<ol>\r\n\t<li>Fresher</li>\r\n\t<li>Junior (1-3 year)</li>\r\n\t<li>Middle (4-7 year)</li>\r\n\t<li>Senior (8-14 year)</li>\r\n\t<li>Top (15+ year)</li>\r\n</ol>"
    //         }
    //     ],
    //     "country_choices":[],
    //     "initial_country":"91",
    //     "pop":true,
    //     "pop_list":[
    //         {
    //             "id":6478,
    //             "label":"Test course",
    //             "heading":"Test course",
    //             "vendor":"analytics vidhya",
    //             "vendor_image":"None",
    //             "url":"/course/courses-certifications/test-course-3/pd-6478",
    //             "inr_price":1021.0,
    //             "fake_inr_price":0.0,
    //             "usd_price":19.0,
    //             "fake_usd_price":0.0,
    //             "aed_price":61.0,
    //             "fake_aed_price":0.0,
    //             "gbp_price":14.0,
    //             "fake_gbp_price":0.0,
    //             "short_description":"None"    
    //         },
    //         {
    //             "id":2714,
    //             "label":"Test University Course",
    //             "heading":"university course46",
    //             "vendor":"ops",
    //             "vendor_image":"None",
    //             "url":"/course/courses-certifications/test-university-course/pd-2714",
    //             "inr_price":700.0,
    //             "fake_inr_price":0.0,
    //             "usd_price":13.0,
    //             "fake_usd_price":0.0,
    //             "aed_price":42.0,
    //             "fake_aed_price":0.0,
    //             "gbp_price":10.0,
    //             "fake_gbp_price":0.0,
    //             "short_description":"None"    
    //         },
    //         {
    //             "id":25,
    //             "label":"Job Service5",
    //             "heading":"Job Service5",
    //             "vendor":"VSkill",
    //             "vendor_image":"https://learning-media-staging-189607.storage.googleapis.com/l2/m/vendor/2/1609910163_5388.png",
    //             "url":"/course/courses-certifications/job-service5/pd-25",
    //             "inr_price":0.0,
    //             "fake_inr_price":0.0,
    //             "usd_price":0.0,
    //             "fake_usd_price":0.0,
    //             "aed_price":0.0,
    //             "fake_aed_price":0.0,
    //             "gbp_price":0.0,
    //             "fake_gbp_price":0.0,
    //             "short_description":"None"    
    //         },
    //         {
    //             "id":22,
    //             "label":"Job Service2",
    //             "heading":"Job Service2",
    //             "vendor":"VSkill",
    //             "vendor_image":"https://learning-media-staging-189607.storage.googleapis.com/l2/m/vendor/2/1609910163_5388.png",
    //             "url":"/course/courses-certifications/job-service2/pd-22",
    //             "inr_price":0.0,
    //             "fake_inr_price":0.0,
    //             "usd_price":0.0,
    //             "fake_usd_price":0.0,
    //             "aed_price":0.0,
    //             "fake_aed_price":0.0,
    //             "gbp_price":0.0,
    //             "fake_gbp_price":0.0,
    //             "short_description":"None"    
    //         },
    //         {
    //             "id":1921,
    //             "label":"Certified ERP Manager",
    //             "heading":"Certified ERP Manager - Certification Course",
    //             "vendor":"Vskills",
    //             "vendor_image":"https://learning-media-staging-189607.storage.googleapis.com/l2/m/vendor/15/1609910067_2290.png",
    //             "url":"/course/courses-certifications/certified-erp-manager-2/pd-1921",
    //             "inr_price":7800.0,
    //             "fake_inr_price":0.0,
    //             "usd_price":143.0,
    //             "fake_usd_price":0.0,
    //             "aed_price":468.0,
    //             "fake_aed_price":0.0,
    //             "gbp_price":110.0,
    //             "fake_gbp_price":0.0,
    //             "short_description":"None"    
    //         }
    //     ],
    //     "selected_var": {
    //         "id":2,
    //         "label":"Six Sigma Black Belt",
    //         "mode":"OL",
    //         "duration":"D0",
    //         "dur_days":45,
    //         "type":"BS",
    //         "level":"BG",
    //         "certify":0,
    //         "inrp":"1",
    //         "aedp":"1",
    //         "usdp":"1",
    //         "gbpp":"1",
    //         "inr_price":100.0,
    //         "fake_inr_price":500.0,
    //         "usd_price":2.0,
    //         "fake_usd_price":0.0,
    //         "aed_price":6.0,
    //         "fake_aed_price":0.0,
    //         "gbp_price":1.0,
    //         "fake_gbp_price":0.0
    //     },
    //     "variation":true,
    //     "var_list":[
    //         {
    //             "id":2,
    //             "label":"Six Sigma Black Belt",
    //             "mode":"OL",
    //             "duration":"D0",
    //             "dur_days":45,
    //             "type":"BS",
    //             "level":"BG",
    //             "certify":0,
    //             "inrp":"1",
    //             "aedp":"1",
    //             "usdp":"1",
    //             "gbpp":"1",
    //             "inr_price":100.0,
    //             "fake_inr_price":500.0,
    //             "usd_price":2.0,
    //             "fake_usd_price":0.0,
    //             "aed_price":6.0,
    //             "fake_aed_price":0.0,
    //             "gbp_price":1.0,
    //             "fake_gbp_price":0.0    
    //         },
    //         {
    //             "id":3,
    //             "label":"course 3",
    //             "mode":"CA",
    //             "duration":"D1",
    //             "dur_days":100,
    //             "type":"BD",
    //             "level":"AD",
    //             "certify":0,
    //             "inrp":"1",
    //             "aedp":"2",
    //             "usdp":"2",
    //             "gbpp":"2",
    //             "inr_price":1500.0,
    //             "fake_inr_price":0.0,
    //             "usd_price":28.0,
    //             "fake_usd_price":0.0,
    //             "aed_price":90.0,
    //             "fake_aed_price":0.0,
    //             "gbp_price":21.0,
    //             "fake_gbp_price":0.0    
    //         }
    //     ],
    //     "canonical_url":"/courses/banking-and-finance/certitications-and-assesment/84/",
    //     "fbt":true,
    //     "fbt_list":[
    //         {
    //             "id":83,
    //             "label":"Cover Letter",
    //             "heading":"Cover Letter",
    //             "country":"",
    //             "experience":"",
    //             "inr_price":599.0,
    //             "fake_inr_price":0.0,
    //             "usd_price":11.0,
    //             "fake_usd_price":0.0,
    //             "aed_price":36.0,
    //             "fake_aed_price":0.0,
    //             "gbp_price":8.0,
    //             "fake_gbp_price":0.0,
    //             "short_description":"None",
    //             "visible_on_crm":true,
    //             "image":"https://learning-media-staging-189607.storage.googleapis.com/l2/m/product_image/83/1609995525_223.png"    
    //         },
    //         {
    //             "id":56,
    //             "label":"Second regular resume",
    //             "heading":"Second regular resume",
    //             "country":"",
    //             "experience":"FR",
    //             "inr_price":599.0,
    //             "fake_inr_price":0.0,
    //             "usd_price":11.0,
    //             "fake_usd_price":0.0,
    //             "aed_price":36.0,
    //             "fake_aed_price":0.0,
    //             "gbp_price":8.0,
    //             "fake_gbp_price":0.0,
    //             "short_description":"None",
    //             "visible_on_crm":true,
    //             "image":"https://learning-media-staging-189607.storage.googleapis.com/l2/m/product_image/56/1501150029_6389.png"
    
    //         }
    //     ],
    //     "domain_name":"http//127.0.0.1:8000",
    //     "prd_vendor_slug":"career-plus",
    //     "get_fakeprice":"None",
    //     "show_chat":true,
    //     "prd_vendor_count":136,
    //     "selected_products":[],
    //     "prd_rv_total":19,
    //     "prd_rv_page":1,
    //     "widget_objs":"None",
    //     "widget_obj":"None",
    //     "is_logged_in":false,
    //     "linkedin_resume_services": [
    //         2684,
    //         2685,
    //         2682,
    //         2683
    //     ],
    //     "redeem_test":false,
    //     "product_redeem_count":0,
    //     "redeem_option":"assessment",
    //     "navigation":true
    // }

    // return data;
}

export default {
    mainCourses,
    otherProvidersCourses,
}   

