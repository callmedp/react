import { FETCH_DOMAIN_JOBS  } from './actionTypes';

const fetchCoursesAndAssessments = (payload) => {
    return {
        type : FETCH_COURSES_AND_ASSESSMENTS,
        payload
    }
}

export {
    fetchCourses,
}