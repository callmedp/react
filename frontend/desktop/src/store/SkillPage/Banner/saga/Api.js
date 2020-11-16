import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'


const skillPageBanner = (data) => {
    const url = `about/?id=${data?.id}`;
    return BaseApiService.get(`${siteDomain}/courses/api/v1/${url}`);
};


export default {
    skillPageBanner,
}