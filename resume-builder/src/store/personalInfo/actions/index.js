import {FETCH_PERSONAL_INFO, UPDATE_PERSONAL_INFO, FETCH_IMAGE_URL} from './actionTypes';


export const fetchPersonalInfo = () => ({
    type: FETCH_PERSONAL_INFO
});


export const updatePersonalInfo = (payload) => ({
    type: UPDATE_PERSONAL_INFO,
    payload
});


export const fetchImageUrl = (payload) => ({
    type: FETCH_IMAGE_URL,
    payload
});

