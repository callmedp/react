import {
    OtherProviderCoursesFetched,
} from './actions';

const otherProvidersCoursesState = {
    pop_list: {}
}

export const OtherProvidersCoursesReducer = (state = otherProvidersCoursesState, action) => {
    switch (action.type) {
        case OtherProviderCoursesFetched.type: return { ...otherProvidersCoursesState, ...action.payload  }
        default: return state;
    }
}