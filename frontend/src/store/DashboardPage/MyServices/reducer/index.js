import * as Actions from '../actions/actionTypes';

const initState = {
    data: [],
    pending_resume_items: [],
    page: {},
}

export const DashboardMyServicesReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.MY_SERVICES_FETCHED : return { ...initState,...action.item}

        case Actions.GET_OI_COMMENT: {
            return { ...state, };
        }

        case Actions.OI_COMMENT_SUCCESS: {
            const oi_detail = state.oi_comment ? [...state.oi_comment] : [];
            const action_detail = action.oi_comment ? [action.oi_comment] : [];
            return {
                ...state, oi_comment: [...oi_detail.filter((item) => item.id !== action.oi_comment.id), ...action_detail], loading: false, oi_comment_loading: false,
            }
        }
        
        case Actions.OI_COMMENT_FAILED: {
            return {
                ...state, oi_comment_loading: false, oi_comment_error: 'Something went Wrong'
            }
        }

        case Actions.FETCH_MY_REVIEWS: {
            return { ...state, ...action.item, loading: false, };
        }

        case Actions.SUBMIT_DASHBOARD_SUCCESS: {
            const review_detail = state.reviews ? [...state.reviews] : [];
            const rev_action_detail = action.reviews ? [action.reviews] : [];
            return {
                ...state, reviews: [...review_detail.filter((item) => item.product !== action.reviews.object_id), ...rev_action_detail], loading: false, 
            }
        }

        case Actions.SUBMIT_DASHBOARD_FAILED: {
            return {
                ...state, ...action.item
            }
        }

        default: return state;
    }
}

const commentInitState = {
    comment: [],
}

export const CommentReducer = (state=commentInitState, action) => {
    switch(action.type){
        

        default: return state;
    }
}