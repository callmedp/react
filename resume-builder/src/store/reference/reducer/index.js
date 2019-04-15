import {SAVE_USER_REFERENCE} from "../actions/actionTypes";

const initialState = {
    list: []
};


export const referenceReducer = (state = initialState, action) => {
    switch (action.type) {

        case SAVE_USER_REFERENCE: {
            return {
                ...state,
                ...action.data
            };
        }
        default: {
            return state;
        }
    }
};

