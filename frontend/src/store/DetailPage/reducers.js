import {
    OtherProviderCoursesFetched, mainCoursesFetched, ReviewsFetched, recommendedCoursesFetched, addToCartEnrollFetched, recommendCourseFetched
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
    results: []
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

const addToCartState = {
    // prd_reviews: {}
}

export const AddToCartReducer = (state = addToCartState, action) => {
    switch (action.type) {
        case addToCartEnrollFetched.type: return { ...addToCartState, ...action.payload  }
        default: return state;
    }
}
