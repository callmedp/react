import BaseApiService from '../../../services/BaseApiService'
import {siteDomain} from "../../../Utils/domains";

const getCandidateId = () => {
    const url = `user-profile/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};


const loginCandidate = (data) => {
    const url = `candidate-login/`;
    return BaseApiService.post(`${siteDomain}/api/v1/${url}`, data, {
        "Content-Type": "application/json",
    });
};

const getInformation = (data) => {
    const url = 'candidate-login/';
    return BaseApiService.get(`${siteDomain}/api/v1/${url}`)
}


export const Api = {
    getCandidateId,
    loginCandidate,
    getInformation

}