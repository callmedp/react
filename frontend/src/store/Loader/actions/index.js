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