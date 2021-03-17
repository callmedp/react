import {
    OtherProviderCoursesFetched, mainCoursesFetched, ReviewsFetched, recommendedCoursesFetched
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
    pop_list: {}
}

export const OtherProvidersCoursesReducer = (state = otherProvidersCoursesState, action) => {
    switch (action.type) {
        case OtherProviderCoursesFetched.type: return { ...otherProvidersCoursesState, ...action.payload  }
        default: return state;
    }
}

const recommendedCoursesState = {
    pop_list: {}
}

export const RecommendedCoursesReducer = (state = recommendedCoursesState, action) => {
    switch (action.type) {
        case recommendedCoursesFetched.type: return { ...recommendedCoursesState, ...action.payload  }
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