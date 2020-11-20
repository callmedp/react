import { FETCH_POPULER_COURSES  } from './actionTypes';

const fetchPopulerCourses = () => {
    return {
        type : FETCH_POPULER_COURSES,
    }
}

export {
    fetchPopulerCourses,
}