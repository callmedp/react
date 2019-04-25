import BaseApiService from '../../../services/BaseApiService'


const createUserAward = (data, candidateId, userAwardId = '') => {
    delete data['id'];

    const url = `candidate/${candidateId}/achievements/`;
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};

const fetchUserAward = (candidateId) => {

    const url = `candidate/${candidateId}/achievements/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
};

const updateUserAward = (data, candidateId, userAwardId) => {

    const url = `candidate/${candidateId}/achievements/${userAwardId}/`;
    return BaseApiService.put(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};


const deleteUserAward = (candidateId, awardId) => {
    ////console.log(awardId)
    const url = `candidate/${candidateId}/achievements/${awardId}/`;

    return BaseApiService.deleteMethod(`http://127.0.0.1:8000/api/v1/resume/${url}`);

};


const bulkUpdateUserAward = (data, candidateId) => {

    const url = `candidate/${candidateId}/bulk-update/achievement/`;
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/resume/${url}`,data);


}


export const Api = {
    fetchUserAward,
    updateUserAward,
    createUserAward,
    deleteUserAward,
    bulkUpdateUserAward
}