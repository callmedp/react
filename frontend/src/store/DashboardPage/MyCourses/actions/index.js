import { FETCH_MY_COURSES, BOARD_NEO_USER, UPDATE_COURSE_COMMENT_COUNT  } from './actionTypes';

const fetchMyCourses = (payload) => {
    return {
        type : FETCH_MY_COURSES,
        payload
    }
}

const boardNeoUser = (payload) =>{
    return{
        type: BOARD_NEO_USER,
        payload
    }
}

const updateCourseCommentCount = payload => {
    return {
        type: UPDATE_COURSE_COMMENT_COUNT,
        payload
    }
}

export {
    fetchMyCourses,
    boardNeoUser,
    updateCourseCommentCount,
}