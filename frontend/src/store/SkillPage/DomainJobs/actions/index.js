import { FETCH_DOMAIN_JOBS  } from './actionTypes';

const fetchDomainJobs = (payload) => {
    return {
        type : FETCH_DOMAIN_JOBS,
        payload
    }
}

export {
    fetchDomainJobs,
}