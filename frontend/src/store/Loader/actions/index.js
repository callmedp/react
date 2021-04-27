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

export const startHomePageLoader = () => {
    return {
        type: Actions.START_HOME_PAGE_LOADER,
        payload: { homeLoader: true } 
    }
}

export const stopHomePageLoader = () => {
    return {
        type: Actions.STOP_HOME_PAGE_LOADER,
        payload: { homeLoader: false }
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

export const startOiDetailsLoader = () => {
    return {
        type: Actions.START_OI_DETAILS_LOADER,
        payload: { oiDetailsLoader: true }
    }
}

export const stopOiDetailsLoader = () => {
    return {
        type: Actions.STOP_OI_DETAILS_LOADER,
        payload: { oiDetailsLoader: false }
    }
}

// main course loader
export const startMainCourseLoader = () => {
    return {
        type: Actions.START_MAIN_COURSE_LOADER,
        payload: { mainCourseLoader: true }
    }
}

export const stopMainCourseLoader = () => {
    return {
        type: Actions.STOP_MAIN_COURSE_LOADER,
        payload: { mainCourseLoader: false }
    }
}

// main course cart loader
export const startMainCourseCartLoader = () => {
    return {
        type: Actions.START_MAIN_COURSE_CART_LOADER,
        payload: { mainCourseCartLoader: true }
    }
}

export const stopMainCourseCartLoader = () => {
    return {
        type: Actions.STOP_MAIN_COURSE_CART_LOADER,
        payload: { mainCourseCartLoader: false }
    }
}

// need help loader
export const startNeedHelpLoader = () => {
    return {
        type: Actions.START_NEED_HELP_LOADER,
        payload: { needHelpLoader: true }
    }
}

export const stopNeedHelpLoader = () => {
    return {
        type: Actions.STOP_NEED_HELP_LOADER,
        payload: { needHelpLoader: false }
    }
}

export const startGetResumeScoreLoader = () => {
    return {
        type: Actions.START_GET_RESUME_SCORE_LOADER,
        payload: { resumeScoreLoader: true }
    }
}

export const stopGetResumeScoreLoader = () => {
    return {
        type: Actions.STOP_GET_RESUME_SCORE_LOADER,
        payload: { resumeScoreLoader: false }
    }
}

export const startJobsUpskillsLoader = () => {
    return {
        type: Actions.START_OI_DETAILS_LOADER,
        payload: { jobsUpskillsLoader: true }
    }
}

export const stopJobsUpskillsLoader = () => {
    return {
        type: Actions.STOP_OI_DETAILS_LOADER,
        payload: { jobsUpskillsLoader: false }
    }
}

export const startCareerChangeLoader = () => {
    return {
        type: Actions.START_CAREER_CHANGE_LOADER,
        payload: { careerChangeLoader: true }
    }
}

export const stopCareerChangeLoader = () => {
    return {
        type: Actions.STOP_CAREER_CHANGE_LOADER,
        payload: { careerChangeLoader: false }
    }
}