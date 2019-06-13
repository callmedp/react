import {UPDATE_MAIN_PAGE_LOADER,UPDATE_DATA_LOADER,FETCH_LOADER_STATUS,CHANGE_FORM_NAME,SET_SUGGESTION_TYPE,FETCH_ALERT_MODAL_STATUS,UPDATE_ALERT_MODAL_STATUS} from './actionTypes'


export const updateMainLoader = (payload) => {
    return {
        type: UPDATE_MAIN_PAGE_LOADER,
        payload
    }
}

export const updateDataLoader = (payload) => {
    return {
        type: UPDATE_DATA_LOADER,
        payload
    }
}

export const fetchLoaderStatus = () => {
    return {
        type: FETCH_LOADER_STATUS,
    }
}

export const changeFormName = (payload) => {
    return {
        type: CHANGE_FORM_NAME,
        payload
    }
}

export const setSuggestionType = (type) => {
    return {
        type: SET_SUGGESTION_TYPE,
        data: {suggestionType: type}
    }
}

export const fetchAlertModalStatus = () =>{
    return {
        type: FETCH_ALERT_MODAL_STATUS
    }
}

export const updateAlertModalStatus = (payload) =>{
    return {
        type: UPDATE_ALERT_MODAL_STATUS,
        payload
    }
}