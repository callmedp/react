import BaseApiService from '../../../services/BaseApiService'

import {siteDomain} from "../../../Utils/domains";

const createUserSkill = (data, candidateId, skillId = '') => {

    delete data['id'];
    const url = `candidate/${candidateId}/skills/`;
    return BaseApiService.post(`${siteDomain}/api/v1/resume/${url}`, data);
};

const fetchUserSkill = (candidateId) => {

    const url = `candidate/${candidateId}/skills/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
};

const updateUserSkill = (data, candidateId, skillId) => {

    const url = `candidate/${candidateId}/skills/${skillId}/`;

    return BaseApiService.put(`${siteDomain}/api/v1/resume/${url}`, data);
};


const deleteUserSkill = (candidateId, skillId) => {

    const url = `candidate/${candidateId}/skills/${skillId}/`;

    return BaseApiService.deleteMethod(`${siteDomain}/api/v1/resume/${url}`);

};


const bulkSaveUserSkill = (data, candidateId) => {

    const url = `candidate/${candidateId}/bulk-update/skill/`;
    return BaseApiService.post(`${siteDomain}/api/v1/resume/${url}`,data);


}


export const Api = {
    fetchUserSkill,
    createUserSkill,
    updateUserSkill,
    deleteUserSkill,
    bulkSaveUserSkill
}