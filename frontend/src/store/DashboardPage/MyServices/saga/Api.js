import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';

const myServicesData = (data) => {
    const url = `my-services/?page=${data?.page}`;
    return BaseApiService.get(`${siteDomain}/dashboard/api/v1/${url}`);
};

// // if pending items exists then show upload resume api
// const getPendingOrderItems = (data) => {
//     const url = `${siteDomain}/api/v1/dashboard-notification-box/?candidate_id=568a0b20cce9fb485393489b&email=priya.kharb@hindustantimes.com`;
//     return BaseApiService.get(url)
// }

const getOiComment = (data) => {
    const url = `${siteDomain}/api/v1/order-item-comment/?oi_pk=${data.oi_id}`
    return BaseApiService.get(url)
}

const postOiComment = (data) => {
    const url = `${siteDomain}/api/v1/order-item-comment/`
    return BaseApiService.post(url, data)
}

const uploadResumeDashboardForm = (data) => {
    const url = `${siteDomain}/api/v1/dashboard-resume-upload/`;
    return BaseApiService.post(`${url}`, data, {
    }, true);
}

// fetch reviews
const myReviewsData = (data) => {
    const url = `review/?product_id=${data.prod}&page=${data.page}`;
    return BaseApiService.get(`${siteDomain}/dashboard/api/v1/${url}`);
};

const saveReviewsData = (data) => {
    const url = `review/`;
    return BaseApiService.post(`${siteDomain}/dashboard/api/v1/${url}`, data);
};

export default {
    myServicesData,
    // getPendingOrderItems,
    uploadResumeDashboardForm,
    getOiComment,
    postOiComment,
    myReviewsData,
    saveReviewsData
}