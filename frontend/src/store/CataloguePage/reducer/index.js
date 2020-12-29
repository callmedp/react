import * as Actions from '../actions/actionTypes';

const initState = {
   SnMCourseList : [],
   ITCourseList : [],
   BnFCourseList : []
}

export const CourseAndAssessmentsReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.COURSES_AND_ASSESSMENTS_FETCHED : return {...state, ...action.item}
        default: return state;
    }
}


const recentCoursesState = {

}

export const RecentlyAddedCoursesReducer = (state=recentCoursesState, action) => {
    switch(action.type){
        case Actions.RECENTLY_ADDED_COURSES_FETCHED : return {...recentCoursesState, ...action.item}
        default : return state;
    }
}