import {
    OtherProviderCoursesFetched,
    ReviewsFetched
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

const reviewsState = {
    prd_reviews: {}
}

export const ProductReviewsReducer = (state = reviewsState, action) => {
    switch (action.type) {
        case ReviewsFetched.type: return { ...reviewsState, ...action.payload  }
        default: return state;
    }
}