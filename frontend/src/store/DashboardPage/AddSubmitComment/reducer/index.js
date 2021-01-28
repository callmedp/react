import * as Actions from '../actions/actionTypes';

const initState = {
    comment: [],
}

export const CommentReducer = (state = initState, action) => {
    switch(action.type){
        case Actions.OI_COMMENT_FETCHED: {
            return { ...state, ...action.comment };
        }

        default: return state;
    }
}
