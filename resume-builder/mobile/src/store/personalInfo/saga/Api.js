import BaseApiService from '../../../services/BaseApiService'

import {siteDomain} from "../../../Utils/domains";

const fetchPersonalInfo = (candidateId) => {

    const url = `candidates/${candidateId}/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};

const updatePersonalData = (data, candidateId) => {
    const url = `candidates/${candidateId}/`;
    return BaseApiService.put(`${siteDomain}/api/v1/resume/${url}`, data);
};

const fetchImageUrl = (data) => {
    const url = `media-upload/`;
    return BaseApiService.post(`${siteDomain}/api/v1/${url}`, data,
        {}, false, true);
};


export const Api = {
    fetchPersonalInfo,
    updatePersonalData,
    fetchImageUrl
}