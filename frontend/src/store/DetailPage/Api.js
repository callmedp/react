import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'

const otherProvidersCourses = (data) => {
    // const url = `/api/v1/most-viewed-courses/?category_id=${data.categoryId}`;
    // return BaseApiService.get(`${siteDomain}${url}`);
    return {
        'data':{
            'pop_list':[
                {
                   "id":6478,
                   "imgAlt":"Test course",
                   "name":"Test course",
                   "providerName":"analytics vidhya",
                   "imgUrl":"https://learning-media-staging-189607.storage.googleapis.com/l2/m/vendor/2/1609910163_5388.png",
                   "url":"/course/courses-certifications/test-course-3/pd-6478",
                   "price":1021.0,
                   "rating": 4,
                   "stars": [
                       '*', '*', '*', '*', '*', '+'
                   ],
                   "short_description":"None"
                },
                {
                   "id":2714,
                   "imgAlt":"Test University Course",
                   "name":"university course46",
                   "providerName":"ops",
                   "imgUrl":"https://learning-media-staging-189607.storage.googleapis.com/l2/m/vendor/2/1609910163_5388.png",
                   "url":"/course/courses-certifications/test-university-course/pd-2714",
                   "price":700.0,
                   "rating": 4,
                   "stars": [
                       '*', '*', '*', '*', '*', '-'
                   ],
                   "short_description":"None"
                },
                {
                   "id":25,
                   "imgAlt":"Job Service5",
                   "name":"Job Service5",
                   "providerName":"VSkill",
                   "imgUrl":"https://learning-media-staging-189607.storage.googleapis.com/l2/m/vendor/2/1609910163_5388.png",
                   "url":"/course/courses-certifications/job-service5/pd-25",
                   "price":0.0,
                   "rating": 4,
                   "stars": [
                        '*', '*', '*', '*', '*', '+'
                    ],
                   "short_description":"None"
                },
                {
                   "id":22,
                   "imgAlt":"Job Service2",
                   "name":"Job Service2",
                   "providerName":"VSkill",
                   "imgUrl":"https://learning-media-staging-189607.storage.googleapis.com/l2/m/vendor/2/1609910163_5388.png",
                   "url":"/course/courses-certifications/job-service2/pd-22",
                   "price":0.0,
                   "rating": 4,
                   "stars": [
                        '*', '*', '*', '*', '*', '-'
                    ],
                   "short_description":"None"
                },
                {
                   "id":1921,
                   "imgAlt":"Certified ERP Manager",
                   "name":"Certified ERP Manager - Certification Course",
                   "providerName":"Vskills",
                   "imgUrl":"https://learning-media-staging-189607.storage.googleapis.com/l2/m/vendor/15/1609910067_2290.png",
                   "url":"/course/courses-certifications/certified-erp-manager-2/pd-1921",
                   "price":7800.0,
                   "rating": 4,
                   "stars": [
                        '*', '*', '*', '*', '*', '+'
                    ],
                   "short_description":"None"
                },
                {
                   "id":2787,
                   "imgAlt":"Test Product New",
                   "name":"Test Product New",
                   "providerName":"ops",
                   "imgUrl":"https://learning-media-staging-189607.storage.googleapis.com/l2/m/vendor/2/1609910163_5388.png",
                   "url":"/services/courses-certifications/test-product-new/pd-2787",
                   "price":3000.0,
                   "rating": 4,
                   "stars": [
                        '*', '*', '*', '*', '*', '+'
                    ],
                   "short_description":"None"
                }
            ]
        }
    }
}

const fetchReviews = (data) => {
    const url = `/shop/api/v1/get-prd-review/?pid=${data.prdId}&page=${data.page}`;
    return BaseApiService.get(`${siteDomain}${url}`);
}

const submitReviews = (data) => {
    const url = `/shop/api/v1/product/review/`;
    return BaseApiService.post(`${siteDomain}${url}`, data);

    // return {'data': {'display_message': 'Form Submitted Succesfully'}}
}

const mainCourses = (id) => {
    const url = `/shop/api/v1/get-product/?pid=${id}`;
    return BaseApiService.get(`${siteDomain}${url}`);
}

const recommendedCoursesApi = (data) => {
    // const url = `/api/v1/most-viewed-courses/?category_id=${data.categoryId}`;
    // return BaseApiService.get(`${siteDomain}${url}`);
    return {
        'data':{
            'pop_list':[
                {
                   "id":6478,
                   "imgAlt":"Test course",
                   "name":"Test course",
                   "providerName":"analytics vidhya",
                   "imgUrl":"https://learning-media-staging-189607.storage.googleapis.com/l2/m/vendor/2/1609910163_5388.png",
                   "url":"/course/courses-certifications/test-course-3/pd-6478",
                   "price":1021.0,
                   "rating": 4,
                   "stars": [
                       '*', '*', '*', '*', '*', '+'
                   ],
                   "short_description":"None"
                },
                {
                   "id":2714,
                   "imgAlt":"Test University Course",
                   "name":"university course46",
                   "providerName":"ops",
                   "imgUrl":"https://learning-media-staging-189607.storage.googleapis.com/l2/m/vendor/2/1609910163_5388.png",
                   "url":"/course/courses-certifications/test-university-course/pd-2714",
                   "price":700.0,
                   "rating": 4,
                   "stars": [
                       '*', '*', '*', '*', '*', '-'
                   ],
                   "short_description":"None"
                },
                {
                   "id":25,
                   "imgAlt":"Job Service5",
                   "name":"Job Service5",
                   "providerName":"VSkill",
                   "imgUrl":"https://learning-media-staging-189607.storage.googleapis.com/l2/m/vendor/2/1609910163_5388.png",
                   "url":"/course/courses-certifications/job-service5/pd-25",
                   "price":0.0,
                   "rating": 4,
                   "stars": [
                        '*', '*', '*', '*', '*', '+'
                    ],
                   "short_description":"None"
                },
                {
                   "id":22,
                   "imgAlt":"Job Service2",
                   "name":"Job Service2",
                   "providerName":"VSkill",
                   "imgUrl":"https://learning-media-staging-189607.storage.googleapis.com/l2/m/vendor/2/1609910163_5388.png",
                   "url":"/course/courses-certifications/job-service2/pd-22",
                   "price":0.0,
                   "rating": 4,
                   "stars": [
                        '*', '*', '*', '*', '*', '-'
                    ],
                   "short_description":"None"
                },
                {
                   "id":1921,
                   "imgAlt":"Certified ERP Manager",
                   "name":"Certified ERP Manager - Certification Course",
                   "providerName":"Vskills",
                   "imgUrl":"https://learning-media-staging-189607.storage.googleapis.com/l2/m/vendor/15/1609910067_2290.png",
                   "url":"/course/courses-certifications/certified-erp-manager-2/pd-1921",
                   "price":7800.0,
                   "rating": 4,
                   "stars": [
                        '*', '*', '*', '*', '*', '+'
                    ],
                   "short_description":"None"
                },
                {
                   "id":2787,
                   "imgAlt":"Test Product New",
                   "name":"Test Product New",
                   "providerName":"ops",
                   "imgUrl":"https://learning-media-staging-189607.storage.googleapis.com/l2/m/vendor/2/1609910163_5388.png",
                   "url":"/services/courses-certifications/test-product-new/pd-2787",
                   "price":3000.0,
                   "rating": 4,
                   "stars": [
                        '*', '*', '*', '*', '*', '+'
                    ],
                   "short_description":"None"
                }
            ]
        }
    }
}


const EnquireNewSend = (data) => {
    const url = `lead-management`;
    return BaseApiService.post(`${siteDomain}/lead/api/v1/${url}/`, data);
}

const addToCartApi = (data) => {
    console.log(data);
    return BaseApiService.post(`${siteDomain}/api/v1/cart/add/`, data);
}

export default {
    mainCourses,
    otherProvidersCourses,
    fetchReviews,
    submitReviews,
    recommendedCoursesApi,
    EnquireNewSend,
    addToCartApi
}   

