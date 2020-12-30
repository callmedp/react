import { 
    FETCH_COURSES_AND_ASSESSMENTS, 
    FETCH_RECENTLY_ADDED_COURSES,
    FETCH_POPULAR_SERVICES,
    FETCH_TRENDING_CATEGORIES
} from './actionTypes';

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

const fetchPopularServices = (payload) => {
   
    return {
        type : FETCH_POPULAR_SERVICES,
        payload
    }
}

const fetchTrendingCategories = (payload) => {

    return {
        type : FETCH_TRENDING_CATEGORIES,
        payload
    }
}

export {
    fetchCoursesAndAssessments,
    fetchRecentlyAddedCourses,
    fetchPopularServices,
    fetchTrendingCategories
}