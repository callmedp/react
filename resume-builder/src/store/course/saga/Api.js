import BaseApiService from '../../../services/BaseApiService'

const fetchUserCourse = (candidateId) => {

    const url = `user-certifications/?c_id=${candidateId}/`;
    //return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
    return {
        data: {
            "name_of_certification": 'JAVA CERTIFICATE',
            "year_of_certification": '20-10-2019',
        }
    }
};


export const Api = {
    fetchUserCourse
}