import * as Actions from '../actions/actionTypes';

const initState = {
    skillLoader : false,
    walletLoader: false,
    orderLoader: false,
    coursesLoader: false
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
        
        default: return state;
    }
}