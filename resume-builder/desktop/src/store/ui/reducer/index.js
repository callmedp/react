import {
    UPDATE_UI, SHOW_TEMPLATE_MODAL,
    HIDE_TEMPLATE_MODAL,
    SHOW_SELECT_TEMPLATE_MODAL,
    HIDE_SELECT_TEMPLATE_MODAL,
    SELECT_CURRENT_FORM,
    SHOW_MORE_SECTION,
    HIDE_MORE_SECTION,
    SHOW_SUGGESTION_MODAL,
    HIDE_SUGGESTION_MODAL,
    SHOW_ALERT_MODAL,
    HIDE_ALERT_MODAL,
    SAVE_SUGGESTIONS,
    SET_SUGGESTION_TYPE,
    UPDATE_PREVIEW_CLICK_STATUS,
    SHOW_GENERATE_RESUME_MODAL,
    HIDE_GENERATE_RESUME_MODAL,
    HIDE_HELP_MODAL,
    SHOW_HELP_MODAL
} from "../actions/actionTypes";

const initialState = {
    'loader': false,
    'modal': false,
    'select_template_modal': false,
    'formName': '',
    'showMoreSection': false,
    'suggestionModal': false,
    'alertModal': false,
    'alertType': 'error',
    'generateResumeModal':false,
    'suggestions': [],
    'suggestionType': 'experience',
    'previewClicked' : false,
    'helpModal': false,
};

export const uiReducer = (state = initialState, action) => {
    switch (action.type) {
        case UPDATE_UI: {
            return {
                ...state,
                ...action.data
            }
        }
        case SHOW_TEMPLATE_MODAL: {
            return {
                ...state,
                ...action.data
            }
        }
        case HIDE_TEMPLATE_MODAL: {
            return {
                ...state,
                ...action.data
            }
        }
        case SHOW_SELECT_TEMPLATE_MODAL: {
            return {
                ...state,
                ...action.data
            }
        }
        case HIDE_SELECT_TEMPLATE_MODAL: {
            return {
                ...state,
                ...action.data
            }
        }
        case SELECT_CURRENT_FORM: {
            return {
                ...state,
                ...action.data
            }
        }
        case SHOW_MORE_SECTION: {
            return {
                ...state,
                ...action.data
            }
        }
        case HIDE_MORE_SECTION: {
            return {
                ...state,
                ...action.data
            }
        }
        case SHOW_SUGGESTION_MODAL: {
            return {
                ...state,
                ...action.data
            }
        }
        case HIDE_SUGGESTION_MODAL: {
            return {
                ...state,
                ...action.data
            }
        }
        case SHOW_ALERT_MODAL: {
            return {
                ...state,
                ...action.data
            }
        }
        case HIDE_ALERT_MODAL: {
            return {
                ...state,
                ...action.data
            }
        }
        case SHOW_GENERATE_RESUME_MODAL: {
            return {
                ...state,
                ...action.data
            }
        }
        case HIDE_GENERATE_RESUME_MODAL: {
            return {
                ...state,
                ...action.data
            }
        }
        case SAVE_SUGGESTIONS: {
            return {
                ...state,
                ...action.data
            }
        }
        case SET_SUGGESTION_TYPE: {
            return {
                ...state,
                ...action.data
            }
        }
        case UPDATE_PREVIEW_CLICK_STATUS: {
            return {
                ...state,
                ...action.data
            }
        }
         case SHOW_HELP_MODAL: {
            return {
                ...state,
                ...action.data
            }
        }
        case HIDE_HELP_MODAL: {
            return {
                ...state,
                ...action.data
            }
        }

        default: {
            return state;
        }
    }
};

