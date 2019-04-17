import {SAVE_TEMPLATE} from "../actions/actionTypes";

const initialState = {
    'html': ''
};


export const templateReducer = (state = initialState, action) => {
    switch (action.type) {
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

