import {
    UPLOAD_FILE,
    UPDATE_SCORE
} from './actionTypes';


export const uploadFile = (payload) => ({
    type: UPLOAD_FILE,
    payload
});

export const updateScore = (payload) => ({
    type: UPDATE_SCORE,
    payload
})