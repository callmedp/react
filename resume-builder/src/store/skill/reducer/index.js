import {SAVE_USER_SKILL, REMOVE_SKILL} from "../actions/actionTypes";

const initialState = {
    list: []
};


export const skillReducer = (state = initialState, action) => {
    switch (action.type) {
        case SAVE_USER_SKILL: {
            return {
                ...state,
                ...action.data
            }
        }
        case REMOVE_SKILL: {
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

