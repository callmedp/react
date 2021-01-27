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

const fetchPendingResumes = (payload) => {
    return {
        type: Actions.FETCH_PENDING_RESUMES,
        payload
    }
}

export {
    fetchMyServices,
    uploadResumeForm,
    fetchPendingResumes
}