


import BaseApiService from '../../../services/BaseApiService'
import {siteDomain} from "../../../Utils/domains";







const fetchFileUrl = (data) => {
    const url = 'resume/api/v1/resume-score-checker/';
    return BaseApiService.post(`${siteDomain}/api/v1/${url}`, data,
        {}, false, true);
};



export const Api ={
    fetchFileUrl
}