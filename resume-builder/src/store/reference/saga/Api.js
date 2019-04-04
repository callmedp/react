import BaseApiService from '../../../services/BaseApiService'

const fetchUserReference = (candidateId) => {

    const url = `candidate/${candidateId}/references/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
    // return {
    //     data: {
    //         "reference_name": 'Sugam Mehta',
    //         "reference_designation": 'Chief Executive Officer',
    //         "about_user": "Well works",
    //     }
    // }
};


const updateUserReference = (data, candidateId, userReferenceId) => {

    const url = `candidate/${candidateId}/references/${userReferenceId}/`;

    return BaseApiService.put(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
    // return {
    //     data: {
    //         "name": 'JavaScript',
    //         "proficiency": 7
    //     }
    // }
};

const createUserReference = (data, candidateId, userReferenceId = '') => {

    delete data['id'];
    const url = `candidate/${candidateId}/references/`;
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
    // return {
    //     data: {
    //         "name": 'JavaScript',
    //         "proficiency": 7
    //     }
    // }
};


export const Api = {
    fetchUserReference,
    createUserReference,
    updateUserReference
}