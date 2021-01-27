import * as Actions from './actionTypes';

const fetchOiComment = (payload) => {
    return {
        type : Actions.FETCH_OI_COMMENT,
        payload
    }
}

export {
    fetchOiComment,
}