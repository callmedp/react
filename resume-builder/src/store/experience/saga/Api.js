import BaseApiService from '../../../services/BaseApiService'

const fetchUserExperience = (candidateId) => {

    const url = `user-experience/?c_id=${candidateId}/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
};


export const Api = {
    fetchUserExperience
}