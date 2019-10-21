import {apiError} from '../../../Utils/apiError';
import {takeLatest, call, put} from "redux-saga/effects";
import {siteDomain} from "../../../Utils/domains";
import * as Actions from '../actions/actionTypes';
import {entityList} from "../../../Utils/formCategoryList";
import {SAVE_USER_INFO} from "../../personalInfo/actions/actionTypes";
import * as uiAction from '../../ui/actions/actionTypes';
import {LandingPageToast} from '../../../services/toastService'
import {Api} from './Api.js';

function* getCandidateId() {
    try {
        const result = yield call(Api.getCandidateId);
        if (result['error']) {
            apiError();

        }

        localStorage.setItem('candidateId', JSON.parse((result.data && result.data['candidate_id'])) || '');

    } catch (e) {
        apiError();
    }
}

function* loginCandidate(action) {
    try {
        let {data: {payload, resolve, reject, isTokenAvail}} = action;

        yield put({type: uiAction.UPDATE_MAIN_PAGE_LOADER, payload: {mainloader: true}})

        let result;
        if (isTokenAvail) {
            result = yield call(Api.loginCandidate, payload);
        }
        if (result && result['error'] || !isTokenAvail) {
            result = yield call(Api.getInformation)
        }


        if (result && result['error']) {
            apiError('login')
            localStorage.clear();
            window.location.href = `${siteDomain}/login/${window.location.search ? window.location.search+'&' : '?'}next=/resume-builder/`;
            return;
            //redirect code here
        }
        const {data: {candidate_id, candidate_profile, token, entity_status, experience}} = result;
        localStorage.setItem('candidateId', (candidate_id) || '');
        localStorage.setItem('experience',(experience || 0));
        for (const key in candidate_profile) {
            const entityObj = entity_status.find(el => el['display_value'] === key);
            if (key === 'personalInfo') {
                candidate_profile[key] = {
                    ...candidate_profile[key],
                    ...{
                        "location": ''
                    }
                }
                localStorage.setItem('email', candidate_profile[key]['email'] || '');
                const fName = (candidate_profile[key]['first_name'] ||'').trim()
                const lName = (candidate_profile[key]['last_name'] ||'').trim()
                let name = fName ? (lName ? fName + " " + lName : fName):lName ? lName :'Dummy User'   
                localStorage.setItem('name', name || '');
                localStorage.setItem('mobile',candidate_profile[key]['number'])

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
                    localStorage.setItem(key, (JSON.stringify(candidate_profile[key])) || '');
                    localStorage.setItem('summary', '')
                } else localStorage.setItem(key, (JSON.stringify(candidate_profile[key])) || '');
            }
        }
        localStorage.setItem('token', (token) || '');
        resolve('Login Successfully');

        yield put({type: uiAction.UPDATE_MAIN_PAGE_LOADER, payload: {mainloader: false}})
    } catch
        (e) {
        apiError();
    }
}


function* feedbackSubmit(action) {
    try {
        let {payload} = action;
        let result = yield call(Api.feedbackSubmit, payload);
        if (result["error"]) {
            console.log("error");
        } else {
            LandingPageToast.fire({
                type: "success",
                title: "<font size='3'>Feedback Submitted Successfully</font>"
            });
        }
    } catch (e) {
        console.log(e);
    }
}


export default function* watchLandingPage() {
    yield takeLatest(Actions.GET_CANDIDATE_ID, getCandidateId);
    yield takeLatest(Actions.LOGIN_CANDIDATE, loginCandidate);
    yield takeLatest(Actions.FEEDBACK_SUBMIT, feedbackSubmit);

}