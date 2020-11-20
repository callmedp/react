import * as Actions from '../actions/actionTypes';

const initState = {
    pCourseList: []
}

export const PopularCoursesReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.POPULER_COURSES_FETCHED :
            return {...state, ...action.item}
        
        default:
            return state;
    }
}