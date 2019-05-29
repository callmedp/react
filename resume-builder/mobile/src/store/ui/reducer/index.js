import {UPDATE_MAIN_PAGE_LOADER,UPDATE_DATA_LOADER,CHANGE_FORM_NAME,SAVE_SUGGESTIONS,SET_SUGGESTION_TYPE} from "../actions/actionTypes";

const initialState = {
    'mainloader': true,
    'dataloader': false,
    'formName' : '',
    'suggestions': [],
    'suggestionType': 'experience'
};

export const uiReducer = (state = initialState, action) => {
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
        case CHANGE_FORM_NAME: {
            return {
                ...state,
                ...action.payload
            }
        }
        case SAVE_SUGGESTIONS: {
            return {
                ...state,
                ...action.data
            }
        }
        case SET_SUGGESTION_TYPE: {
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

