import {FETCH_PERSONAL_INFO, SAVE_PERSONAL_INFO} from './actionTypes';


export const fetchPersonalInfo = () =>({
    type: FETCH_PERSONAL_INFO
});


export const savePersonalInfo = (payload) => ({
    type: SAVE_PERSONAL_INFO,
    data: payload
});

