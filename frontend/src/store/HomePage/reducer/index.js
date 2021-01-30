import * as Actions from '../actions/actionTypes';

const latestBlogState = {
    recentCoursesList : []
}



export const LatestBlogReducer = (state=latestBlogState, action) => {
    switch(action.type){
        case Actions.LATEST_BLOG_FETCHED : return {...latestBlogState, ...action.item}
        default : return state;
    }
}

const mostViewedCoursesState = {
    recentCoursesList : []
}

export const MostViewedCoursesReducer = (state=mostViewedCoursesState, action) => {
    switch(action.type){
        case Actions.MOST_VIEWED_PRODUCTS_FETCHED  : return {...mostViewedCoursesState, ...action.item}
        default : return state;
    }
}

const inDemandProductsState = {
    recentCoursesList : []
}

export const InDemandProductsReducer = (state=inDemandProductsState, action) => {
    switch(action.type){
        case Actions.IN_DEMAND_PRODUCTS_FETCHED : return {...inDemandProductsState, ...action.item}
        default : return state;
    }
}

const jobAssistanceServicesState = {
    recentCoursesList : []
}

export const JobAssistanceServicesReducer = (state=jobAssistanceServicesState, action) => {
    switch(action.type){
        case Actions.JOB_ASSISTANCE_SERVICES_FETCHED : return {...jobAssistanceServicesState, ...action.item}
        default : return state;
    }
}
