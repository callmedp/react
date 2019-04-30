import {Api} from './Api';

import {takeLatest, put, call} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import moment from 'moment'

import {SubmissionError} from 'redux-form'

import {interestList} from '../../../Utils/interestList'
import {UPDATE_UI} from "../../ui/actions/actionTypes";

const genderDict = {
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
    const {date_of_birth, gender, extracurricular} = data;
    data = {
        ...data,
        ...{
            date_of_birth: (date_of_birth && moment(date_of_birth).format('YYYY-MM-DD')) || '',
            gender: (gender && genderDict[gender]) || '',
            extracurricular: (extracurricular && extracurricular.split(',').map(key => interestList[key])) || ''
        }
    }
    return data;
}

function* getPersonalDetails(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';

        yield put({type: UPDATE_UI, data: {loader: true}})


        if (localStorage.getItem('personalInfo')) {

            yield put({
                type: Actions.SAVE_USER_INFO,
                data: modifyPersonalInfo(JSON.parse(localStorage.getItem('personalInfo')) || [])
            })
            return;
        }

        const result = yield call(Api.fetchPersonalInfo, candidateId);
        if (result['error']) {
            console.log('error');
        }
        yield put({type: UPDATE_UI, data: {loader: false}})

        let {data} = result;
        data = modifyPersonalInfo(data)
        console.log('data');
        yield put({type: Actions.SAVE_USER_INFO, data: data})
    } catch (e) {
        console.log(e);
    }
}

function* updatePersonalDetails(action) {
    try {
        const {payload: {personalDetails, resolve, reject}} = action;

        const candidateId = localStorage.getItem('candidateId') || '';

        yield put({type: UPDATE_UI, data: {loader: false}})

        const result = yield call(Api.updatePersonalData, personalDetails, candidateId);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        localStorage.removeItem('personalInfo');

        yield put({type: UPDATE_UI, data: {loader: true}})


        yield put({type: Actions.SAVE_USER_INFO, data: result['data']});

        return resolve('User Personal  Info saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}


function* fetchImageUrl(action) {
    try {
        const {payload: {imageFile, resolve}} = action;

        var data = new FormData();

        const imageInfo = {
            'privacy': '2',
            'prefix': 'images',
            'media': imageFile
        };

        for (const key in imageInfo) {
            data.append(key, imageInfo[key]);
        }

        const candidateId = localStorage.getItem('candidateId') || '';

        const result = yield call(Api.fetchImageUrl, data, candidateId);

        return resolve(result['data']['path'])


    } catch (e) {

        console.log('error', e);
    }
}

function* updateEntityPreference(action) {
    try {
        const {payload} = action;
        const candidateId = localStorage.getItem('candidateId') || '';

        const result = yield call(Api.updateEntityPreference, payload, candidateId);
        yield put({type: Actions.SAVE_USER_INFO, data: result['data']});

    } catch (e) {
        console.log('error', e);
    }
}

export default function* watchPersonalInfo() {
    yield takeLatest(Actions.FETCH_PERSONAL_INFO, getPersonalDetails);
    yield takeLatest(Actions.UPDATE_PERSONAL_INFO, updatePersonalDetails);
    yield takeLatest(Actions.FETCH_IMAGE_URL, fetchImageUrl);
    yield takeLatest(Actions.UPDATE_ENTITY_PREFERENCE, updateEntityPreference);

}