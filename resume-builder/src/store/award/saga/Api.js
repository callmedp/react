import BaseApiService from '../../../services/BaseApiService'

const fetchUserAward = (candidateId) => {

    const url = `user-achievements/?c_id=${candidateId}/`;
    //return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
    return {
        data: {
            "title": 'Snackdown 2019',
            "date": '22-10-2019',
            "summary": 'A competitive programming challenge with all over the world.',
        }
    }
};


export const Api = {
    fetchUserAward
}