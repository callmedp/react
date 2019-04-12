import {SAVE_USER_SKILL} from "../actions/actionTypes";

const initialState = {
    list: []
};


export const skillReducer = (state = initialState, action) => {
    switch (action.type) {
        case SAVE_USER_SKILL: {
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

