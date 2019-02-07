import {
    FETCH_HOME_DATA, SAVE_USER_DETAILS, UPDATE_USER_DETAILS
} from "./actionTypes";

export const fetchHomeData = () => ({
    type: FETCH_HOME_DATA
})

export const saveUserDetails = (payload) => ({
    type: SAVE_USER_DETAILS,
    payload
})

export const updateUserDetails = (payload) => ({
    type: UPDATE_USER_DETAILS,
    payload
})
