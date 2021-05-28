import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'

const fetchUserInform = (payload = { em: '' }) => {
    const url = '/api/v1/fetch-info/';
    return BaseApiService.post(`${siteDomain}${url}`, payload);
}

const chatbotScriptApi = () => {
    let url = "";

    if(localStorage.getItem('candidateId')) url = `${siteDomain}/chatbot/api/app/learning_course_page/get-script`;
    else url = `${siteDomain}/chatbot/api/app/learning_course_non_loggedIn/get-script/`;

    return BaseApiService.get(url);
}

export default {
    fetchUserInform,
    chatbotScriptApi
}
