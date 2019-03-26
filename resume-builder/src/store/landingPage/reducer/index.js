import {FETCH_SHINE_PROFILE} from "../actions/actionTypes";

const initialState = {
    userId: ''
};


export const landingPageReducer = (state = initialState, action) => {
    switch (action.type) {

        case FETCH_SHINE_PROFILE: {
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
