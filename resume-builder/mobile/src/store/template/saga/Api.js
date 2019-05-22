import BaseApiService from '../../../services/BaseApiService'

import {siteDomain} from "../../../Utils/domains";

const fetchTemplate = (candidateId, templateId = 5) => {
    console.log("template Id",templateId)
    const url = `candidate/${candidateId}/preview/${templateId}/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};

export const Api = {
    fetchTemplate,

}