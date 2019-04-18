import {SAVE_USER_COURSE, REMOVE_COURSE} from "../actions/actionTypes";

const initialState = {
    list: [{
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
                    list: state['list'].filter(item => item.id !== action.id)
                }
            }
        }
        default: {
            return state;
        }
    }
};

