import BaseApiService from '../../../services/BaseApiService'

import {siteDomain} from "../../../Utils/domains";

const createUserProject = (data, candidateId, userProjectId = '') => {
    delete data['id'];
    const url = `candidate/${candidateId}/projects/`;
    return BaseApiService.post(`${siteDomain}/api/v1/resume/${url}`, data);
};


const fetchUserProject = (candidateId) => {
    const url = `candidate/${candidateId}/projects/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};


const updateUserProject = (data, candidateId, userProjectId) => {
    const url = `candidate/${candidateId}/projects/${userProjectId}/`;
    return BaseApiService.put(`${siteDomain}/api/v1/resume/${url}`, data);
};

const deleteUserProject = (candidateId, projectId) => {

    const url = `candidate/${candidateId}/projects/${projectId}/`;

    return BaseApiService.deleteMethod(`${siteDomain}/api/v1/resume/${url}`);

};


const bulkUpdateUserProject = (data, candidateId) => {

    const url = `candidate/${candidateId}/bulk-update/project/`;
    return BaseApiService.post(`${siteDomain}/api/v1/resume/${url}`,data);


}


export const Api = {
    fetchUserProject,
    createUserProject,
    updateUserProject,
    deleteUserProject,
    bulkUpdateUserProject
}