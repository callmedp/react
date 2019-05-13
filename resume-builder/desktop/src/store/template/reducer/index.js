import {FETCH_TEMPLATE,SAVE_TEMPLATE} from "../actions/actionTypes";

const initialState = {
    'html': '',
    'template' :1
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
        default: {
            return state;
        }
    }
};

