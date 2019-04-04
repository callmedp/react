import BaseApiService from '../../../services/BaseApiService'

const fetchUserCourse = (candidateId) => {

    const url = `candidate/${candidateId}/certifications/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
    // return {
    //     data: {
    //         "name_of_certification": 'JAVA CERTIFICATE',
    //         "year_of_certification": '20-10-2019',
    //     }
    // }
};


const createUserCourse = (data, candidateId, courseId = '') => {
    delete data['id'];
    const url = `candidate/${candidateId}/certifications/`;
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
    // return {
    //     data: {
    //         "specialization": 'B-Tech',
    //         "institution_name": 'GTBIT',
    //         "course_type": 'FULL TIME',
    //         "start_date": '02-11-2013',
    //         "percentage_cgpa": '78%',
    //         "end_date": '01-10-2017',
    //     }
    // }
};

const updateUserCourse = (data, candidateId, courseId) => {

    const url = `candidate/${candidateId}/certifications/${courseId}/`;
    return BaseApiService.put(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
    // return {
    //     data: {
    //         "specialization": 'B-Tech',
    //         "institution_name": 'GTBIT',
    //         "course_type": 'FULL TIME',
    //         "start_date": '02-11-2013',
    //         "percentage_cgpa": '78%',
    //         "end_date": '01-10-2017',
    //     }
    // }
};




export const Api = {
    fetchUserCourse,
    createUserCourse,
    updateUserCourse
}