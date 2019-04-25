import {Api} from './Api';

import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import moment from 'moment'

import {SubmissionError} from 'redux-form'

import {interestList} from '../../../Utils/interestList'
import {entityLinkNameLink ,iconClassList,delete_icon} from '../../../Utils/entitydata'


function* getPersonalDetails(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '5c4ede4da4d7330573d8c79b';

        const result = yield call(Api.fetchPersonalInfo, candidateId);
        if (result['error']) {
            ////console.log('error');
        }
        let {data} = result;
        const {date_of_birth, gender, extracurricular ,entity_preference_data} = data;

        data = {
            ...data,
            ...{
                date_of_birth: date_of_birth && moment(date_of_birth).format('YYYY-MM-DD') || '',
                extracurricular: extracurricular.split(',').map(key => interestList[key]),
                entity_preference_data :entity_preference_data.map((obj,key) => {
                                                    obj.entity_link = entityLinkNameLink[obj.entity_id];
                                                    obj.icon_class = iconClassList[obj.entity_id];
                                                    obj.delete_icon = delete_icon[obj.entity_id];
                                                    if(obj.entity_id ===1 || obj.entity_id == 4){
                                                        obj.active =true
                                                    }
                                                    return obj;
                                                }).sort((a,b)=>b.active -a.active )
            }
        }
        ////console.log('data');
        yield put({type: Actions.SAVE_USER_INFO, data: data})
    } catch (e) {
        ////console.log(e);
    }
}

function* updatePersonalDetails(action) {
    try {
        const {payload: {personalDetails, resolve, reject}} = action;

        const candidateId = localStorage.getItem('candidateId') || '5c4ede4da4d7330573d8c79b';

        const result = yield call(Api.updatePersonalData, personalDetails, candidateId);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }


        yield put({type: Actions.SAVE_USER_INFO, data: result['data']});

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

        const candidateId = localStorage.getItem('candidateId') || '5c4ede4da4d7330573d8c79b';

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