import BaseApiService from '../../../services/BaseApiService'

import {siteDomain} from "../../../Utils/domains";

const createUserExperience = (data, candidateId, experienceId = '') => {
    delete data['id'];
    const url = `candidate/${candidateId}/experiences/`;

    return BaseApiService.post(`${siteDomain}/api/v1/resume/${url}`, data);

};


const fetchUserExperience = (candidateId) => {

    const url = `candidate/${candidateId}/experiences/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};

const updateUserExperience = (data, candidateId, experienceId = '') => {

    const url = `candidate/${candidateId}/experiences/${experienceId}/`;

    return BaseApiService.put(`${siteDomain}/api/v1/resume/${url}`, data);
};


const deleteUserExperience = (candidateId, experienceId) => {

    const url = `candidate/${candidateId}/experiences/${experienceId}/`;

    return BaseApiService.deleteMethod(`${siteDomain}/api/v1/resume/${url}`);

};


const bulkUpdateUserExperience = (data, candidateId) => {

    const url = `candidate/${candidateId}/bulk-update/experience/`;
    return BaseApiService.post(`${siteDomain}/api/v1/resume/${url}`, data);

};

const fetchJobTitlesAndSuggestions = (title, subType = '') => {

    let url = `suggestion/?main_type=job_title&query=${title}`;
    if (subType) {
        url += `&sub_type=${subType}`
    }
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);

};


export const Api = {
    fetchUserExperience,
    updateUserExperience,
    createUserExperience,
    deleteUserExperience,
    bulkUpdateUserExperience,
    fetchJobTitlesAndSuggestions
}