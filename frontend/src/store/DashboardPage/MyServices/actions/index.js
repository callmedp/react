import * as Actions from './actionTypes';

const fetchMyServices = (payload) => {
    return {
        type : Actions.FETCH_MY_SERVICES,
        payload
    }
}

const uploadResumeForm = (payload) => ({
    type: Actions.UPLOAD_RESUME_FORM,
    payload
})

// oi comment
const getoiComment = (payload) => {
    return {
        type: Actions.GET_OI_COMMENT,
        payload
    }
}

// fetch reviews
const fetchMyReviews = (payload) => {
    return {
        type : Actions.FETCH_MY_REVIEWS,
        payload
    }
}

const fetchPendingResumes = (payload) => {
    return {
        type: Actions.FETCH_PENDING_RESUMES,
        payload
    }
}

export {
    fetchMyServices,
    uploadResumeForm,
    getoiComment,
    fetchMyReviews,
    fetchPendingResumes
}