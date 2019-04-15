import {SAVE_USER_EXPERIENCE} from "../actions/actionTypes";

const initialState = {
    list: []
};


export const experienceReducer = (state = initialState, action) => {
    switch (action.type) {

        case SAVE_USER_EXPERIENCE: {
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

