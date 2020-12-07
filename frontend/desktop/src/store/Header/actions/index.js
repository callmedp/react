import * as Actions from './actionTypes';

export const sessionAvailability = (payload) => ({
    type: Actions.FETCH_SESSION_AVAILABILITY,
    payload
})

export const cartCount = () =>{
    return {
        type: Actions.FETCH_CART_COUNT
    }
}

export const getCandidateInfo = (payload) => ({
    type: Actions.FETCH_CANDIDATE_INFO,
    payload
})