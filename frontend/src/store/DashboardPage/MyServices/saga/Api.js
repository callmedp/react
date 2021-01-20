import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';

const myServicesData = (data) => {
    const url = `my-services/`;
    return BaseApiService.get(`${siteDomain}/dashboard/api/v1/${url}`);
};


const getOiComment = (data) => {
    // const url = `${siteDomain}/api/v1/order-item-comment/?candidate_id=${data.cid}&oi_pk=${data.oi_id}`
    const url = "https://learning.shine.com/api/v1/order-item-comment/?candidate_id=53461c6e6cca0763532d4b09&oi_pk=501736"
    return BaseApiService.get(url)
}

const postOiComment = (data) => {
    const url = `${siteDomain}/api/v1/order-item-comment/`
    return BaseApiService.post(url, {candidate_id: "53461c6e6cca0763532d4b09",
    comment: "   fg fg fg",
    oi_pk: 501736,
    type: "POST"})
}

const uploadResumeDashboardForm = (data) => {
    const url = `${siteDomain}/api/v1/dashboard-resume-upload/`;
    return BaseApiService.post(`${url}`, data, {
    }, true);
}


export default {
    myServicesData,
    uploadResumeDashboardForm,
    getOiComment,
    postOiComment
}