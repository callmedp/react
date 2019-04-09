import {SAVE_USER_SKILL} from "../actions/actionTypes";

const initialState = {
    "id": '',
    "candidate_id": '',
    "name": '',
    "proficiency": ''
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

