import BaseApiService from '../../../services/BaseApiService';
import { siteDomain } from '../../../Utils/domains';

const defaultHeaders = {}

const fileUpload = (data) =>{
    const url = `resume-score-checker/`
    // return BaseApiService.post(`${siteDomain}/resume/api/v1/${url}`, data, { defaultHeaders } , false, true);
    return {
        data :{'total_score': 32, 'section_score': [{'section_name': 'Format/Style', 'section_score': 2.0, 'section_total_score': 10, 'section_description': 'format style', 'section_status': 1}, {'section_name': 'Summary & Objective', 'section_score': 2.5, 'section_total_score': 10, 'section_description': 'summary', 'section_status': 1}, {'section_name': 'Education Detail', 'section_score': 5.0, 'section_total_score': 10, 'section_description': 'education', 'section_status': 2}, {'section_name': 'Work Experience', 'section_score': 6.0, 'section_total_score': 10, 'section_description': 'experience', 'section_status': 2}, {'section_name': 'Contact Detail', 'section_score': 10.0, 'section_total_score': 30, 'section_description': 'New Description', 'section_status': 1}, {'section_name': 'Skills', 'section_score': 7.0, 'section_total_score': 10, 'section_description': 'some description', 'section_status': 2}], 'error_message': ''}
    }
    // return{
    //     data:{'error_message':"Sorry Please Uplaod New Resume"}
    // }
}

const expertFormSubmit = (data) => {
    // return BaseApiService.post(`${siteDomain}/resume/api/v1/`, data, { defaultHeaders } , false, true);
    return {status_code : 200}
}

const checkSessionAvailability = () => {
    const url = 'session/';
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
}

const getCandidateId = () => {
    const url = `user-profile/`;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
}

const getCandidateResume = () => {
    const url = ``;
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
}

export const Api = {
    fileUpload,
    expertFormSubmit,
    checkSessionAvailability,
    getCandidateId,
    getCandidateResume
};