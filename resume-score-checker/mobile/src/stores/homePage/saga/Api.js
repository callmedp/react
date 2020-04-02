import BaseApiService from '../../../services/BaseApiService';
import { siteDomain } from '../../../Utils/domains';

const defaultHeaders = {}

const fileUpload = (data) =>{
    const url = `resume-score-checker/`
    return BaseApiService.post(`${siteDomain}/resume/api/v1/${url}`, data, { defaultHeaders } , false, true);
}

export const Api = {
    fileUpload
};