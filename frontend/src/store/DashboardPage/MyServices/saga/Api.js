import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';

const myServicesData = (data) => {
    const url = `my-services/?page=${data?.page}`;
    return BaseApiService.get(`${siteDomain}/dashboard/api/v1/${url}`);
};


const getOiComment = (data) => {
    const url = `${siteDomain}/api/v1/order-item-comment/?candidate_id=${data.cid}&oi_pk=${data.oi_id}`
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
    uploadResumeDashboardForm,
    getOiComment,
    postOiComment,
    // submitDashboardReviews,
    myReviewsData,
    saveReviewsData
}