import BaseApiService from '../../../services/BaseApiService'

const fetchUserLanguage = (candidateId) => {

    const url = `candidate/${candidateId}/languages/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
    // return {
    //     data: {
    //         "name": 'English',
    //         "proficiency": 7
    //     }
    // }
};


const updateUserLanguage = (data, candidateId, languageId) => {

    const url = `candidate/${candidateId}/languages/${languageId}/`;

    return BaseApiService.put(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
    // return {
    //     data: {
    //         "name": 'JavaScript',
    //         "proficiency": 7
    //     }
    // }
};

const createUserLanguage = (data, candidateId, languageId = '') => {

    delete data['id'];
    const url = `candidate/${candidateId}/languages/`;
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
    // return {
    //     data: {
    //         "name": 'JavaScript',
    //         "proficiency": 7
    //     }
    // }
};

export const Api = {
    fetchUserLanguage,
    updateUserLanguage,
    createUserLanguage
}