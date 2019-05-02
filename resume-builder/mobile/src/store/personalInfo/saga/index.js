import {Api} from './Api';

import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';
import * as LoaderAction from '../../loader/actions/actionTypes';

import moment from 'moment'

import {SubmissionError} from 'redux-form'

import {interestList} from '../../../Utils/interestList'

function modifyPersonalInfo(data) {
    const {date_of_birth, gender, extracurricular ,entity_preference_data} = data;

        data = {
            ...data,
            ...{
                date_of_birth: date_of_birth && moment(date_of_birth).format('YYYY-MM-DD') || '',
                extracurricular: extracurricular.split(',').map(key => interestList[key]),
                entity_preference_data :entity_preference_data.map((obj,key) => {
                                                    if(obj.entity_id ===1 || obj.entity_id === 2 || obj.entity_id === 5){
                                                        obj.active =true
                                                    }
                                                    return obj;
                                                })
            }
        }
    return data;
}

function* getPersonalDetails(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';

        if (localStorage.getItem('personalInfo')) {

            yield put({
                type: Actions.SAVE_USER_INFO,
                data: modifyPersonalInfo(JSON.parse(localStorage.getItem('personalInfo')) || [])
            })
            return;
        }

        const result = yield call(Api.fetchPersonalInfo, candidateId);
        if (result['error']) {
            ////console.log('error');
        }
        let {data} = result;
        data =modifyPersonalInfo(data)
        ////console.log('data');
        yield put({type: Actions.SAVE_USER_INFO, data: data});

        yield put({type:LoaderAction.UPDATE_MAIN_PAGE_LOADER,payload:{mainloader: false}})
        // yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: false}})

    } catch (e) {
        ////console.log(e);
    }
}

function* updatePersonalDetails(action) {
    try {
        const {payload: {personalDetails, resolve, reject}} = action;

        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: true}})
        const result = yield call(Api.updatePersonalData, personalDetails, candidateId);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        localStorage.removeItem('personalInfo');

        yield put({type: Actions.SAVE_USER_INFO, data:result['data']});
        // yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: false}})

        return resolve('User Personal  Info saved successfully.');

    } catch (e) {

        ////console.log('error', e);
    }
}


function* fetchImageUrl(action) {
    try {
        const {payload: {imageFile, resolve, reject}} = action;

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

        ////console.log('error', e);
    }
}


export default function* watchPersonalInfo() {
    yield takeLatest(Actions.FETCH_PERSONAL_INFO, getPersonalDetails)
    yield takeLatest(Actions.UPDATE_PERSONAL_INFO, updatePersonalDetails)
    yield takeLatest(Actions.FETCH_IMAGE_URL, fetchImageUrl)

}