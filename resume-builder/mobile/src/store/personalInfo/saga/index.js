import {Api} from './Api';

import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';
import * as uiAction from '../../ui/actions/actionTypes';

import moment from 'moment'

import {SubmissionError} from 'redux-form'

import {interestList} from '../../../Utils/interestList'

function modifyPersonalInfo(data) {
    let {date_of_birth, gender, extracurricular,image} = data;
    let newData = {
            ...data,
            ...{
                "date_of_birth": (date_of_birth && moment(date_of_birth).format('YYYY-MM-DD')) || '',
                extracurricular: (extracurricular && extracurricular.split(',').map(key => ({
                    'value': key,
                    'label': key
                }))) || '',
                gender,
                image
                }
        }
    return newData;
}

function* getPersonalDetails(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type:uiAction.UPDATE_MAIN_PAGE_LOADER,payload:{mainloader: true}})
        if (localStorage.getItem('personalInfo')) {

            yield put({
                type: Actions.SAVE_USER_INFO,
                data: modifyPersonalInfo(JSON.parse(localStorage.getItem('personalInfo')) || [])
            })
            yield put({type:uiAction.UPDATE_MAIN_PAGE_LOADER,payload:{mainloader: false}})
            return;
        }

        const result = yield call(Api.fetchPersonalInfo, candidateId);
        if (result['error']) {
            console.log('error');
        }
        let {data} = result;
        data =modifyPersonalInfo(data)
        yield put({type: Actions.SAVE_USER_INFO, data: data});

        yield put({type:uiAction.UPDATE_MAIN_PAGE_LOADER,payload:{mainloader: false}})

    } catch (e) {
        console.log(e);
    }
}

function* updatePersonalDetails(action) {
    try {
        let {payload: {personalDetails, resolve, reject}} = action;
        delete personalDetails['subscription_status']
        if(localStorage.getItem('newUser')){
            localStorage.removeItem('newUser')
        }
        if(localStorage.getItem('selected_template')){
            personalDetails = {
                ...personalDetails,
                ...{
                    'selected_template' : localStorage.getItem('selected_template')
                }
            }
        }
        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})

        let result = null;
        if (localStorage.getItem('personalInfo')) result = yield call(Api.createPersonalInfo, personalDetails);
        else result = yield call(Api.updatePersonalData, personalDetails, candidateId);
        
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        localStorage.removeItem('personalInfo');
        

        yield put({type: Actions.SAVE_USER_INFO, data:modifyPersonalInfo(result['data'])});
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})

        return resolve('User Personal  Info saved successfully.');

    } catch (e) {

        console.log('error', e);
    }
}

function* getInterestList(action){
    try{
        const {payload: {value, resolve, reject}} = action;
        const result = yield call(Api.fetchInterestList,value);

        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        let {data:{data}} = result;

        const newResult = Object.keys(data).map((el, key) => {
            return {'value': data[el], 'label': data[el]}
        })

        return resolve(newResult)

    }catch (e) {
        console.log(e);
    }
}


function* fetchImageUrl(action) {
    try {
        const {payload: {imageFile, resolve, reject}} = action;
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})


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
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})


        return resolve(result['data']['path'])


    } catch (e) {

        console.log('error', e);
    }
}

function* updateEntityPreference(action) {
    try {
        const {payload: {entity_preference_data, resolve, reject}} = action;
        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})
        const result = yield call(Api.updateEntityPreference, {entity_preference_data}, candidateId);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        const data = modifyPersonalInfo(result['data']);

        yield put({type: Actions.SAVE_USER_INFO, data: data});
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
        return resolve("ENtity Updated")

    } catch (e) {
        console.log('error', e);
    }
}


export default function* watchPersonalInfo() {
    yield takeLatest(Actions.FETCH_PERSONAL_INFO, getPersonalDetails)
    yield takeLatest(Actions.UPDATE_PERSONAL_INFO, updatePersonalDetails)
    yield takeLatest(Actions.FETCH_IMAGE_URL, fetchImageUrl)
    yield takeLatest(Actions.FETCH_INTEREST_LIST, getInterestList);
    yield takeLatest(Actions.UPDATE_ENTITY_PREFERENCE, updateEntityPreference);

}