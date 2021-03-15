import {
    OtherProviderCoursesFetched,
} from './actions';

const otherProvidersCoursesState = {
    mostViewedCourses: {}
}

export const OtherProvidersCoursesReducer = (state = otherProvidersCoursesState, action) => {
    switch (action.type) {
        case OtherProviderCoursesFetched.type: return { ...otherProvidersCoursesState, ...action.payload  }
        default: return state;
    }
}