import BaseApiService from '../../../services/BaseApiService'

import {siteDomain} from "../../../Utils/domains";

const createUserAward = (data, candidateId, userAwardId = '') => {
    delete data['id'];

    const url = `candidate/${candidateId}/achievements/`;
    return BaseApiService.post(`${siteDomain}/api/v1/resume/${url}`, data);
};

const fetchUserAward = (candidateId) => {

    const url = `candidate/${candidateId}/achievements/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};

const updateUserAward = (data, candidateId, userAwardId) => {

    const url = `candidate/${candidateId}/achievements/${userAwardId}/`;
    return BaseApiService.put(`${siteDomain}/api/v1/resume/${url}`, data);
};


const deleteUserAward = (candidateId, awardId) => {

    const url = `candidate/${candidateId}/achievements/${awardId}/`;

    return BaseApiService.deleteMethod(`${siteDomain}/api/v1/resume/${url}`);

};


const bulkUpdateUserAward = (data, candidateId) => {

    const url = `candidate/${candidateId}/bulk-update/award/`;
    return BaseApiService.post(`${siteDomain}/api/v1/resume/${url}`, data);


}


export const Api = {
    fetchUserAward,
    updateUserAward,
    createUserAward,
    deleteUserAward,
    bulkUpdateUserAward
}