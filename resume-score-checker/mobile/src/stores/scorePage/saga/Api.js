import BaseApiService from '../../../services/BaseApiService';
import { siteDomain, shineSite } from '../../../Utils/domains';

const defaultHeaders = {}

const fileUpload = (data) => {
    const url = `resume-score-checker/get-score/`
    return BaseApiService.post(`${shineSite}/${url}`, data, defaultHeaders, false, true);
    // return {
    //     data :{'total_score': 32, 'section_score': [{'section_name': 'Format/Style', 'section_score': 2.0, 'section_total_score': 10, 'section_description': 'format style', 'section_status': 1, 'section_message': 'New section msg added'}, {'section_name': 'Summary & Objective', 'section_score': 2.5, 'section_total_score': 10, 'section_description': 'summary', 'section_status': 0, 'section_message': 'Changed'}, {'section_name': 'Education Detail', 'section_score': 5.0, 'section_total_score': 10, 'section_description': 'education', 'section_status': 2, 'section_message': 'New section msg added'}, {'section_name': 'Work Experience', 'section_score': 6.0, 'section_total_score': 10, 'section_description': 'experience', 'section_status': 2, 'section_message': 'New section msg added'}, {'section_name': 'Contact Detail', 'section_score': 10.0, 'section_total_score': 30, 'section_description': 'New Description', 'section_status': 1, 'section_message': 'New section msg added'}, {'section_name': 'Skills', 'section_score': 7.0, 'section_total_score': 10, 'section_description': 'some description', 'section_status': 2, 'section_message': 'New section msg added'}], 'error_message': ''}
    // }
}

const getInformation = () => {
    const url = 'candidate-login/?with_info=false';
    return BaseApiService.get(`${siteDomain}/api/v1/${url}`, {
        "Content-Type": "application/json",
        'Authorization': ''
    })
}

const getCandidateScore = (candidateId) => {
    const url = `resume-score-checker/get-score/?candidate_id=${candidateId}`;
    return BaseApiService.get(`${shineSite}/${url}`)
}

const expertFormSubmit = (data) => {
    const url = `lead/lead-management/`;
    return BaseApiService.post(`${siteDomain}/${url}`, data, {
        'Content-Type': 'application/x-www-form-urlencoded'
    }, false);
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

const getCartCount = () => {
    const url = `count/`;
    return BaseApiService.get(`${siteDomain}/api/v1/cart/${url}`);
}


export const Api = {
    fileUpload,
    expertFormSubmit,
    checkSessionAvailability,
    getCandidateId,
    getCandidateResume,
    getCandidateScore,
    getInformation,
    getCartCount
};