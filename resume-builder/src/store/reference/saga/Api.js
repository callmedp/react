import BaseApiService from '../../../services/BaseApiService'

const fetchUserReference = (candidateId) => {

    const url = `user-references/?c_id=${candidateId}/`;
    //return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
    return {
        data: {
            "reference_name": 'Sugam Mehta',
            "reference_designation": 'Chief Executive Officer',
            "about_user": "Well works",
        }
    }
};


export const Api = {
    fetchUserReference
}