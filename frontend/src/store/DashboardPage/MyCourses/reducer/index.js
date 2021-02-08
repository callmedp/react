import * as Actions from '../actions/actionTypes';

const initState = {
    myCourses : [],
    page : {}
}

const updateComment = (state, {payload}) => {
    const updatedState = state.data.map((item) => {
        if(item.id === payload.id){
            return {...item, no_of_comments: payload.no_of_comments }
        }
        else {
            return { ...item };
        }
    })
    return {...state, data : updatedState}; 
}

export const DashboardMyCoursesReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.MY_COURSES_FETCHED : return { ...initState,...action.item}
        case Actions.UPDATE_COURSE_COMMENT_COUNT : return updateComment(state, action)
        default: return state;
    }
}