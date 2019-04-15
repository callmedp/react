import BaseApiService from '../../../services/BaseApiService'


const createUserEducation = (data, candidateId, educationId = '') => {
    delete data['id'];

    const url = `candidate/${candidateId}/educations/`;
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};

const fetchUserEducation = (candidateId) => {

    const url = `candidate/${candidateId}/educations/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
};

const updateUserEducation = (data, candidateId, educationId) => {

    const url = `candidate/${candidateId}/educations/${educationId}/`;
    return BaseApiService.put(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};


const deleteUserEducation = (candidateId, educationId) => {

    const url = `candidate/${candidateId}/educations/${educationId}/`;

    return BaseApiService.deleteMethod(`http://127.0.0.1:8000/api/v1/resume/${url}`);

};

export const Api = {
    fetchUserEducation,
    createUserEducation,
    updateUserEducation,
    deleteUserEducation
}