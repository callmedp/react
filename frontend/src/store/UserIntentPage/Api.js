import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'

const userIntentData = (data) => {
    const url = `/api/v1/user-intent/?${data.data.type}`
    return BaseApiService.post(`${siteDomain}${url}`, data);
}

const fetchServiceRecommendation = (data) => {
    const url = '/intent/api/v1/service-recommendation/'
    return BaseApiService.get(`${siteDomain}${url}`);
}

const uploadFileUrlAPI = (data) => {
    const url = 'api/resume-score-checker/get-score';
    return BaseApiService.post(`${siteDomain}/${url}`, data, {}, true);
};

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
    findRightJobsData,
    upskillYourselfData,
    fetchServiceRecommendation,
    uploadFileUrlAPI,
    sendFeedback
}