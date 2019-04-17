import {FETCH_USER_LANGUAGE, UPDATE_USER_LANGUAGE} from './actionTypes'


export const fetchUserLanguage = () => {
    return {
        type: FETCH_USER_LANGUAGE
    }
}

export const updateUserLanguage = (payload) => {
    return {
        type: UPDATE_USER_LANGUAGE,
        payload
    }
}