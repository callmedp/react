import BaseApiService from '../../../services/BaseApiService'

const fetchUserExperience = (candidateId) => {

    const url = `candidate/${candidateId}/experiences/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
};

const updateUserExperience = (data, candidateId, experienceId = '') => {

    const url = `candidate/${candidateId}/experiences/${experienceId}/`;

    return BaseApiService.put(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};


const createUserExperience = (data, candidateId, experienceId = '') => {
    delete data['id'];
    const url = `candidate/${candidateId}/experiences/`;

    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);

};


export const Api = {
    fetchUserExperience,
    updateUserExperience,
    createUserExperience
}