import { UPLOAD_FILE, UPDATE_SCORE } from "../actions/actionTypes";

const initState = {
    'total_score' : 0,
    'section_score' : [],
    'error_message' : '',
    'cartCount': 0
}

export const uploadFileReducer = (state = initState, action) => {
    switch( action.type ){
        case UPDATE_SCORE :{
            return {
                ...state,
                ...action.payload
            }
        }

        case UPLOAD_FILE :{
            return state
        }
        default : return state;
    }
}