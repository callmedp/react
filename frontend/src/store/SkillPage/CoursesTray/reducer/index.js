import * as Actions from '../actions/actionTypes';

const initState = {
    courseList : [],
    assessmentList : []
}

export const CourseAndAssessmentsReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.COURSES_AND_ASSESSMENTS_FETCHED : return {...state, ...action.item}
        default: return state;
    }
}