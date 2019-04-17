import BaseApiService from '../../../services/BaseApiService'


const createUserLanguage = (data, candidateId, languageId = '') => {

    delete data['id'];
    const url = `candidate/${candidateId}/languages/`;
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};

const fetchUserLanguage = (candidateId) => {

    const url = `candidate/${candidateId}/languages/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
};


const updateUserLanguage = (data, candidateId, languageId) => {

    const url = `candidate/${candidateId}/languages/${languageId}/`;

    return BaseApiService.put(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);

};

const deleteUserLanguage = (candidateId, languageId) => {

    const url = `candidate/${candidateId}/languages/${languageId}/`;

    return BaseApiService.deleteMethod(`http://127.0.0.1:8000/api/v1/resume/${url}`);

};

const bulkUpdateUserLanguage = (data, candidateId) => {

    const url = `candidate/${candidateId}/bulk-update/language/`;
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`,data);


}

export const Api = {
    fetchUserLanguage,
    updateUserLanguage,
    createUserLanguage,
    deleteUserLanguage,
    bulkUpdateUserLanguage
}