import {FETCH_PERSONAL_INFO, UPDATE_PERSONAL_INFO, FETCH_IMAGE_URL,FETCH_INTEREST_LIST,UPDATE_SUMMARY_WITH_SUGGESTION} from './actionTypes';


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


export const fetchInterestList = (payload) => ({
    type: FETCH_INTEREST_LIST ,
    payload
});

export const upateSummaryWithSuggestion = (payload) => ({
    type: UPDATE_SUMMARY_WITH_SUGGESTION ,
    payload
});

