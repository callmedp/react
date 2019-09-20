import {GET_CANDIDATE_ID, LOGIN_CANDIDATE,FEEDBACK_SUBMIT, GET_HOME_COMPONENT_TITLE} from "./actionTypes";
import {GET_HOME_COMPONENT_TITLE} from "../../../../../desktop/src/store/landingPage/actions/actionTypes";

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