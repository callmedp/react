import BaseApiService from '../../../services/BaseApiService'

const fetchUserSkill = (candidateId) => {

    const url = `candidate/${candidateId}/skills/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
};

const updateUserSkill = (data, candidateId, skillId) => {

    const url = `candidate/${candidateId}/skills/${skillId}/`;

    return BaseApiService.put(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};

const createUserSkill = (data, candidateId, skillId = '') => {

    delete data['id'];
    const url = `candidate/${candidateId}/skills/`;
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};


export const Api = {
    fetchUserSkill,
    createUserSkill,
    updateUserSkill
}