import BaseApiService from '../../../services/BaseApiService';
import { siteDomain } from '../../../Utils/domains';

const defaultHeaders = {}

const fileUpload = (data) =>{
    const url = `resume-score-checker/`
    return BaseApiService.post(`${siteDomain}/resume/api/v1/${url}`, data, { defaultHeaders } , false, true);
}

const expertFormSubmit = (data) => {
    const url = ``
    return BaseApiService.post(`${siteDomain}/resume/api/v1/${url}`, data, { defaultHeaders } , false, true);
}

const checkSessionAvailability = () => {
    const url = 'session/';
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
}

const getCandidateId = () => {
    const url = `user-profile/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
}

const getCandidateResume = () => {
    const url = ``;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
}

export const Api = {
    fileUpload,
    expertFormSubmit,
    checkSessionAvailability,
    getCandidateId,
    getCandidateResume
};