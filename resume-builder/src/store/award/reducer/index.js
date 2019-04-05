import {SAVE_USER_AWARD} from "../actions/actionTypes";

const initialState = {
    "candidate_id": '',
    "id": '',
    "title": '',
    "date": '',
    "summary": '',
};


export const awardReducer = (state = initialState, action) => {
    switch (action.type) {

        case SAVE_USER_AWARD: {
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

