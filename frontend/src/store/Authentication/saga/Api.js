import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'

const fetchUserInform = (payload = { em: '' }) => {
    const url = '/api/v1/fetch-info/';
    return BaseApiService.post(`${siteDomain}${url}`, payload);
}

export default fetchUserInform;
