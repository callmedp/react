import {SAVE_PRODUCT_IDS} from "../actions/actionTypes";

const initialState = {

    "ids":[],
};


export const getProductIdsReducer = (state = initialState, action) => {
    switch (action.type) {

        case SAVE_PRODUCT_IDS: {
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

