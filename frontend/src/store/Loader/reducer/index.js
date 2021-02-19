import * as Actions from '../actions/actionTypes';

const initState = {
    skillLoader : false,
    walletLoader: false,
    orderLoader: false,
    coursesLoader: false,
    serviceLoader: false,
    commentLoader: false,
    reviewLoader: false,
    acceptRejectLoader: false,
    homeLoader: false,
    uploadLoader: false,
    oiDetailsLoader: false
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

        // accept reject loader
        case Actions.START_ACCEPT_REJECT_LOADER : return {...state, ...action.payload}
        case Actions.STOP_ACCEPT_REJECT_LOADER : return {...state, ...action.payload}

        // homepage loader
        case Actions.START_HOME_PAGE_LOADER : return { ...state, ...action.payload }
        case Actions.STOP_HOME_PAGE_LOADER : return { ...state, ...action.payload }
        // upload loader
        case Actions.START_UPLOAD_LOADER : return {...state, ...action.payload}
        case Actions.STOP_UPLOAD_LOADER : return {...state, ...action.payload}

        // oi details loader
        case Actions.START_OI_DETAILS_LOADER : return {...state, ...action.payload}
        case Actions.STOP_OI_DETAILS_LOADER : return {...state, ...action.payload}

        default: return state;
    }
}