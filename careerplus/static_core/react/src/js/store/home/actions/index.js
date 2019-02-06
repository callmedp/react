import {
    FETCH_HOME_DATA, SAVE_HOME_DATA
} from "./actionTypes";

export const fetchHomeData = () => ({
    type: FETCH_HOME_DATA
})

export const saveHomeData = (data) => ({
    type: SAVE_HOME_DATA,
    data
})
