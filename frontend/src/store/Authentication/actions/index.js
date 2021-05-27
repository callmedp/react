import { FETCH_USER, FETCH_CHATBOT_SCRIPT } from './actionTypes'

export const fetchAlreadyLoggedInUser = (payload) => {
    return {
        type: FETCH_USER,
        payload
    }
}

export const fetchChatbotScript = (payload) => {
   
    return {
        type : FETCH_CHATBOT_SCRIPT,
        payload
    }
}