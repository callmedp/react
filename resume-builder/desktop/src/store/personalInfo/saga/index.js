import { Api } from './Api';

import { takeLatest, takeEvery, put, call } from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import moment from 'moment'

import { SubmissionError } from 'redux-form'
import { Toast } from "../../../services/ErrorToast";
import { UPDATE_UI } from "../../ui/actions/actionTypes";

const genderDict = {
    '0': {
        value: '0',
        'label': 'None'
    },
    '1': {
        value: '1',
        'label': 'Male'
    },
    '2': {
        value: '2',
        'label': 'Female'
    },
    '3': {
        value: '3',
        'label': 'Other'
    }
}

function modifyPersonalInfo(data) {
    const { date_of_birth, gender, extracurricular, entity_preference_data, first_name, selected_template } = data;
    let templateId = selected_template;
    if (!first_name) {
        localStorage.setItem('newUser', true);
    }
    if (!selected_template && localStorage.getItem('selected_template')) {
        templateId = localStorage.getItem('selected_template')
    }
    data = {
        ...data,
        ...{
            date_of_birth: (date_of_birth && moment(date_of_birth).format('YYYY-MM-DD')) || '',
            gender: (gender && genderDict[gender]) || '',
            selected_template: templateId,
            extracurricular: (extracurricular && extracurricular.split(',').map(key => ({
                'value': key,
                'label': key
            }))) || '',
        }
    };
    return data;
}

function* getPersonalDetails(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        const { payload } = action;
        const loader = payload && payload.noUiLoader ? false : true
        
        if (localStorage.getItem('personalInfo')) {
            yield put({
                type: Actions.SAVE_USER_INFO,
                data: modifyPersonalInfo(JSON.parse(localStorage.getItem('personalInfo')) || [])
            });
            return;
        }
        
        yield put({ type: UPDATE_UI, data: { loader } });
        const result = yield call(Api.fetchPersonalInfo, candidateId);
        
        if (result['error']) {
            Toast.fire({
                type: 'error',
                title: result['errorMessage']
            });
        }
        
        
        yield put({ type: UPDATE_UI, data: { loader: false } })
        
        let { data } = result;
        data = modifyPersonalInfo(data)
        
        const { active_subscription: subscriptionActive } = data;
        if (subscriptionActive) {
            localStorage.setItem('subscriptionActive', true);
        }
        else {
            localStorage.setItem('subscriptionActive', false);
        }
        yield put({ type: Actions.SAVE_USER_INFO, data: data })
        
    } catch (e) {
        console.log(e);
    }
}

function* getInterestList(action) {
    try {
        const { payload: { value, res, rej } } = action;
        
        
        const result = yield call(Api.fetchInterestList, value);
        if (result['error']) {
            return rej(new SubmissionError({ _error: result['errorMessage'] }));
        }
        let { data: { data } } = result;
        
        const newResult = Object.keys(data).map((el, key) => {
            return { 'value': data[el], 'label': data[el] }
        })
        
        return res(newResult)
        
        
    } catch (e) {
        console.log(e);
    }
}

function* updatePersonalDetails(action) {
    try {
        let { payload: { personalDetails, resolve, reject } } = action;
        
        const candidateId = localStorage.getItem('candidateId') || '';
        delete personalDetails['subscription_status']
        if (localStorage.getItem('newUser')) {
            localStorage.removeItem('newUser')
        }
        const { resume_generated, order_data } = personalDetails;
        
        const isOrderedAndSingle = Object.keys(order_data || {}).length ? (order_data.combo ? false : order_data.expiry ? false : true) : false;
        if (localStorage.getItem('selected_template') && !(resume_generated && isOrderedAndSingle)) {
            personalDetails = {
                ...personalDetails,
                ...{
                    'selected_template': localStorage.getItem('selected_template')
                }
            }
            // localStorage.removeItem('selected_template')
        }
        
        yield put({ type: UPDATE_UI, data: { loader: true } });
        
        let result = null;
        if (localStorage.getItem('personalInfo')) result = yield call(Api.createPersonalInfo, personalDetails);
        else result = yield call(Api.updatePersonalData, personalDetails, candidateId);
        
        if (result['error']) {
            return reject(new SubmissionError({ _error: result['errorMessage'] }));
        }
        
        localStorage.removeItem('personalInfo');
        
        yield put({ type: UPDATE_UI, data: { loader: false } })
        
        
        let { data } = result;
        
        data = modifyPersonalInfo(data)
        
        yield put({ type: Actions.SAVE_USER_INFO, data: data });
        
        return resolve('User Personal  Info saved successfully.');
        
    } catch (e) {
        console.log('error', e);
    }
}


function* fetchImageUrl(action) {
    try {
        const { payload: { imageFile, resolve } } = action;
        
        var data = new FormData();
        
        const imageInfo = {
            'privacy': '2',
            'prefix': 'images',
            'media': imageFile
        };
        
        for (const key in imageInfo) {
            data.append(key, imageInfo[key]);
        }
        yield put({ type: UPDATE_UI, data: { loader: true } });
        
        const candidateId = localStorage.getItem('candidateId') || '';
        
        
        const result = yield call(Api.fetchImageUrl, data, candidateId);
        
        yield put({ type: UPDATE_UI, data: { loader: false } })
        
        return resolve(result['data']['path'])
        
        
    } catch (e) {
        
        console.log('error', e);
    }
}

function* updateEntityPreference(action) {
    try {
        const { payload: { entity_preference_data, resolve, reject, showLoader } } = action;
        const candidateId = localStorage.getItem('candidateId') || '';
        
        if (showLoader) yield put({ type: UPDATE_UI, data: { loader: true } });
        
        const result = yield call(Api.updateEntityPreference, { entity_preference_data }, candidateId);
        
        yield put({ type: UPDATE_UI, data: { loader: false } })
        
        if (result['error']) {
            return reject(new SubmissionError({ _error: result['errorMessage'] }));
        }
        
        
        const data = modifyPersonalInfo(result['data']);
        
        yield put({ type: Actions.SAVE_USER_INFO, data: data });
        return resolve("Entity Updated")
        
    } catch (e) {
        console.log('error', e);
    }
}

function* getComponentTitle(action) {
    try {
        let { payload: { resolve, reject } } = action;
        resolve('Edit-Preview Page | Shine Learning');
    } catch (e) {
        console.log(e);
    }
}


function* getChatBotUrl() {
    var hours = 24; // Reset when storage is more than 24hours
    var now = new Date().getTime();
    var setupTime = localStorage.getItem('setupTime');
    
    try {
        const result = yield call(Api.getChatBotUrl);
        
        if (setupTime == null) {
            if(result['data']['script_link'] != "script not available") {
                localStorage.setItem('script_link', result['data']['script_link'])
                localStorage.setItem('setupTime', now);
            }
        }
        else {
            if(now-setupTime > hours*60*60*1000) {
                localStorage.clear();
                if(result['data']['script_link'] != "script not available") {
                    localStorage.setItem('script_link', result['data']['script_link'])
                    localStorage.setItem('setupTime', now);
                }
            }
        }
    }
    catch (e) {
        console.log(e);
    }
}

export default function* watchPersonalInfo() {
    yield takeEvery(Actions.FETCH_PERSONAL_INFO, getPersonalDetails);
    yield takeLatest(Actions.UPDATE_PERSONAL_INFO, updatePersonalDetails);
    yield takeLatest(Actions.FETCH_IMAGE_URL, fetchImageUrl);
    yield takeLatest(Actions.UPDATE_ENTITY_PREFERENCE, updateEntityPreference);
    yield takeLatest(Actions.FETCH_INTEREST_LIST, getInterestList);
    yield takeLatest(Actions.GET_COMPONENT_TITLE, getComponentTitle);
    yield takeLatest(Actions.GET_CHATBOT_URL, getChatBotUrl);
}