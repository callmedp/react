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

const submitDashboardReviews = (data) => {
    const url = `${siteDomain}/api/v1/dashboard-feedback/`;
    return BaseApiService.post(url, data)
}



export default {
    myServicesData,
    uploadResumeDashboardForm,
    getOiComment,
    postOiComment,
    submitDashboardReviews
}