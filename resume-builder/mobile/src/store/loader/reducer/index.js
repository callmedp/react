import {UPDATE_MAIN_PAGE_LOADER,UPDATE_DATA_LOADER} from "../actions/actionTypes";

const initialState = {
    'mainloader': true,
    'dataloader': false
};

export const loaderReducer = (state = initialState, action) => {
    switch (action.type) {
        case UPDATE_MAIN_PAGE_LOADER: {
            return {
                ...state,
                ...action.payload
            }
        }
        case UPDATE_DATA_LOADER: {
            return {
                ...state,
                ...action.payload
            }
        }
        default: {
            return state;
        }
    }
};

