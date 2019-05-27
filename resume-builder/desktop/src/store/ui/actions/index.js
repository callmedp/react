import {
    SHOW_TEMPLATE_MODAL,
    HIDE_TEMPLATE_MODAL,
    SHOW_SELECT_TEMPLATE_MODAL,
    HIDE_SELECT_TEMPLATE_MODAL,
    SELECT_CURRENT_FORM,
    SHOW_MORE_SECTION,
    SHOW_SUGGESTION_MODAL,
    HIDE_SUGGESTION_MODAL,
    SHOW_ALERT_MODAL,
    HIDE_ALERT_MODAL,
    SET_SUGGESTION_TYPE
} from "./actionTypes";


export const showModal = () => {
    return {
        type: SHOW_TEMPLATE_MODAL,
        data: {modal: true}
    }
}


export const showSuggestionModal = () => {
    return {
        type: SHOW_SUGGESTION_MODAL,
        data: {'suggestionModal': true}
    }
}


export const hideSuggestionModal = () => {
    return {
        type: HIDE_SUGGESTION_MODAL,
        data: {'suggestionModal': false}
    }
}

export const hideModal = () => {
    return {
        type: HIDE_TEMPLATE_MODAL,
        data: {modal: false}
    }
}


export const showSelectTemplateModal = () => {
    return {
        type: SHOW_SELECT_TEMPLATE_MODAL,
        data: {select_template_modal: true}
    }
}

export const hideSelectTemplateModal = () => {
    return {
        type: HIDE_SELECT_TEMPLATE_MODAL,
        data: {select_template_modal: false}
    }
}

export const currentForm = (payload) => {
    return {
        type: SELECT_CURRENT_FORM,
        data: payload
    }
}

export const showMoreSection = () => {
    return {
        type: SHOW_MORE_SECTION,
        data: {showMoreSection: true}
    }
}

export const hideMoreSection = () => {
    return {
        type: SHOW_MORE_SECTION,
        data: {showMoreSection: false}
    }
}
export const showAlertModal = (alertType) => {
    return {
        type: SHOW_ALERT_MODAL,
        data: {alertModal: true, alertType:alertType}
    }
}

export const hideAlertModal = () => {
    return {
        type: HIDE_ALERT_MODAL,
        data: {alertModal: false}
    }
}
export const setSuggestionType = (type) => {
    return {
        type: SET_SUGGESTION_TYPE,
        data: {suggestionType: type}
    }
}