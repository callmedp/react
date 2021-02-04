import * as Actions from './actionTypes';

const fetchMyServices = (payload) => {
    return {
        type : Actions.FETCH_MY_SERVICES,
        payload
    }
}

const fetchPendingResume = payload => {
    return {
        type: Actions.GET_PENDING_RESUME,
        payload: payload,
    }
}

const uploadResumeForm = (payload) => ({
    type: Actions.UPLOAD_RESUME_FORM,
    payload
})

const CandidateAcceptRejectResume = (payload) => {
    return {
        type: Actions.REQUEST_CANDIDATE_OI_ACCEPT_REJECT,
        payload
    }
}

const pausePlayResume = (payload) => {
    return {
        type: Actions.PAUSE_AND_RESUME_SERVICE_REQUEST,
        payload
    }
}

const fetchOiDetails = (payload) => {
    return {
        type: Actions.FETCH_OI_DETAILS,
        payload
    }
}

export {
    fetchMyServices,
    uploadResumeForm,
    fetchPendingResume,
    CandidateAcceptRejectResume,
    pausePlayResume,
    fetchOiDetails
}