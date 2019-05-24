import BaseApiService from '../../../services/BaseApiService'
import {siteDomain} from "../../../Utils/domains";

const fetchTemplate = (candidateId, templateId = 6) => {

    const url = `candidate/${candidateId}/preview/${templateId}/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};

const fetchTemplateImages = (candidateId, templateId = 6) => {

    const url = `candidate/${candidateId}/image-preview/${templateId}/?tsize=151x249`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};
const fetchDefaultCustomization = (candidateId, templateId = 6) => {

    const url = `candidate/${candidateId}/customisations/${templateId}/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};

const customizeTemplate = (candidateId, templateId, data) => {
    const url = `candidate/${candidateId}/customisations/${templateId}/`
    return BaseApiService.patch(`${siteDomain}/api/v1/resume/${url}`, data)
}

export const Api = {
    fetchTemplate,
    customizeTemplate,
    fetchTemplateImages,
    fetchDefaultCustomization
}