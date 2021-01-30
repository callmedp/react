import { 
    FETCH_LATEST_BLOG,
    FETCH_MOST_VIEWED_PRODUCTS,
    FETCH_IN_DEMAND_PRODUCTS,
    FETCH_JOB_ASSISTANCE_SERVICES
} from './actionTypes';

const fetchLatestBlog = (payload) => {
   
    return {
        type : FETCH_LATEST_BLOG,
        payload
    }
}

const fetchMostViewedCourses = (payload) => {
   
    return {
        type : FETCH_MOST_VIEWED_PRODUCTS,
        payload
    }
}

const fetchInDemandProducts = (payload) => {
   
    return {
        type : FETCH_IN_DEMAND_PRODUCTS,
        payload
    }
}

const fetchJobAssistanceServices = (payload) => {
   
    return {
        type : FETCH_JOB_ASSISTANCE_SERVICES,
        payload
    }
}


export {
    fetchLatestBlog,
    fetchMostViewedCourses,
    fetchInDemandProducts,
    fetchJobAssistanceServices,
}