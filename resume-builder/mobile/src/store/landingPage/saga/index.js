import {Api} from './Api';
import {takeLatest, call, put} from "redux-saga/effects";
import {siteDomain} from "../../../Utils/domains";
import * as Actions from '../actions/actionTypes';
import {LOGIN_CANDIDATE} from "../actions/actionTypes";
import {entityList} from "../../../Utils/formCategoryList";
import {SAVE_USER_INFO} from "../../personalInfo/actions/actionTypes";


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
        localStorage.clear();


        let result = yield call(Api.loginCandidate, payload);

        if (result['error']) {
            result = yield call(Api.getInformation)
        }
        if (result['error']) {
            console.log('error here and now returning');
            window.location.href = `${siteDomain}/login/?next=/resume-builder/`;
            return;
            //redirect code here
        }
        const {data: {candidate_id, candidate_profile, token, entity_status}} = result;
        localStorage.setItem('candidateId', (candidate_id) || '');
        for (const key in candidate_profile) {
            const entityObj = entity_status.find(el => el['display_value'] === key);
            if (key === 'personalInfo') {
                yield put({type: SAVE_USER_INFO, data: candidate_profile[key]})
            }
            if (!entityObj.set) {
                if (key == 'personalInfo') {

                    candidate_profile[key] = {
                        ...candidate_profile[key],
                        ...{
                            "entity_preference_data": entityList
                        }
                    };
                    localStorage.setItem(key, (JSON.stringify(candidate_profile[key])) || '')
                    localStorage.setItem('summary', '')
                } else localStorage.setItem(key, (JSON.stringify(candidate_profile[key])) || '');
            }
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