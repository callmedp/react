import BaseApiService from '../../../services/BaseApiService'


const createUserProject = (data, candidateId, userProjectId = '') => {
    delete data['id'];
    const url = `candidate/${candidateId}/projects/`;
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};


const fetchUserProject = (candidateId) => {
    const url = `candidate/${candidateId}/projects/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
};


const updateUserProject = (data, candidateId, userProjectId) => {
    const url = `candidate/${candidateId}/projects/${userProjectId}/`;
    return BaseApiService.put(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};

const deleteUserProject = (candidateId, projectId) => {

    const url = `candidate/${candidateId}/projects/${projectId}/`;

    return BaseApiService.deleteMethod(`http://127.0.0.1:8000/api/v1/resume/${url}`);

};


const bulkUpdateUserProject = (data, candidateId) => {

    const url = `candidate/${candidateId}/bulk-update/project/`;
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`,data);


}


export const Api = {
    fetchUserProject,
    createUserProject,
    updateUserProject,
    deleteUserProject,
    bulkUpdateUserProject
}