import {SAVE_USER_LANGUAGE, REMOVE_LANGUAGE} from "../actions/actionTypes";

const initialState = {
    list: [{
        "candidate_id": '',
        "id": '',
        "name": '',
        "proficiency": {
            value: 5, 'label': '5'
        },
        order: 0
        }
    ]
};


export const languageReducer = (state = initialState, action) => {
    switch (action.type) {
        case SAVE_USER_LANGUAGE: {
            return {
                ...state,
                ...action.data
            }
        }
        case REMOVE_LANGUAGE: {
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

