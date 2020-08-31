import {FETCH_USER_LANGUAGE, UPDATE_USER_LANGUAGE, BULK_U_C_USER_LANGUAGE,
    DELETE_USER_LANGUAGE, HANDLE_LANGUAGE_SWAP,} from './actionTypes'


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


export const bulkUpdateOrCreateUserLanguage = (payload) => {
    return {
        type: BULK_U_C_USER_LANGUAGE,
        payload
    }
}

export const handleLanguageSwap = (payload) => {
    return {
        type: HANDLE_LANGUAGE_SWAP,
        payload
    }
}