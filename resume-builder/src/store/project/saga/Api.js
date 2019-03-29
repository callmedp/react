import BaseApiService from '../../../services/BaseApiService'

const fetchUserProject = (candidateId) => {

    const url = `user-projects/?c_id=${candidateId}/`;
    //return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
    return {
        data: {
            "project_name": 'Implement Facial Expression',
            "start_date": '22-10-2018',
            "end_date": '22-02-2019',
            "skills": '',
            "description": ''
        }
    }
};


export const Api = {
    fetchUserProject
}