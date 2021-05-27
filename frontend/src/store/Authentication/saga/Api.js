import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'

const fetchUserInform = (payload = { em: '' }) => {
    const url = '/api/v1/fetch-info/';
    return BaseApiService.post(`${siteDomain}${url}`, payload);
}

const chatbotScriptApi = () => {
    let url = "";

    url = `${siteDomain}/chatbot/api/app/learning_course_non_loggedIn/get-script/`;
    // else url = `https://chat.shine.com/chatbot/api/app/learning_course_non_loggedIn/get-script/`;

    return BaseApiService.get(url);
}

export default {
    fetchUserInform,
    chatbotScriptApi
}
