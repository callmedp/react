import {SAVE_USER_PROJECT} from "../actions/actionTypes";

const initialState = {
    "id": '',
    "candidate_id": '',
    "project_name": '',
    "start_date": '',
    "end_date": '',
    "skills": [],
    "description": '',
    'currently_working': false,
};


export const projectReducer = (state = initialState, action) => {
    switch (action.type) {

        case SAVE_USER_PROJECT: {
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

