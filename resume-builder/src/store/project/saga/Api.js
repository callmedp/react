import BaseApiService from '../../../services/BaseApiService'

const fetchUserProject = (candidateId) => {

    const url = `candidate/${candidateId}/projects/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
    // return {
    //     data: {
    //         "project_name": 'Implement Facial Expression',
    //         "start_date": '22-10-2018',
    //         "end_date": '22-02-2019',
    //         "skills": '',
    //         "description": ''
    //     }
    // }
};


const updateUserProject = (data, candidateId, userProjectId) => {

    const url = `candidate/${candidateId}/projects/${userProjectId}/`;

    return BaseApiService.put(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
    // return {
    //     data: {
    //         "name": 'JavaScript',
    //         "proficiency": 7
    //     }
    // }
};

const createUserProject = (data, candidateId, userProjectId = '') => {

    delete data['id'];
    const url = `candidate/${candidateId}/projects/`;
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
    // return {
    //     data: {
    //         "name": 'JavaScript',
    //         "proficiency": 7
    //     }
    // }
};


export const Api = {
    fetchUserProject,
    createUserProject,
    updateUserProject
}