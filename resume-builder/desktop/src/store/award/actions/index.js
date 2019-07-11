import {
    FETCH_USER_AWARD,
    UPDATE_USER_AWARD,
    DELETE_USER_AWARD,
    BULK_U_C_USER_AWARD,
    HANDLE_AWARD_SWAP
} from './actionTypes'


export const fetchUserAward = () => {
    return {
        type: FETCH_USER_AWARD
    }
}
export const updateUserAward = (payload) => {
    return {
        type: UPDATE_USER_AWARD,
        payload
    }
}

export const deleteAward = (awardId) => {
    return {
        type: DELETE_USER_AWARD,
        awardId
    }
}


export const bulkUpdateOrCreateUserAward = (payload) => {
    return {
        type: BULK_U_C_USER_AWARD,
        payload
    }
}


export const handleAwardSwap = (payload) => {
    return {
        type: HANDLE_AWARD_SWAP,
        payload
    }
}