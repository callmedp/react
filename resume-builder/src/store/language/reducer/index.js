import {SAVE_USER_LANGUAGE, REMOVE_LANGUAGE} from "../actions/actionTypes";

const initialState = {
    list: []
};


export const languageReducer = (state = initialState, action) => {
    switch (action.type) {
        case SAVE_USER_LANGUAGE: {
            return {
                ...state,
                ...action.data
            }
        }
        case REMOVE_LANGUAGE: {
            return {
                ...state,
                ...{
                    list: state.filter(item => item.id !== action.id)
                }
            }
        }

        default: {
            return state;
        }
    }
};

