import {GET_CANDIDATE_ID, LOGIN_CANDIDATE} from "./actionTypes";

export const getCandidateId = () => ({
    type: GET_CANDIDATE_ID
});


export const loginCandidate = (payload) => ({
    type: LOGIN_CANDIDATE,
    payload
});