import {
    UPLOAD_FILE,
    UPDATE_SCORE,
    SUBMIT_EXPERT_FORM,
    CHECK_SESSION_AVAILABILITY,
    GET_CANDIDATE_ID,
    GET_CANDIDATE_RESUME
} from './actionTypes';


export const uploadFile = (payload) => ({
    type: UPLOAD_FILE,
    payload
});

export const updateScore = (payload) => ({
    type: UPDATE_SCORE,
    payload
})

export const expertForm = (payload) => ({
    type: SUBMIT_EXPERT_FORM,
    payload
})

export const checkSessionAvailability = (payload) => ({
    type: CHECK_SESSION_AVAILABILITY,
    payload
})

export const getCandidateId = (payload) => ({
    type: GET_CANDIDATE_ID,
    payload
})

export const getCandidateResume = (payload) => ({
    type: GET_CANDIDATE_RESUME,
    payload
})