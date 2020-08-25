import {GET_CANDIDATE_ID, LOGIN_CANDIDATE,FEEDBACK_SUBMIT, GET_HOME_COMPONENT_TITLE, CHECK_SESSION_AVAILABILITY, GET_CANDIDATE_SHINE_DETAILS} from "./actionTypes";

export const getCandidateId = () => ({
    type: GET_CANDIDATE_ID
});


export const loginCandidate = (data) => ({
    type: LOGIN_CANDIDATE,
    data
});

export const feedbackSubmit = (payload) => ({
    type: FEEDBACK_SUBMIT,
    payload
});


export const getComponentTitle = (payload) => ({
    type: GET_HOME_COMPONENT_TITLE,
    payload
});

export const getCandidateShineDetails = (payload) => ({
    type: GET_CANDIDATE_SHINE_DETAILS,
    payload
});


export const checkSessionAvaialability = (payload) => ({
    type: CHECK_SESSION_AVAILABILITY,
    payload
});