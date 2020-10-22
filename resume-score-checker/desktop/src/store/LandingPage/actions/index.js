import {
    UPLOAD_FILE_URL,EXPERT_FORM_SUBMIT,CHECK_SESSION_AVAILABILITY,
    GET_CANDIDATE_ID,GET_CANDIDATE_RESUME, GET_CANDIDATE_SCORE, GET_CANDIDATE_INFO, GET_CART_COUNT  
} from './actionTypes';


export const uploadFileUrl = (payload) =>({
    type : UPLOAD_FILE_URL,
    payload
})

export const expertFormSubmit = (payload) =>({
    type : EXPERT_FORM_SUBMIT,
    payload
})


export const checkSessionAvailability = (payload) => ({
    type: CHECK_SESSION_AVAILABILITY,
    payload
})

export const getCandidateId = (payload) => ({
    type: GET_CANDIDATE_ID,
    payload
});

export const getCandidateResume = (payload) => ({
    type : GET_CANDIDATE_RESUME,
    payload
})

export const getCandidateScore = (payload) => {
return    {
    type: GET_CANDIDATE_SCORE,
    payload
}
}

export const getCartCount = () =>{
    return {
        type: GET_CART_COUNT
    }
}

export const getCandidateInfo = (payload) => ({
    type: GET_CANDIDATE_INFO,
    payload
})