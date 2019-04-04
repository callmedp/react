import BaseApiService from '../../../services/BaseApiService'

const fetchUserAward = (candidateId) => {

    const url = `candidate/${candidateId}/achievements/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
    // return {
    //     data: {
    //         "title": 'Snackdown 2019',
    //         "date": '22-10-2019',
    //         "summary": 'A competitive programming challenge with all over the world.',
    //     }
    // }
};


const createUserAward = (data, candidateId, userAwardId = '') => {
    delete data['id'];

    const url = `candidate/${candidateId}/achievements/`;
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

const updateUserAward = (data, candidateId, userAwardId) => {

    const url = `candidate/${candidateId}/achievements/${userAwardId}/`;
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
    fetchUserAward,
    updateUserAward,
    createUserAward
}