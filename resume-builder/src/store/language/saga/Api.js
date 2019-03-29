import BaseApiService from '../../../services/BaseApiService'

const fetchUserLanguage = (candidateId) => {

    const url = `user-language/?c_id=${candidateId}/`;
    //return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
    return {
        data: {
            "name": 'English',
            "proficiency": 7
        }
    }
};


export const Api = {
    fetchUserLanguage
}