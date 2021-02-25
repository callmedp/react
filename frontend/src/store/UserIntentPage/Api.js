import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'

const userIntentData = (data) => {
    const url = `/api/v1/user-intent/?${data.data.type}`
    
    return BaseApiService.post(`${siteDomain}${url}`, data);
}

const fetchServiceRecommendation = (data) => {

    const url = '/intent/api/v1/service-recommendation/'

    if(data?.candidate_id != false){
        const candidate_id = data?.candidate_id;
        url = url + '?candidate_id=' + candidate_id
    }

    return BaseApiService.get(`${siteDomain}${url}`);
}

const uploadFileUrlAPI = (data) => {
    const url = 'api/resume-score-checker/get-score';

    return BaseApiService.post(`${siteDomain}/${url}`, data,
        {}, true);

};

const careerChangeData = () => {
    const url = `/intent/api/v1/course-recommendation/`
    // return BaseApiService.get(`${siteDomain}${url}`);
    return {
        "message": "recommended courses fetched",
        "data": {
            "course_data": [
                {
                    "id": 1568,
                    "name": "Designing BI Solutions with MS SQL Server 2012 Online Training",
                    "about": null,
                    "url": "/course/operation-management/designing-bi-solutions-with-ms-sql-server-2012-online-training/pd-1568",
                    "imgUrl": "https://learning-media-staging-189607.storage.googleapis.com/l1/m/attachment/default_product_image.jpg",
                    "imgAlt": "Designing BI Solutions with MS SQL Server 2012 Online Training",
                    "title": "Designing BI Solutions with MS SQL Server 2012 Online Training -  (INR 5562) - Shine Learning",
                    "slug": "designing-bi-solutions-with-ms-sql-server-2012-online-training",
                    "jobsAvailable": 32959,
                    "skillList": null,
                    "rating": 4.5,
                    "stars": [
                        "*",
                        "*",
                        "*",
                        "*",
                        "+"
                    ],
                    "mode": null,
                    "providerName": "simplilearn",
                    "price": 5561.82,
                    "tags": 0,
                    "highlights": null,
                    "brochure": null,
                    "u_courses_benefits": null,
                    "u_desc": "<p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify;\"><span style=\"font-size: 10.0pt; font-family: 'Verdana','sans-serif';\">The training provided by Simplilearn allows a candidate gain wide skills in business intelligence solutions with Microsoft SQL server 2012 as its base. After completion of the course the candidate will have a clear picture of concepts of Business Intelligence.</span></p>\n<p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify;\"><span style=\"font-size: 10.0pt; font-family: 'Verdana','sans-serif';\">&nbsp;</span></p>\n<p class=\"MsoNormal\" style=\"margin-bottom: 0.0001pt; text-align: justify;\"><span style=\"font-size: 10.0pt; font-family: 'Verdana','sans-serif';\">With Shine.com you get one month complimentary Featured Profile services which further gives boost to your job search and chances of recruiter view increases by 10 times.</span></p>",
                    "duration": 0,
                    "type": "",
                    "label": "Designing BI Solutions with MS SQL Server 2012 Online Training",
                    "level": ""
                },
                {
                    "id": 4,
                    "name": "Profile plus package",
                    "about": "Certified Logistics and Supply Chain Professional Logistics and Supply Chain Management Professional Certification, offered by Vskills, approved by Government (PSU) helps in to enhancing traditional management by focusing on organization and integration amongst various partners of supply.",
                    "url": "/course/category21-2/profile-plus-package/pd-4",
                    "imgUrl": "https://learning-media-staging-189607.storage.googleapis.com/l1/m/product_image/4/1591342088_9121.png",
                    "imgAlt": "Profile plus package",
                    "title": "Profile plus package (INR 1) - Shine Learning",
                    "slug": "profile-plus-package",
                    "jobsAvailable": 4,
                    "skillList": [
                        "HTML",
                        "CSS",
                        "Python",
                        "Production"
                    ],
                    "rating": 3.0,
                    "stars": [
                        "*",
                        "*",
                        "*",
                        "-",
                        "-"
                    ],
                    "mode": null,
                    "providerName": "Career Plus",
                    "price": 1.0,
                    "tags": 2,
                    "highlights": [
                        "Certified Logistics and Supply Chain Professional Logistics and Supply Chain Management Professional Certification, offered by Vskills, approved by Government (PSU) helps in to enhancing traditional management by focusing on organization and integration amongst various partners of supply chain for better management; thus providing greater value to the consumer."
                    ],
                    "brochure": null,
                    "u_courses_benefits": null,
                    "u_desc": "<p>Why should one take this certificate? It is used to develop knowledge, skills and competencies in the field of Logistics &amp; Supply Chain Management so as to learn different aspects of logistics including purchase, operations, warehouse, transportation and supply chain management. This certificate assists one in understanding logistics and supply chain management globally</p>"
                },
                {
                    "id": 1,
                    "name": "Lean Six Sigma Green Belt Test",
                    "about": "Test GreyCampus offers an online training and certification program on Lean Six Sigma Green Belt. Study with confidence as the course covers every topic in accordance with IASSC. Lean Six Sigma incorporates the most widely-used concepts and tools from both the Lean and Six Sigma bodies of knowledge along with DMAIC problem solving approach.",
                    "url": "/course/courses-certifications/lean-six-sigma-green-belt-test/pd-1",
                    "imgUrl": "https://learning-media-staging-189607.storage.googleapis.com/l2/m/product_image/1/1608784815_5352.png",
                    "imgAlt": "Lean Six Sigma Green Belt",
                    "title": "Lean Six Sigma Green Belt Test (INR 500) - Shine Learning",
                    "slug": "lean-six-sigma-green-belt-test",
                    "jobsAvailable": 555,
                    "skillList": [
                        "CSS",
                        "Java",
                        "Python",
                        "MongoDB",
                        "Javascript",
                        "Time Management",
                        "Management",
                        "Communication",
                        "LEAN",
                        "Six Sigma",
                        "Data Structures",
                        "Ruby On Rails",
                        "Selenium",
                        "Spooler Plus",
                        "GST",
                        "Energy Efficiency",
                        "Efficiency Management",
                        "Production",
                        "Production Techniques",
                        "Vcs Simulator",
                        "Loop Simulator",
                        "ios",
                        "aol",
                        "Decision Making",
                        "WHO",
                        "A++",
                        "Adaptability"
                    ],
                    "rating": 4.93,
                    "stars": [
                        "*",
                        "*",
                        "*",
                        "*",
                        "*"
                    ],
                    "mode": "Online",
                    "providerName": "Career Plus",
                    "price": 100.0,
                    "tags": 2,
                    "highlights": [
                        "Test GreyCampus offers an online training and certification program on Lean Six Sigma Green Belt.",
                        "Study with confidence as the course covers every topic in accordance with IASSC."
                    ],
                    "brochure": null,
                    "u_courses_benefits": null,
                    "u_desc": "<ul>\n\t<li>Lean Best suited for candidates who wish to make a successful career in quality function of an organization. management, communication, adaptability, leadership, time management, ruby on rails, react, angular, vue, decision making, communication, mongodb, ruby on rails, decision making, who, six sigma, time management</li>\n</ul>\n\n<p>&nbsp;</p>",
                    "duration": 100,
                    "type": "Basic + More Deliverable",
                    "label": "course 3",
                    "level": "Advanced"
                }
            ],
            "recommended_course_ids": [],
            "page": {
                "current_page": 1,
                "total": 1,
                "has_prev": false,
                "has_next": false
            }
        },
        "status": 200,
        "error": false
    }
}

const findRightJobsData = (data) => {
    const url = `/intent/api/v1/jobs/${data?.jobParams}&intent=2`;
    return BaseApiService.get(`${siteDomain}${url}`);
}

const upskillYourselfData = (data) => {
    const url = `/intent/api/v1/course-recommendation/${data}`;
    return BaseApiService.get(`${siteDomain}${url}`);
}

const sendFeedback = (data) => {
    const url = `/intent/api/v1/recommendation-feedback/`;
    return BaseApiService.post(`${siteDomain}${url}`, data);
}

export default {
    userIntentData,
    careerChangeData,
    findRightJobsData,
    upskillYourselfData,
    fetchServiceRecommendation,
    uploadFileUrlAPI,
    sendFeedback
}