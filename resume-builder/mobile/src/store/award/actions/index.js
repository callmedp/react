import {FETCH_USER_AWARD, UPDATE_USER_AWARD, DELETE_USER_AWARD, BULK_UPDTATE_USER_AWARD} from './actionTypes'


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

export const bulkUpdateUserAward = (payload) => {
    return {
        type: BULK_UPDTATE_USER_AWARD,
        payload
    }
}