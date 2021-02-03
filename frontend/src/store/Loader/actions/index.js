import * as Actions from './actionTypes';

export const startSkillPageLoader = () => {
    return {
        type: Actions.START_SKILL_PAGE_LOADER,
        payload: { skillLoader: true } 
    }
}

export const stopSkillPageLoader = () => {
    return {
        type: Actions.STOP_SKILL_PAGE_LOADER,
        payload: { skillLoader: false }
    }
}

// Dashboard wallet loader
export const startDashboardWalletPageLoader = () => {
    return {
        type: Actions.START_DASHBOARD_WALLET_PAGE_LOADER,
        payload: { walletLoader: true } 
    }
}

export const stopDashboardWalletPageLoader = () => {
    return {
        type: Actions.STOP_DASHBOARD_WALLET_PAGE_LOADER,
        payload: { walletLoader: false }
    }
}

// Dashboard order loader
export const startDashboardOrderPageLoader = () => {
    return {
        type: Actions.START_DASHBOARD_ORDER_PAGE_LOADER,
        payload: { orderLoader: true } 
    }
}

export const stopDashboardOrderPageLoader = () => {
    return {
        type: Actions.STOP_DASHBOARD_ORDER_PAGE_LOADER,
        payload: { orderLoader: false }
    }
}

// Dashboard courses loader
export const startDashboardCoursesPageLoader = () => {
    return {
        type: Actions.START_DASHBOARD_COURSES_PAGE_LOADER,
        payload: { coursesLoader: true } 
    }
}

export const stopDashboardCoursesPageLoader = () => {
    return {
        type: Actions.STOP_DASHBOARD_COURSES_PAGE_LOADER,
        payload: { coursesLoader: false }
    }
}

// Dashboard services loader
export const startDashboardServicesPageLoader = () => {
    return {
        type: Actions.START_DASHBOARD_SERVICES_PAGE_LOADER,
        payload: { serviceLoader: true } 
    }
}

export const stopDashboardServicesPageLoader = () => {
    return {
        type: Actions.STOP_DASHBOARD_SERVICES_PAGE_LOADER,
        payload: { serviceLoader: false }
    }
}

export const startCommentLoader = () => {
    return {
        type: Actions.START_COMMENT_LOADER,
        payload: { commentLoader: true } 
    }
}

export const stopCommentLoader = () => {
    return {
        type: Actions.STOP_COMMENT_LOADER,
        payload: { commentLoader: false }
    }
}

export const startReviewLoader = () => {
    return {
        type: Actions.START_REVIEW_LOADER,
        payload: { reviewLoader: true } 
    }
}

export const stopReviewLoader = () => {
    return {
        type: Actions.STOP_REVIEW_LOADER,
        payload: { reviewLoader: false }
    }
}

export const startAcceptRejectLoader = () => {
    return {
        type: Actions.START_ACCEPT_REJECT_LOADER,
        payload: { acceptRejectLoader: true }
    }
}

export const stopAcceptRejectLoader = () => {
    return {
        type: Actions.STOP_ACCEPT_REJECT_LOADER,
        payload: { acceptRejectLoader: false }
    }
}

export const startUploadLoader = () => {
    return {
        type: Actions.START_UPLOAD_LOADER,
        payload: { uploadLoader: true }
    }
}

export const stopUploadLoader = () => {
    return {
        type: Actions.STOP_UPLOAD_LOADER,
        payload: { uploadLoader: false }
    }
}