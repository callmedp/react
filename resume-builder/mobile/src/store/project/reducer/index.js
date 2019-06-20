import {SAVE_USER_PROJECT, REMOVE_PROJECT} from "../actions/actionTypes";

const initialState = {
    list: []
};


export const projectReducer = (state = initialState, action) => {
    switch (action.type) {

        case SAVE_USER_PROJECT: {
            return {
                ...state,
                ...action.data
            };
        }
        case REMOVE_PROJECT: {
            return {
                ...state,
                ...{
                    list: state['list'].filter(item => item.id !== action.id)
                }
            };
        }
        default: {
            return state;
        }
    }
};

