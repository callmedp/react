import {
    UPDATE_MAIN_PAGE_LOADER,
    UPDATE_DATA_LOADER,
    FETCH_LOADER_STATUS,
    CHANGE_FORM_NAME,
    SET_SUGGESTION_TYPE,
    FETCH_ALERT_MODAL_STATUS,
    UPDATE_ALERT_MODAL_STATUS,
    SHOW_GENERATE_RESUME_MODAL,
    HIDE_GENERATE_RESUME_MODAL,
    SHOW_HELP_MODAL,
    HIDE_HELP_MODAL
} from './actionTypes'


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
export const showGenerateResumeModal = () => {
    return {
        type: SHOW_GENERATE_RESUME_MODAL,
        data: {'generateResumeModal': true}
    }
}

export const hideGenerateResumeModal = () => {
    return {
        type: HIDE_GENERATE_RESUME_MODAL,
        data: {'generateResumeModal': true}
    }
}

export const showHelpModal = () => {
    return {
        type: SHOW_HELP_MODAL,
        data: {helpModal: true}
    }
}

export const hideHelpModal = () => {
    return {
        type: HIDE_HELP_MODAL,
        data: {helpModal: false}
    }
}
