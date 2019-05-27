import {SAVE_USER_PROJECT, REMOVE_PROJECT} from "../actions/actionTypes";

export const initialState = {
    list: [{
        "candidate_id": '',
        "id": '',
        "project_name": '',
        "start_date": '',
        "end_date": '',
        "description": ''
    }]
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
                    list: state['list'].length === 1 ? initialState.list : state['list'].filter(item => item.id !== action.id)
                }
            };
        }
        default: {
            return state;
        }
    }
};

