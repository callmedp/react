import {Api} from './Api';
import {takeLatest, call} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';
import {LOGIN_CANDIDATE} from "../actions/actionTypes";


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

function* loginCandidate(action) {
    try {
        let {payload} = action;
        const result = yield call(Api.loginCandidate, payload);
        console.log('---login state-', result);
        if (result['error']) {
            //redirect code here
        }
        const {data: {candidate_id, candidate_profile, token}} = result;


    } catch (e) {
        console.log(e);
    }
}


export default function* watchLandingPage() {
    yield takeLatest(Actions.GET_CANDIDATE_ID, getCandidateId);
    yield takeLatest(Actions.LOGIN_CANDIDATE, loginCandidate);

}