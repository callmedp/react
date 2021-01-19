import {TRACK_USER} from './actionTypes';

export const trackUser = (payload) => {
    return {
        type: TRACK_USER,
        payload
    }
}
