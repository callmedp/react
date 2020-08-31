import {FETCH_USER_REFERENCE, UPDATE_USER_REFERENCE, DELETE_USER_REFERENCE, BULK_UPDATE_USER_REFERENCE} from './actionTypes'


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

export const deleteReference = (referenceId) => {
    return {
        type: DELETE_USER_REFERENCE,
        referenceId
    }
}

export const bulkUpdateUserReference = (payload) => {
    return {
        type: BULK_UPDATE_USER_REFERENCE,
        payload
    }
}