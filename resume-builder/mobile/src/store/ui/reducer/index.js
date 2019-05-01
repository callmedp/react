import {UPDATE_UI} from "../actions/actionTypes";

const initialState = {
    'mainloader': true,
    'dataloader': false
};

export const uiReducer = (state = initialState, action) => {
    switch (action.type) {
        case UPDATE_UI: {
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

