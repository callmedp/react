import * as Actions from '../actions/actionTypes';

const recentCoursesState = {
    recentCoursesList : []
}

export const RecentlyAddedCoursesReducer = (state=recentCoursesState, action) => {
    switch(action.type){
        case Actions.RECENTLY_ADDED_COURSES_FETCHED : return {...recentCoursesState, ...action.item}
        default : return state;
    }
}

const popularState = {
    popularServices : []
}

export const PopularServicesReducer = (state=popularState, action) => {
    switch(action.type){
        case Actions.POPULAR_SERVICES_FETCHED : return {...popularState, ...action.item}
        default : return state;
    }
}

const trendingCategoriesState = {
    SnMCourseList : [],
    ITCourseList : [],
    BnFCourseList : []
}

export const TrendingCategoriesReducer = (state=trendingCategoriesState, action) => {
    switch(action.type){
        case Actions.TRENDING_CATEGORIES_FETCHED : return {...trendingCategoriesState, ...action.item}
        default : return state;
    }
}

const allCategoriesState = {
    categoryList : [],
    vendorList : []
}

export const AllCategoriesReducer = (state=allCategoriesState, action) => {
    switch(action.type){
        case Actions.ALL_CATEGORIES_AND_VENDORS_FETCHED : return {...allCategoriesState, ...action.item}
        default : return state;
    }
}