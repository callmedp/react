import BaseApiService from '../../../services/BaseApiService'

const fetchPersonalInfo = (candidateId) => {
    const url = `users/${candidateId}/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
};

const updatePersonalData = (data, candidateId) => {
    const url = `users/${candidateId}/`;
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};


export const Api = {
    fetchPersonalInfo,
    updatePersonalData
}