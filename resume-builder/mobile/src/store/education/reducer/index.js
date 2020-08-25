import {SAVE_USER_EDUCATION, REMOVE_EDUCATION} from "../actions/actionTypes";

const initialState = {
    list: []
};


export const educationReducer = (state = initialState, action) => {
    switch (action.type) {

        case SAVE_USER_EDUCATION: {
            return {
                ...state,
                ...action.data
            };
        }
        case REMOVE_EDUCATION: {
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

