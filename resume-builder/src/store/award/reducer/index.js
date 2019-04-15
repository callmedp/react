import {SAVE_USER_AWARD, REMOVE_AWARD} from "../actions/actionTypes";

const initialState = {
    list: []
};


export const awardReducer = (state = initialState, action) => {
    switch (action.type) {

        case SAVE_USER_AWARD: {
            return {
                ...state,
                ...action.data
            };
        }
        case REMOVE_AWARD: {
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

