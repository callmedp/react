import BaseApiService from '../../../services/BaseApiService'
import { siteDomain } from "../../../Utils/domains";

const getCandidateId = () => {
    const url = `user-profile/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};


const loginCandidate = (data) => {
    const url = `candidate-login/`;
    return BaseApiService.post(`${siteDomain}/api/v1/${url}`, data, {
        "Content-Type": "application/json",
    });
};

const getInformation = (data) => {
    const url = 'candidate-login/';
    return BaseApiService.get(`${siteDomain}/api/v1/${url}`,
        {
            "Content-Type": "application/json",
            'Authorization': ''
        })
}

const feedbackSubmit = (data) => {
    const url = 'lead/lead-management/';
    return BaseApiService.post(`${siteDomain}/${url}`, data, { 'Content-Type': 'application/x-www-form-urlencoded' }, false);
}


const checkSessionAvaialability = () => {
    const url = 'session/';
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
}

export const Api = {
    getCandidateId,
    loginCandidate,
    getInformation,
    feedbackSubmit,
    checkSessionAvaialability
}