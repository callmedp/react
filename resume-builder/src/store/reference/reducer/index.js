import {SAVE_USER_REFERENCE, REMOVE_REFERENCE} from "../actions/actionTypes";

const initialState = {
    list: []
};


export const referenceReducer = (state = initialState, action) => {
    switch (action.type) {

        case SAVE_USER_REFERENCE: {
            return {
                ...state,
                ...action.data
            };
        }
        case REMOVE_REFERENCE: {
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

