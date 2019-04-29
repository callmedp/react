import {Api} from './Api';
import {takeLatest, call} from "redux-saga/effects";
import {siteDomain} from "../../../Utils/domains";
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
        // handle token already present in there
        if (localStorage.getItem('token')) {
            return;
        }
        const result = yield call(Api.loginCandidate, payload);
        console.log('---login state-', result);
        if (result['error']) {
            console.log('error here and now returning');
            window.location.href = `${siteDomain}/login/?next=/resume-builder/`;
            return;
            //redirect code here
        }
        const {data: {candidate_id, candidate_profile, token}} = result;
        localStorage.setItem('candidateId', (candidate_id) || '');
        for (const key in candidate_profile) {
            localStorage.setItem(key, (candidate_profile[key]) || '');
        }
        localStorage.setItem('token', (token) || '');
    } catch (e) {
        console.log(e);
    }
}


export default function* watchLandingPage() {
    yield takeLatest(Actions.GET_CANDIDATE_ID, getCandidateId);
    yield takeLatest(Actions.LOGIN_CANDIDATE, loginCandidate);

}