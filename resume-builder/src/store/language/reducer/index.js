import {SAVE_USER_LANGUAGE} from "../actions/actionTypes";

const initialState = {
    list: []
};


export const languageReducer = (state = initialState, action) => {
    switch (action.type) {
        case SAVE_USER_LANGUAGE: {
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

