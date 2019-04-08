import BaseApiService from '../../../services/BaseApiService'

const fetchTemplate = (candidateId, templateId = 1) => {

    const url = `candidate/${candidateId}/preview/${templateId}/`;
    return BaseApiService.get(`http://127.0.0.1:8000/api/v1/resume/${url}`);
    // // return {
    // //     data: {
    // //         "name": 'JavaScript',
    // //         "proficiency": 7
    // //     }
    // }
};

export const Api = {
    fetchTemplate,

}