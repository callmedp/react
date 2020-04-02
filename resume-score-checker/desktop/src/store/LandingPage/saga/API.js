


import BaseApiService from '../../../services/BaseApiService'
import {siteDomain} from "../../../utils/domains";






const uploadFileUrl = (data) => {
    const url = 'resume-score-checker/';
    return BaseApiService.post(`${siteDomain}/resume/api/v1/${url}`, data,
        {}, false, true);
};



export const Api ={
    uploadFileUrl
}

