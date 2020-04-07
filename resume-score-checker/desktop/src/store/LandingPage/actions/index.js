import {
    UPLOAD_FILE_URL,EXPERT_FORM_SUBMIT,CHECK_SESSION_AVAILABILITY,GET_CANDIDATE_ID
} from './actionTypes';


export const uploadFileUrl = (payload) =>({
    type : UPLOAD_FILE_URL,
    payload
})

export const expertFormSubmit = (payload) =>({
    type : EXPERT_FORM_SUBMIT,
    payload
})


export const checkSessionAvaialability = (payload) => ({
    type: CHECK_SESSION_AVAILABILITY,
    payload
})

export const getCandidateId = (payload) => ({
    type: GET_CANDIDATE_ID,
    payload
});
