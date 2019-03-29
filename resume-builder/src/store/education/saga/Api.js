import BaseApiService from '../../../services/BaseApiService'

const fetchUserEducation = (candidateId) => {

    const url = `user-education/?c_id=${candidateId}/`;
    //return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
    return {
        data: {
            "specialization": 'B-Tech',
            "institution_name": 'GTBIT',
            "course_type": 'FULL TIME',
            "start_date": '02-11-2013',
            "percentage_cgpa": '78%',
            "end_date": '01-10-2017',
        }
    }
};


export const Api = {
    fetchUserEducation
}