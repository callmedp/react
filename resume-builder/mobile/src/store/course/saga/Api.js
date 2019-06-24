import BaseApiService from '../../../services/BaseApiService'

import {siteDomain} from "../../../Utils/domains";


const createUserCourse = (data, candidateId, courseId = '') => {
    delete data['id'];
    const url = `candidate/${candidateId}/certifications/`;
    return BaseApiService.post(`${siteDomain}/api/v1/resume/${url}`, data);
};

const fetchUserCourse = (candidateId) => {

    const url = `candidate/${candidateId}/certifications/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};


const updateUserCourse = (data, candidateId, courseId) => {

    const url = `candidate/${candidateId}/certifications/${courseId}/`;
    return BaseApiService.put(`${siteDomain}/api/v1/resume/${url}`, data);
};


const deleteUserCourse = (candidateId, courseId) => {

    const url = `candidate/${candidateId}/certifications/${courseId}/`;

    return BaseApiService.deleteMethod(`${siteDomain}/api/v1/resume/${url}`);

};


const bulkUpdateUserCourse = (data, candidateId) => {

    const url = `candidate/${candidateId}/bulk-update/certification/`;
    return BaseApiService.post(`${siteDomain}/api/v1/resume/${url}`,data);


}


export const Api = {
    fetchUserCourse,
    createUserCourse,
    updateUserCourse,
    deleteUserCourse,
    bulkUpdateUserCourse
}