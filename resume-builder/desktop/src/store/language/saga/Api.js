import BaseApiService from '../../../services/BaseApiService'

import {siteDomain} from "../../../Utils/domains";

const createUserLanguage = (data, candidateId, languageId = '') => {

    delete data['id'];
    const url = `candidate/${candidateId}/languages/`;
    return BaseApiService.post(`${siteDomain}/api/v1/resume/${url}`, data);
};

const fetchUserLanguage = (candidateId) => {

    const url = `candidate/${candidateId}/languages/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};


const updateUserLanguage = (data, candidateId, languageId) => {

    const url = `candidate/${candidateId}/languages/${languageId}/`;

    return BaseApiService.put(`${siteDomain}/api/v1/resume/${url}`, data);

};

const deleteUserLanguage = (candidateId, languageId) => {

    const url = `candidate/${candidateId}/languages/${languageId}/`;

    return BaseApiService.deleteMethod(`${siteDomain}/api/v1/resume/${url}`);

};

const bulkUpdateUserLanguage = (data, candidateId) => {

    const url = `candidate/${candidateId}/bulk-update/language/`;
    return BaseApiService.post(`${siteDomain}/api/v1/resume/${url}`, data);


}

export const Api = {
    fetchUserLanguage,
    updateUserLanguage,
    createUserLanguage,
    deleteUserLanguage,
    bulkUpdateUserLanguage
}