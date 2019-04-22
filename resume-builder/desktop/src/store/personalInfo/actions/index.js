import {FETCH_PERSONAL_INFO, UPDATE_PERSONAL_INFO, FETCH_IMAGE_URL, UPDATE_ENTITY_PREFERENCE} from './actionTypes';


export const fetchPersonalInfo = () => ({
    type: FETCH_PERSONAL_INFO
});


export const updatePersonalInfo = (payload) => ({
    type: UPDATE_PERSONAL_INFO,
    payload
});


export const updateEntityPreference = (payload) => ({
    type: UPDATE_ENTITY_PREFERENCE,
    payload
})
export const fetchImageUrl = (payload) => ({
    type: FETCH_IMAGE_URL,
    payload
});

