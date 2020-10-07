import {
    UPLOAD_FILE,
    UPDATE_SCORE,
    SUBMIT_EXPERT_FORM,
    CHECK_SESSION_AVAILABILITY,
    GET_CANDIDATE_ID,
    GET_CANDIDATE_RESUME,
    GET_CANDIDATE_INFO,
    GET_CANDIDATE_SCORE,
    GET_CART_COUNT
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

export const getCandidateScore = (payload) => {
    return    {
        type: GET_CANDIDATE_SCORE,
        payload
    }
    }
    
    export const getCandidateInfo = (payload) => ({
        type: GET_CANDIDATE_INFO,
        payload
    })

    export const getCartCount = () =>{
        return {
            type: GET_CART_COUNT
        }
    }