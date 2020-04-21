


import BaseApiService from '../../../services/BaseApiService'
import { siteDomain, shineSite } from "../../../utils/domains";


const getInformation = () => {
    const url = 'candidate-login/?with_info=false';
    return BaseApiService.get(`${siteDomain}/api/v1/${url}`, {
        "Content-Type": "application/json",
        'Authorization': ''
    })
}

const uploadFileUrl = (data) => {
    const url = 'resume-score-checker/get-score/';

    return BaseApiService.post(`${shineSite}/${url}`, data,
        {}, false, true);
};
const getCandidateScore = (candidateId) => {
    const url = `resume-score-checker/get-score/?candidate_id=${candidateId}`;
    return BaseApiService.get(`${shineSite}/${url}`)
}
const expertFormSubmit = (data) => {
    const url = 'lead/lead-management/';
    return BaseApiService.post(`${siteDomain}/${url}`, data,
        { 'Content-Type': 'application/x-www-form-urlencoded' }, false);
};


const checkSessionAvailability = () => {
    const url = 'session/';
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
}


const getCandidateResume = () => {
    const url = 'candidate-resume/';
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
}

export const Api = {
    uploadFileUrl,
    expertFormSubmit,
    checkSessionAvailability,
    getCandidateResume,
    getCandidateScore,
    getInformation
}

