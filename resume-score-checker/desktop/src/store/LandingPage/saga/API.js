


import BaseApiService from '../../../services/BaseApiService'
import {siteDomain} from "../../../utils/domains";

const getCandidateId = () => {
    const url = `user-profile/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};



const uploadFileUrl = (data) => {
    const url = 'resume-score-checker/';
   
    return BaseApiService.post(`${siteDomain}/resume/api/v1/${url}`, data,
        {}, false, true);
};

const expertFormSubmit = (data) => {
    const url = 'experts/';
    return BaseApiService.post(`${siteDomain}/resume/api/v1/${url}`, data,
        {}, false, true);
};


const checkSessionAvailability = () => {
    const url = 'session/';
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
}


const getCandidateResume = () => {
    const url = 'candidate-resume/';
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
}

export const Api ={
    uploadFileUrl,
    expertFormSubmit,
    checkSessionAvailability,
    getCandidateId,
    getCandidateResume,
}

