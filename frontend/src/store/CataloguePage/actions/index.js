import { FETCH_COURSES_AND_ASSESSMENTS, FETCH_RECENTLY_ADDED_COURSES  } from './actionTypes';

const fetchCoursesAndAssessments = (payload) => {
    return {
        type : FETCH_COURSES_AND_ASSESSMENTS,
        payload
    }
}

const fetchRecentlyAddedCourses = (payload) => {
   
    return {
        type : FETCH_RECENTLY_ADDED_COURSES,
        payload
    }
}

export {
    fetchCoursesAndAssessments,
    fetchRecentlyAddedCourses,
}