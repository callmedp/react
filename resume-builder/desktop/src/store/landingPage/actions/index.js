import {GET_CANDIDATE_ID, LOGIN_CANDIDATE, FEEDBACK_SUBMIT} from "./actionTypes";

export const getCandidateId = () => ({
    type: GET_CANDIDATE_ID
});


export const loginCandidate = (payload) => ({
    type: LOGIN_CANDIDATE,
    payload
});

export const feedbackSubmit = (payload) => ({
    type: FEEDBACK_SUBMIT,
    payload
});