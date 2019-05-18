import {SAVE_USER_REFERENCE, REMOVE_REFERENCE} from "../actions/actionTypes";

const initialState = {
    list: [{
        "candidate_id": '',
        "id": '',
        "reference_name": '',
        "reference_designation": '',
        "about_user": "",
    }]
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
                    list: state['list'].length === 1 ? initialState.list : state['list'].filter(item => item.id !== action.id)
                }
            }
        }

        default: {
            return state;
        }
    }
};

