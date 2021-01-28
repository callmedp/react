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

export default {
    myServicesData,
    getPendingOrderItems,
    uploadResumeDashboardForm
}