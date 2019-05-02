import {UPDATE_UI, SHOW_TEMPLATE_MODAL, HIDE_TEMPLATE_MODAL} from "../actions/actionTypes";

const initialState = {
    'loader': false,
    'modal': false
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
        default: {
            return state;
        }
    }
};

