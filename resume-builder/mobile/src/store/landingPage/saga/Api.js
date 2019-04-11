import BaseApiService from '../../../services/BaseApiService'

const getCandidateId = () => {
    const url = `user-profile/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
};

export const Api = {
    getCandidateId
}