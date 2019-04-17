import BaseApiService from '../../../services/BaseApiService'

const fetchTemplate = (candidateId, templateId = 5) => {

    const url = `candidate/${candidateId}/preview/${templateId}/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
};

export const Api = {
    fetchTemplate,

}