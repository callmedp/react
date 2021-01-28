import * as Actions from './actionTypes';

const fetchMyServices = (payload) => {
    return {
        type : Actions.FETCH_MY_SERVICES,
        payload
    }
}

export const fetchPendingResume = payload => {
    return {
        type: Actions.GET_PENDING_RESUME,
        payload: payload,
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

export const CandidateAcceptRejectResume = (payload) => {
    return {
        type: Actions.REQUEST_CANDIDATE_OI_ACCEPT_REJECT,
        payload
    }
}

export {
    fetchMyServices,
    uploadResumeForm,
    fetchPendingResumes
}