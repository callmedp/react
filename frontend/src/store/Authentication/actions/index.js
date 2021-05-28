import { FETCH_USER } from './actionTypes'

export const fetchAlreadyLoggedInUser = (payload) => {
    return {
        type: FETCH_USER,
        payload
    }
}