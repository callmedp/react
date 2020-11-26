import { FETCH_POPULER_COURSES  } from './actionTypes';

const fetchPopulerCourses = (payload) => {
    return {
        type : FETCH_POPULER_COURSES,
        payload
    }
}

export {
    fetchPopulerCourses,
}