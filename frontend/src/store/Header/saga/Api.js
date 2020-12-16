import BaseApiService from 'services/BaseApiService';
import { siteDomain } from 'utils/domains';

const sessionAvailability = () => {
    const url = 'session/';
    return BaseApiService.get(`${siteDomain}/api/v1/resume/${url}`);
}

const cartCount = () => {
    const url = `count/`;
    return BaseApiService.get(`${siteDomain}/api/v1/cart/${url}`);
}

const candidateInformation = ({ candidateId }) => {
    const url = `candidate-login/${candidateId}`;
    return BaseApiService.get(`${siteDomain}/api/v1/${url}`, {
        "Content-Type": "application/json",
        'Authorization': ''
    })
}

const navOffersAndTags = (data) => {
    const url = `nav-offers-and-tags/`;
    return BaseApiService.get(`${siteDomain}/api/v1/${url}`);
};


export default {
    sessionAvailability,
    cartCount,
    candidateInformation,
    navOffersAndTags,
}


