import BaseApiService from '../../../services/BaseApiService'

const fetchPersonalInfo = (candidateId) => {

    const url = `candidates/${candidateId}/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
};

const updatePersonalData = (data, candidateId) => {
    const url = `candidates/${candidateId}/`;
    return BaseApiService.put(`http://127.0.0.1:8000/api/v1/resume/${url}`, data);
};

const fetchImageUrl = (data) => {
    const url = `media-upload/`;
    return BaseApiService.post(`http://127.0.0.1:8000/api/v1/${url}`, data,
        {}, false, true);
};


export const Api = {
    fetchPersonalInfo,
    updatePersonalData,
    fetchImageUrl
}