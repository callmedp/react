import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';

const myServicesData = (data) => {
    const url = `my-services/?page=${data?.page}`;
    return BaseApiService.get(`${siteDomain}/dashboard/api/v1/${url}`);
};

const uploadResumeDashboardForm = (data) => {
    const url = `${siteDomain}/api/v1/dashboard-resume-upload/`;
    return BaseApiService.post(`${url}`, data, {
    }, true);
}

//fetch Pending Resumes
const getPendingResumes = (data) => {
    const url = `${siteDomain}/api/v1/dashboard-notification-box/`
    return BaseApiService.get(url)
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
    uploadResumeDashboardForm,
    getPendingResumes,
    candidateAccept,
    candidateReject
}