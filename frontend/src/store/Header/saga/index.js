import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

function* sessionAvailability(action) {
    let { payload: { resolve } } = action;
    try {
        let resp = yield call(Api.sessionAvailability)
        const { result, candidate_id } = resp.data;
        localStorage.setItem('isAuthenticated', result);
        localStorage.setItem('candidateId', candidate_id);
        resolve({ result: result, candidate_id: candidate_id });
    } catch (e) {
        return resolve(false)
    }
}

function* cartCount(action) {
    try {
        const response = yield call(Api.cartCount);
        if (response["error"]) {
            return
        }
        const item = response?.data;
        yield put({ 
            type: Actions.CART_COUNT_FETCHED,
            item 
        });

    }
    catch (e) {
        console.error("Exception occured at cartCount Api", e);
    }
}


function* candidateInfo(action) {
    const { payload: { candidateId, resolve, reject } } = action;
    try {
        const result = yield call(Api.candidateInformation, candidateId);
        const { candidate_id, profile : { first_name, email, cell_phone } } = result?.data;
        localStorage.setItem('userId', candidate_id);
        localStorage.setItem('userName', first_name);
        localStorage.setItem('userEmail', email);
        resolve({ candidateId: candidate_id || '', name: first_name || '', email: email || '' , mobile: cell_phone || ''});
    }
    catch (e) {
        console.error("Exception occured at candidateInfo Api", e);
        return reject(e);
    }
}

function* navOffersAndTags(action) {
    try {
        const { payload } = action;
        const response = yield call(Api.navOffersAndTags, payload);
        if (response["error"]) {
            return
        }
        const item = response?.data?.data;

        yield put({ 
            type : Actions.NAVIGATION_OFFERS_AND_SPECIAL_TAGS_FETCHED, 
            item 
        })

    } catch (e) {
        console.error("Exception occured at navOffersAndTags ",e)
    }
}

export default function* WatchHeader(){
    yield takeLatest(Actions.FETCH_SESSION_AVAILABILITY, sessionAvailability);
    yield takeLatest(Actions.FETCH_CART_COUNT, cartCount);
    yield takeLatest(Actions.FETCH_CANDIDATE_INFO, candidateInfo);
    yield takeLatest(Actions.FETCH_NAVIGATION_OFFERS_AND_SPECIAL_TAGS, navOffersAndTags);
}