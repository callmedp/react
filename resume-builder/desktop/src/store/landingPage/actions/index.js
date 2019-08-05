import {GET_CANDIDATE_ID, LOGIN_CANDIDATE, FEEDBACK_SUBMIT} from "./actionTypes";

export const getCandidateId = (payload) => ({
    type: GET_CANDIDATE_ID,
    payload
});


export const loginCandidate = (data) => ({
    type: LOGIN_CANDIDATE,
    data
});

export const feedbackSubmit = (payload) => ({
    type: FEEDBACK_SUBMIT,
    payload
});