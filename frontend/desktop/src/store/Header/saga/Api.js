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

const candidateInformation = () => {
    const url = 'candidate-login/?with_info=false';
    return BaseApiService.get(`${siteDomain}/api/v1/${url}`, {
        "Content-Type": "application/json",
        'Authorization': ''
    })
}


export default {
    sessionAvailability,
    cartCount,
    candidateInformation
}


