import BaseApiService from '../../../services/BaseApiService'

const fetchUserSkill = (candidateId) => {

    const url = `skills/?c_id=${candidateId}/`;
    //return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
    return {
        data: {
            "name": 'JavaScript',
            "proficiency": 7
        }
    }
};


export const Api = {
    fetchUserSkill
}