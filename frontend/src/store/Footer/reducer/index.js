import * as Actions from '../actions/actionTypes';

const initState = {
    trendingCourses : [],
    trendingSkills : []
}

export const FooterReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.TRENDING_COURSES_AND_SKILLS_FETCHED : return {...state, ...action.item}
        default: return state;
    }
}

const popularCoursesState = {
    trendingCourses : [],
    trendingSkills : []
}

export const PopularCoursesReducer = (state=popularCoursesState, action) => {
    switch(action.type){
        case Actions.POPULAR_COURSES_FETCHED : return {...state, ...action.item}
        default: return state;
    }
}