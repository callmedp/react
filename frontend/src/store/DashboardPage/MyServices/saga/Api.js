import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';

const myServicesData = (data) => {
    const url = `my-services/?page=${data?.page}`;
    return BaseApiService.get(`${siteDomain}/dashboard/api/v1/${url}`);
};

const getPendingOrderItems = () => {
    const url = `${siteDomain}/dashboard/api/v1/pending-resume_items/`
    return BaseApiService.get(url)
}

const uploadResumeDashboardForm = (data) => {
    const url = `${siteDomain}/api/v1/dashboard-resume-upload/`;
    return BaseApiService.post(`${url}`, data, {
    }, true);
}

const candidateAccept = (data) => {
    const url = `${siteDomain}/dashboard/inbox-acceptservice/`
    return BaseApiService.post(url, data)
}

const candidateReject = (data) => {
    const url = `${siteDomain}/dashboard/inbox-rejectservice/`
    return BaseApiService.post(url, data, {}, true)
}

export default {
    myServicesData,
    getPendingOrderItems,
    uploadResumeDashboardForm,
    candidateAccept,
    candidateReject
}