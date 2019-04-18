import {FETCH_USER_LANGUAGE, UPDATE_USER_LANGUAGE, DELETE_USER_LANGUAGE, BULK_UPDATE_USER_LANGUAGE,} from './actionTypes'


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

export const deleteLanguage = (languageId) => {
    return {
        type: DELETE_USER_LANGUAGE,
        languageId
    }
}

export const bulkUpdateUserLanguage = (payload) => {
    return {
        type: BULK_UPDATE_USER_LANGUAGE,
        payload
    }
}