import BaseApiService from '../../../services/BaseApiService'

import {siteDomain} from "../../../Utils/domains";


const createUserReference = (data, candidateId, userReferenceId = '') => {

    delete data['id'];
    const url = `candidate/${candidateId}/references/`;
    return BaseApiService.post(`${siteDomain}/api/v1/resume/${url}`, data);
};


const fetchUserReference = (candidateId) => {

    const url = `candidate/${candidateId}/references/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};


const updateUserReference = (data, candidateId, userReferenceId) => {

    const url = `candidate/${candidateId}/references/${userReferenceId}/`;

    return BaseApiService.put(`${siteDomain}/api/v1/resume/${url}`, data);
};


const deleteUserReference = (candidateId, referenceId) => {

    const url = `candidate/${candidateId}/references/${referenceId}/`;

    return BaseApiService.deleteMethod(`${siteDomain}/api/v1/resume/${url}`);

};


const bulkUpdateUserReference = (data, candidateId) => {

    const url = `candidate/${candidateId}/bulk-update/reference/`;
    return BaseApiService.post(`${siteDomain}/api/v1/resume/${url}`, data);


}


export const Api = {
    fetchUserReference,
    createUserReference,
    updateUserReference,
    deleteUserReference,
    bulkUpdateUserReference
}