import {
    mainCoursesFetched, ReviewsFetched, recommendedCoursesFetched, addToCartEnrollFetched, addToCartRedeemFetched
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
    prd_review_list : []
}

const appendReviews = (state, { payload }) => {
    if (payload.device === 'mobile' || payload.device === 'desktop') {
        if (!!payload.prd_reviews) {
            let reviews;
            let newReviews;

            newReviews = {
                prd_review_list : state.prd_review_list.concat(payload.prd_reviews.prd_review_list)
            }
            reviews = {
                ...payload.prd_reviews,
                ...newReviews
            }

            return { ...reviews };
        }
        else {
            return {}
        }
    }
    
    else {
        return {}
    }
}

export const ProductReviewsReducer = (state = reviewsState, action) => {
    switch (action.type) {
        // case ReviewsFetched.type: return { ...reviewsState, ...action.payload  }
        case ReviewsFetched.type: {
            return { ...reviewsState, ...appendReviews(state, action) }
        }
        default: return state;
    }
}

const addToCartState = {
}

export const AddToCartReducer = (state = addToCartState, action) => {
    switch (action.type) {
        case addToCartEnrollFetched.type: return { ...addToCartState, ...action.payload  }
        default: return state;
    }
}

const addToCartRedeemState = {
}

export const AddToCartRedeemReducer = (state = addToCartRedeemState, action) => {
    switch (action.type) {
        case addToCartRedeemFetched.type: return { ...addToCartRedeemState, ...action.payload  }
        default: return state;
    }
}
