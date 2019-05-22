import {call, takeLatest, put, all} from 'redux-saga/effects'

import * as Actions from '../actions/actionTypes'
import {Api} from "./Api";
import {UPDATE_UI} from "../../ui/actions/actionTypes";
import {FETCH_TEMPLATE_IMAGES} from "../actions/actionTypes";


function* fetchTemplate(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type: UPDATE_UI, data: {loader: true}});
        const result = yield call(Api.fetchTemplate, candidateId, action.payload.template);
        if (result['error']) {
            console.log('error');
        }
        yield put({type: UPDATE_UI, data: {loader: false}});

        yield put({type: Actions.SAVE_TEMPLATE, data: result['data']})
    } catch (e) {
        console.log(e);
    }
}

function* customizeTemplate(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type: UPDATE_UI, data: {loader: true}});
        const {payload} = action;
        const result = yield call(Api.customizeTemplate, candidateId, payload.template, payload);
        if (result['error']) {
            console.log('error');
        }
        yield put({type: UPDATE_UI, data: {loader: false}});

        // yield call(fetchTemplate)

    } catch (e) {
        console.log(e);
    }
}


function* fetchTemplateImages(action) {
    try {
        const candidateId =  12; //localStorage.getItem('candidateId') || '';
        yield put({type: UPDATE_UI, data: {loader: true}});

        const result = yield all([
            call(Api.fetchTemplateImages, candidateId, 1),
            call(Api.fetchTemplateImages, candidateId, 2),
            call(Api.fetchTemplateImages, candidateId, 3),
            call(Api.fetchTemplateImages, candidateId, 4),
            call(Api.fetchTemplateImages, candidateId, 5),
        ]);
        if (result['error']) {
            console.log('error');
        }
        console.log('---', result)
        yield put({type: UPDATE_UI, data: {loader: false}});

        // yield call(fetchTemplate)

    } catch (e) {
        console.log(e);
    }
}

export default function* watchTemplate() {
    yield  takeLatest(Actions.FETCH_TEMPLATE, fetchTemplate)
    yield  takeLatest(Actions.CUSTOMIZE_TEMPLATE, customizeTemplate)
    yield  takeLatest(Actions.FETCH_TEMPLATE_IMAGES, fetchTemplateImages)

}