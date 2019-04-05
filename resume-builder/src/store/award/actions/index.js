import {FETCH_USER_AWARD, UPDATE_USER_AWARD} from './actionTypes'


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