import {UPDATE_SCORE} from "../actions/actionTypes";

const initialState = {
    total_score : 0,
    section_score : [],
    error_message : '',
    cartCount: 0
};


export const landingPageReducer = (state = initialState, action) => {
    switch (action.type) {
        case UPDATE_SCORE : {
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
