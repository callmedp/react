import {Api} from './Api';
import {takeLatest,  call} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';


function* getCandidateId() {
    try {
        const result = yield call(Api.getCandidateId);
        if (result['error']) {
            console.log('error');

        }
        localStorage.setItem('candidateId', (result.data && result.data['candidate_id']) || '');

    } catch (e) {
        console.log(e);
    }
}


export default function* watchLandingPage() {
    yield takeLatest(Actions.GET_CANDIDATE_ID, getCandidateId)
}