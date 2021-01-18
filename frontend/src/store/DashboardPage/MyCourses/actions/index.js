import { FETCH_MY_COURSES  } from './actionTypes';

const fetchMyCourses = (payload) => {
    return {
        type : FETCH_MY_COURSES,
        payload
    }
}

export {
    fetchMyCourses,
}