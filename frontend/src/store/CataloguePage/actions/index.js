import { 
    FETCH_COURSES_AND_ASSESSMENTS, 
    FETCH_RECENTLY_ADDED_COURSES,
    FETCH_POPULAR_SERVICES,
    FETCH_TRENDING_CATEGORIES,
    FETCH_ALL_CATEGORIES_AND_VENDORS
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

const fetchAllCategoriesAndVendors = (payload) => {

    return {
        type : FETCH_ALL_CATEGORIES_AND_VENDORS,
        payload
    }
}

export {
    fetchCoursesAndAssessments,
    fetchRecentlyAddedCourses,
    fetchPopularServices,
    fetchTrendingCategories,
    fetchAllCategoriesAndVendors
}