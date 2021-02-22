import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'


const skillPageBanner = (data) => {
    const code2 = data?.code2 || 'IN';
    const url = `about/${data?.id}/?code2=${code2}/`;
    return BaseApiService.get(`${siteDomain}/courses/api/v1/${url}`);
};


export default {
    skillPageBanner,
}