import {FETCH_PERSONAL_INFO, UPDATE_PERSONAL_INFO} from './actionTypes';


export const fetchPersonalInfo = () => ({
    type: FETCH_PERSONAL_INFO
});


export const updatePersonalInfo = (payload) => ({
    type: UPDATE_PERSONAL_INFO,
    payload
});

