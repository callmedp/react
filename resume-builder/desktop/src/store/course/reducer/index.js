import {SAVE_USER_COURSE, REMOVE_COURSE} from "../actions/actionTypes";

export const initialState = {
    list: [{
        "candidate_id": '',
        "id": '',
        "name_of_certification": '',
        "year_of_certification": '',
    }]
};


export const courseReducer = (state = initialState, action) => {
    switch (action.type) {

        case SAVE_USER_COURSE: {
            return {
                ...state,
                ...action.data
            };
        }
        case REMOVE_COURSE: {
            return {
                ...state,
                ...{
                    list: state['list'].length === 1 ? initialState.list : state['list'].filter(item => item.id !== action.id)
                }
            }
        }
        default: {
            return state;
        }
    }
};

