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