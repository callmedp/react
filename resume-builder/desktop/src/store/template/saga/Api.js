import BaseApiService from '../../../services/BaseApiService'
import {siteDomain} from "../../../Utils/domains";

const fetchTemplate = (candidateId, templateId = 6) => {

    const url = `candidate/${candidateId}/preview/${templateId}/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};

const customizeTemplate = (candidateId, templateId, data) => {
    const url = `candidate/${candidateId}/customize/${templateId}/`
    return BaseApiService.patch(`${siteDomain}/api/v1/resume/${url}`, data)
}

export const Api = {
    fetchTemplate,
    customizeTemplate
}