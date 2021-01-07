import * as Actions from './actionTypes';


export const fetchTrendingCnA = (payload) =>{
    return {
        type: Actions.FETCH_TRENDING_COURSES_AND_SKILLS,
        payload
    }
}

export const fetchPopularCourses = (payload) =>{
    return {
        type: Actions.FETCH_POPULAR_COURSES,
        payload
    }
}

