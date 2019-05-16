import {
    UPDATE_UI, SHOW_TEMPLATE_MODAL,
    HIDE_TEMPLATE_MODAL,
    SHOW_SELECT_TEMPLATE_MODAL,
    HIDE_SELECT_TEMPLATE_MODAL,
    SELECT_CURRENT_FORM
} from "../actions/actionTypes";

const initialState = {
    'loader': false,
    'modal': false,
    'select_template_modal': false,
    'formName': ''
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

        default: {
            return state;
        }
    }
};

