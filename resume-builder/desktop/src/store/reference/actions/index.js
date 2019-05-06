import {
    FETCH_USER_REFERENCE, UPDATE_USER_REFERENCE, DELETE_USER_REFERENCE,
    HANDLE_REFERENCE_SWAP, BULK_U_C_USER_REFERENCE
} from './actionTypes'
import {BULK_U_C_USER_SKILL} from "../../skill/actions/actionTypes";


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


export const bulkUpdateOrCreateUserReference = (payload) => {
    return {
        type: BULK_U_C_USER_REFERENCE,
        payload
    }
}
export const handleReferenceSwap = (payload) => {
    return {
        type: HANDLE_REFERENCE_SWAP,
        payload
    }
}