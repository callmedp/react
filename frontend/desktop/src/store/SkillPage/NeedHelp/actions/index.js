import { SEND_LEAD_DATA } from './actionTypes';

const createLead = (payload) => {
    return {
        type : SEND_LEAD_DATA,
        payload
    }
}

export {
    createLead,

}