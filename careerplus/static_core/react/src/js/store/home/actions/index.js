import {
    FETCH_HOME_DATA, SAVE_USER_DETAILS
} from "./actionTypes";

export const fetchHomeData = () => ({
    type: FETCH_HOME_DATA
})

export const saveUserDetails = (payload) => ({
    type: SAVE_USER_DETAILS,
    payload
})
