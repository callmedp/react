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