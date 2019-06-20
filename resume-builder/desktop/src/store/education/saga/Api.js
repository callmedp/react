import BaseApiService from '../../../services/BaseApiService'
import {siteDomain} from "../../../Utils/domains";

const createUserEducation = (data, candidateId, educationId = '') => {
    delete data['id'];

    const url = `candidate/${candidateId}/educations/`;
    return BaseApiService.post(`${siteDomain}/api/v1/resume/${url}`, data);
};

const fetchUserEducation = (candidateId) => {

    const url = `candidate/${candidateId}/educations/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};

const updateUserEducation = (data, candidateId, educationId) => {

    const url = `candidate/${candidateId}/educations/${educationId}/`;
    return BaseApiService.put(`${siteDomain}/api/v1/resume/${url}`, data);
};


const deleteUserEducation = (candidateId, educationId) => {

    const url = `candidate/${candidateId}/educations/${educationId}/`;

    return BaseApiService.deleteMethod(`${siteDomain}/api/v1/resume/${url}`);

};

const bulkUpdateUserEducation = (data, candidateId) => {

    const url = `candidate/${candidateId}/bulk-update/education/`;
    return BaseApiService.post(`${siteDomain}/api/v1/resume/${url}`, data);


}


export const Api = {
    fetchUserEducation,
    createUserEducation,
    updateUserEducation,
    deleteUserEducation,
    bulkUpdateUserEducation
}