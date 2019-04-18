import BaseApiService from '../../../services/BaseApiService'


const createUserCourse = (data, candidateId, courseId = '') => {
    delete data['id'];
    const url = `candidate/${candidateId}/certifications/`;
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};

const fetchUserCourse = (candidateId) => {

    const url = `candidate/${candidateId}/certifications/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
};


const updateUserCourse = (data, candidateId, courseId) => {

    const url = `candidate/${candidateId}/certifications/${courseId}/`;
    return BaseApiService.put(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};


const deleteUserCourse = (candidateId, courseId) => {

    const url = `candidate/${candidateId}/certifications/${courseId}/`;

    return BaseApiService.deleteMethod(`http://127.0.0.1:8000/api/v1/resume/${url}`);

};


const bulkUpdateUserCourse = (data, candidateId) => {

    const url = `candidate/${candidateId}/bulk-update/certification/`;
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`,data);


}


export const Api = {
    fetchUserCourse,
    createUserCourse,
    updateUserCourse,
    deleteUserCourse,
    bulkUpdateUserCourse
}