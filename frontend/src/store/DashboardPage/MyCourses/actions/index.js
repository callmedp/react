import { FETCH_MY_COURSES, BOARD_NEO_USER  } from './actionTypes';

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

export {
    fetchMyCourses,
    boardNeoUser
}