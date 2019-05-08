import {Api} from './Api';
import {takeLatest, call,put} from "redux-saga/effects";
import {siteDomain} from "../../../Utils/domains";
import * as Actions from '../actions/actionTypes';
import {LOGIN_CANDIDATE} from "../actions/actionTypes";
import {entityList} from "../../../Utils/formCategoryList";


function* getCandidateId() {
    try {
        const result = yield call(Api.getCandidateId);
        if (result['error']) {
            console.log('error');

        }

        localStorage.setItem('candidateId', JSON.parse((result.data && result.data['candidate_id'])) || '');

    } catch (e) {
        console.log(e);
    }
}

function* loginCandidate(action) {
    try {
        let {payload} = action;

        //handle token already present in there
        if (localStorage.getItem('token')) {
            yield put({type: 'FETCH_PERSONAL_INFO'});

            console.log('--token available-');
            return;
        }
        const result = yield call(Api.loginCandidate, payload);
        if (result['error']) {
            console.log('error here and now returning');
            window.location.href = `${siteDomain}/login/?next=/resume-builder/`;
            return;
            //redirect code here
        }
        const {data: {candidate_id, candidate_profile, token}} = result;
        localStorage.setItem('candidateId', (candidate_id) || '');
        for (const key in candidate_profile) {
            if (key == 'personalInfo') {
                candidate_profile[key] = {
                    ...candidate_profile[key],
                    ...{
                        "entity_preference_data": entityList
                    }
                }
                localStorage.setItem(key, (JSON.stringify(candidate_profile[key])) || '')

            } else localStorage.setItem(key, (JSON.stringify(candidate_profile[key])) || '');
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