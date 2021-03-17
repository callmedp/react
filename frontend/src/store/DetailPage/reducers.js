import {
    OtherProviderCoursesFetched, mainCoursesFetched, CourseReviewFetched
} from './actions';


const mainCoursesState = {
    // mainCoursesData: {}
}

export const mainCoursesReducer = (state = mainCoursesState, action) => {
    switch (action.type) {
        case mainCoursesFetched.type: return { ...mainCoursesState, ...action.payload  }
        default: return state;
    }
}

const otherProvidersCoursesState = {
    mostViewedCourses: {}
}

export const OtherProvidersCoursesReducer = (state = otherProvidersCoursesState, action) => {
    switch (action.type) {
        case OtherProviderCoursesFetched.type: return { ...otherProvidersCoursesState, ...action.payload  }
        default: return state;
    }
}

const courseReviewState = {
    // mostViewedCourses: {}
}

export const CourseReviewReducer = (state = courseReviewState, action) => {
    switch (action.type) {
        case CourseReviewFetched.type: return { ...courseReviewState, ...action.payload  }
        default: return state;
    }
}