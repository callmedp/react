import { apiError } from '../../../Utils/apiError';
import { takeLatest, call, put } from "redux-saga/effects";
import { siteDomain } from "../../../Utils/domains";
import * as Actions from '../actions/actionTypes';
import { entityList } from "../../../Utils/formCategoryList";
import { SAVE_USER_INFO } from "../../personalInfo/actions/actionTypes";
import * as uiAction from '../../ui/actions/actionTypes';
import { LandingPageToast } from '../../../services/toastService'
import { Api } from './Api.js';

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


function* getCandidateShineDetails(action) {
    try {
        const { payload: { resolve, reject } } = action;

        yield put({ type: uiAction.UPDATE_MAIN_PAGE_LOADER, payload: { mainloader: true } });

        const result = yield call(Api.getInformation);

        if (result && result['error']) {
            localStorage.clear();
            yield put({ type: uiAction.UPDATE_MAIN_PAGE_LOADER, payload: { mainloader: false } })
            return reject(new Error(result['errorMessage']));
            //redirect code here
        }

        //////////

        const { data: { candidate_id, candidate_profile, token, entity_status, userExperience } } = result;
        localStorage.setItem('candidateId', (candidate_id) || '');
        localStorage.setItem('userExperience', (userExperience || 0));
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
                localStorage.setItem('mobile', candidate_profile[key]['number'])

                yield put({ type: SAVE_USER_INFO, data: candidate_profile[key] })
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

        yield put({ type: uiAction.UPDATE_MAIN_PAGE_LOADER, payload: { mainloader: false } })

        resolve('Login Successfully');


    } catch (e) {
        console.log(e);
    }
}

function* loginCandidate(action) {
    try {
        let { data: { info, resolve, reject, isTokenAvail } } = action;

        yield put({ type: uiAction.UPDATE_MAIN_PAGE_LOADER, payload: { mainloader: true } })

        let result;
        if (isTokenAvail) {
            result = yield call(Api.loginCandidate, info);
        }

        // if some error comes or token not available then
        // get new information using session.

        let checkSession = yield call(Api.checkSessionAvaialability)

        const { data: isSessionAvailable } = checkSession;

        if ((result && result['error'] || !isTokenAvail) && Object.keys(info).indexOf('alt') !== -1 && isSessionAvailable['result']) {
            result = yield call(Api.getInformation)
        }

        if (result && result['error']) {
            yield put({ type: uiAction.UPDATE_MAIN_PAGE_LOADER, payload: { mainloader: false } })
            localStorage.clear();
            return reject(new Error(result['errorMessage']));
            //redirect code here
        }
        const { data: { candidate_id, candidate_profile, token, entity_status, userExperience } } = result;
        localStorage.setItem('candidateId', (candidate_id) || '');
        localStorage.setItem('userExperience', (userExperience || 0));
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
                localStorage.setItem('mobile', candidate_profile[key]['number'])
                yield put({ type: SAVE_USER_INFO, data: candidate_profile[key] })
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
        yield put({ type: uiAction.UPDATE_MAIN_PAGE_LOADER, payload: { mainloader: false } })
        resolve('Login Successfully');
    } catch
    (e) {
        if (typeof document !== 'undefined') apiError();
        else console.log(e);
    }
}


function* feedbackSubmit(action) {
    try {
        let { payload } = action;
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

function* getComponentTitle(action) {
    try {
        let { payload: { resolve, reject } } = action;
        resolve('Resume Builder 2019 | Online Free Resume Maker [Unique Templates] @ Shine Learning')
    } catch (e) {
        console.log(e);
    }
}



function* checkSessionAvaialability(action) {
    try {
        let { payload: { resolve, reject } } = action;
        let result = yield call(Api.checkSessionAvaialability)
        if (result["error"]) {
            resolve(false)
        }
        const { data } = result;
        resolve(data['result']);
    } catch (e) {
        console.log(e);
    }
}


export default function* watchLandingPage() {
    yield takeLatest(Actions.GET_CANDIDATE_ID, getCandidateId);
    yield takeLatest(Actions.LOGIN_CANDIDATE, loginCandidate);
    yield takeLatest(Actions.FEEDBACK_SUBMIT, feedbackSubmit);
    yield takeLatest(Actions.GET_HOME_COMPONENT_TITLE, getComponentTitle);
    yield takeLatest(Actions.GET_CANDIDATE_SHINE_DETAILS, getCandidateShineDetails);
    yield takeLatest(Actions.CHECK_SESSION_AVAILABILITY, checkSessionAvaialability);

}