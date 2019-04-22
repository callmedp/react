import {SAVE_TEMPLATE,UPDATE_MODAL_STATUS} from "../actions/actionTypes";

const initialState = {
    'html': '',
    'modal_status': false
};


export const templateReducer = (state = initialState, action) => {
    switch (action.type) {
        case SAVE_TEMPLATE: {
            return {
                ...state,
                ...action.data
            }
        }
        case UPDATE_MODAL_STATUS: {
            return {
                ...state,
                ...action.payload
            }
        }

        default: {
            return state;
        }
    }
};

