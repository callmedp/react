import BaseApiService from '../../../services/BaseApiService'
import {siteDomain} from "../../../Utils/domains";

const fetchTemplate = (candidateId, templateId = 6) => {

    const url = `candidate/${candidateId}/preview/${templateId}/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};

const fetchTemplateImages = (candidateId, templateId = 6, query) => {

    let url = `candidate/${candidateId}/image-preview/${templateId}/`;
    if (query) url += `?${query}`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};
const fetchDefaultCustomization = (candidateId, templateId = 6) => {

    const url = `candidate/${candidateId}/order-customisations/${templateId}/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};

const customizeTemplate = (candidateId, templateId, data) => {
    const url = `candidate/${candidateId}/order-customisations/${templateId}/`
    return BaseApiService.patch(`${siteDomain}/api/v1/resume/${url}`, data)
}

const reorderSection = (candidateId, templateId, data) => {
    const url = `candidate/${candidateId}/entity-reorder/${templateId}/`;
    return BaseApiService.post(`${siteDomain}/api/v1/resume/${url}`, data)
}

export const Api = {
    fetchTemplate,
    customizeTemplate,
    fetchTemplateImages,
    fetchDefaultCustomization,
    reorderSection
}