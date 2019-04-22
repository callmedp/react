import BaseApiService from '../../../services/BaseApiService'

const getCandidateId = () => {
    const url = `user-profile/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
};


const loginCandidate = (data) => {
    const url = `candidate-login/`;
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/${url}`, data, {
        "Content-Type": "application/json",
    });
}


export const Api = {
    getCandidateId,
    loginCandidate

}