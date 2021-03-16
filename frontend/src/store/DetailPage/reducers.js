import {
    OtherProviderCoursesFetched, mainCoursesFetched
} from './actions';


const mainCoursesState = {
    mainCoursesFetched: {}
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