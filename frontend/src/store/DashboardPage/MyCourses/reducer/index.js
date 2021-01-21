import * as Actions from '../actions/actionTypes';

const initState = {
    myCourses : []
}

export const DashboardMyCoursesReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.MY_COURSES_FETCHED : return { ...initState,...action.item}
        default: return state;
    }
}