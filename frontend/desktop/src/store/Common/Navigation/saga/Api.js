import BaseApiService from 'services/BaseApiService'

import { siteDomain } from 'utils/domains'


const navOffersAndTags = (data) => {
    const url = `nav-offers-and-tags/`;
    return BaseApiService.get(`${siteDomain}/api/v1/${url}`);
};


export default {
    navOffersAndTags,
}