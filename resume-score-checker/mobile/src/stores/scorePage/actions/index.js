import {
    UPLOAD_FILE,
    UPDATE_SCORE,
    SUBMIT_EXPERT_FORM,
    IMPORT_SHINE_RESUME,
    CHECK_SESSION_AVAILABILITY,
    GET_CANDIDATE_ID
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

export const checkSessionAvaialability = (payload) => ({
    type: CHECK_SESSION_AVAILABILITY,
    payload
})

export const getCandidateId = () => ({
    type: GET_CANDIDATE_ID
})

export const importResume = (payload) => ({
    type : IMPORT_SHINE_RESUME,
    payload
})