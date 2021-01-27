import * as Actions from '../actions/actionTypes';

const initState = {
    skillLoader : false,
    walletLoader: false,
    orderLoader: false,
    coursesLoader: false,
    serviceLoader: false,
    commentLoader: false,
    reviewLoader: false
}

export const LoaderReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.START_SKILL_PAGE_LOADER : return {...state, ...action.payload}
        case Actions.STOP_SKILL_PAGE_LOADER : return {...state, ...action.payload}

        // dashboard waller loader
        case Actions.START_DASHBOARD_WALLET_PAGE_LOADER : return {...state, ...action.payload}
        case Actions.STOP_DASHBOARD_WALLET_PAGE_LOADER : return {...state, ...action.payload}

        // dashboard order loader
        case Actions.START_DASHBOARD_ORDER_PAGE_LOADER : return {...state, ...action.payload}
        case Actions.STOP_DASHBOARD_ORDER_PAGE_LOADER : return {...state, ...action.payload}
        
        // dashboard courses loader
        case Actions.START_DASHBOARD_COURSES_PAGE_LOADER : return {...state, ...action.payload}
        case Actions.STOP_DASHBOARD_COURSES_PAGE_LOADER : return {...state, ...action.payload}

        // dashboard service loader
        case Actions.START_DASHBOARD_SERVICES_PAGE_LOADER : return {...state, ...action.payload}
        case Actions.STOP_DASHBOARD_SERVICES_PAGE_LOADER : return {...state, ...action.payload}

        // comment loader
        case Actions.START_COMMENT_LOADER : return {...state, ...action.payload}
        case Actions.STOP_COMMENT_LOADER : return {...state, ...action.payload}

        // review loader
        case Actions.START_REVIEW_LOADER : return {...state, ...action.payload}
        case Actions.STOP_REVIEW_LOADER : return {...state, ...action.payload}

        default: return state;
    }
}