import {FETCH_TEMPLATE, SAVE_TEMPLATE, SET_SELECTED_TEMPLATE} from "../actions/actionTypes";

const initialState = {
    'html': '',
    'template': 1,
    'templateId': 1
};


export const templateReducer = (state = initialState, action) => {
    switch (action.type) {
        case FETCH_TEMPLATE: {
            return {
                ...state,
                ...action.data
            }
        }
        case SAVE_TEMPLATE: {
            return {
                ...state,
                ...action.data
            }
        }
        case SET_SELECTED_TEMPLATE: {
            return {
                ...state,
                ...{
                    templateId: action.templateId
                }
            }
        }
        default: {
            return state;
        }
    }
};

