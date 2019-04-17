import {SAVE_USER_COURSE} from "../actions/actionTypes";

const initialState = {
    'id': '',
    'candidate_id': '',
    "name_of_certification": '',
    "year_of_certification": '',
};


export const courseReducer = (state = initialState, action) => {
    switch (action.type) {

        case SAVE_USER_COURSE: {
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

