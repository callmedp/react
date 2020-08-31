import BaseApiService from '../../../services/BaseApiService'

import {siteDomain, chatDomain} from "../../../Utils/domains";

const fetchPersonalInfo = (candidateId) => {

    const url = `candidates/${candidateId}/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};

const updatePersonalData = (data, candidateId) => {
    const url = `candidates/${candidateId}/`;
    return BaseApiService.put(`${siteDomain}/api/v1/resume/${url}`, data);
};

const createPersonalInfo = (data) => {
    const url = `candidates/`;
    return BaseApiService.post(`${siteDomain}/api/v1/resume/${url}`, data);
}

const fetchImageUrl = (data) => {
    const url = `media-upload/`;
    return BaseApiService.post(`${siteDomain}/api/v1/${url}`, data,
        {}, false, true);
};

const fetchInterestList = (searchText) => {
    return BaseApiService.get(`${siteDomain}/api/v1/resume/interest-list/?search=${searchText}`);
};

const updateEntityPreference = (data, candidateId) => {
    const url = `candidates/${candidateId}/`;
    return BaseApiService.patch(`${siteDomain}/api/v1/resume/${url}`, data);
};

const getChatBotUrl = () => {
    return BaseApiService.get(`${chatDomain}/api/app/resume/get-script/`);
};

export const Api = {
    fetchPersonalInfo,
    updatePersonalData,
    fetchImageUrl,
    createPersonalInfo,
    fetchInterestList,
    updateEntityPreference,
    getChatBotUrl
}