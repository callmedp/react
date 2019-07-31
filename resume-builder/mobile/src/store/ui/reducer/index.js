import {
    UPDATE_MAIN_PAGE_LOADER,
    UPDATE_DATA_LOADER,
    CHANGE_FORM_NAME,
    SAVE_SUGGESTIONS,
    SET_SUGGESTION_TYPE,
    UPDATE_ALERT_MODAL_STATUS,
    SHOW_GENERATE_RESUME_MODAL,
    HIDE_GENERATE_RESUME_MODAL,
    SHOW_HELP_MODAL,
    HIDE_HELP_MODAL,
} from "../actions/actionTypes";

const initialState = {
    'mainloader': true,
    'dataloader': false,
    'formName': '',
    'suggestions': [],
    'suggestionType': 'experience',
    'alertModalStatus': false,
    'generateResumeModal': false,
    'helpModal': false,
};

export const uiReducer = (state = initialState, action) => {
    switch (action.type) {
        case UPDATE_MAIN_PAGE_LOADER: {
            return {
                ...state,
                ...action.payload
            }
        }
        case UPDATE_DATA_LOADER: {
            return {
                ...state,
                ...action.payload
            }
        }
        case CHANGE_FORM_NAME: {
            return {
                ...state,
                ...action.payload
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
        case UPDATE_ALERT_MODAL_STATUS: {
            return {
                ...state,
                ...{
                    alertModalStatus: action.payload
                }
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

