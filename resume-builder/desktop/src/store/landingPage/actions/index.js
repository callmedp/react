import {GET_CANDIDATE_ID, LOGIN_CANDIDATE, FEEDBACK_SUBMIT, GET_HOME_COMPONENT_TITLE, GET_CANDIDATE_SHINE_DETAILS, CHECK_SESSION_AVAILABILITY} from "./actionTypes";

export const getCandidateId = (payload) => ({
    type: GET_CANDIDATE_ID,
    payload
});


export const loginCandidate = (data) => ({
    type: LOGIN_CANDIDATE,
    data
});


export const getCandidateShineDetails = (payload) => ({
    type: GET_CANDIDATE_SHINE_DETAILS,
    payload
});


export const feedbackSubmit = (payload) => ({
    type: FEEDBACK_SUBMIT,
    payload
});

export const getComponentTitle = (payload) => ({
    type: GET_HOME_COMPONENT_TITLE,
    payload
});


export const checkSessionAvaialability = (payload) => ({
    type: CHECK_SESSION_AVAILABILITY,
    payload
});


