import * as Actions from '../actions/actionTypes';

export const FetchUserInfoReducer = (state={}, action) => {
    switch(action.type){
        case Actions.FETCH_USER : return {...state, ...action.item}
        default: return state;
    }
}

const chatbotScriptState = {
    script_link : []
}

export const ChatbotScriptReducer = (state=chatbotScriptState, action) => {
    switch(action.type){
        case Actions.CHATBOT_SCRIPT_FETCHED : return {...chatbotScriptState, ...action.item}
        default : return state;
    }
}