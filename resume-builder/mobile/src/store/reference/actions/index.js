import {FETCH_USER_REFERENCE, UPDATE_USER_REFERENCE} from './actionTypes'


export const fetchUserReference = () => {
    return {
        type: FETCH_USER_REFERENCE
    }
}

export const updateUserReference = (payload) => {
    return {
        type: UPDATE_USER_REFERENCE,
        payload
    }
}