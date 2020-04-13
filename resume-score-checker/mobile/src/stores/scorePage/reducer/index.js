import { UPLOAD_FILE, UPDATE_SCORE } from "../actions/actionTypes";

const initState = {
    score : 0,
    section_score : []
}

export const uploadFileReducer = (state = initState, action) => {
    switch( action.type ){
        case UPDATE_SCORE :{
            return {
                ...state,
                ...{
                    score : action.score,
                    section_score : action.section_score
                }
            }
        }

        case UPLOAD_FILE :{
            return state
        }
        default : return state;
    }
}