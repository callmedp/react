import {SAVE_USER_SKILL, REMOVE_SKILL} from "../actions/actionTypes";

export const initialState = {
    list: [{
        "candidate_id": '',
        "id": '',
        "name": '',
        "proficiency": 5
    }]
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
                    list: state['list'].length === 1 ? initialState.list : state['list'].filter(item => item.id !== action.id)
                }
            }
        }

        default: {
            return state;
        }
    }
};

