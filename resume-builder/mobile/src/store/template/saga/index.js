import {call, takeLatest, put,select,all} from 'redux-saga/effects'

import * as Actions from '../actions/actionTypes'
import {Api} from "./Api";
import * as LoaderAction from '../../loader/actions/actionTypes';
import {FETCH_TEMPLATE_IMAGES, SET_CUSTOMIZATION} from "../actions/actionTypes";


const getLoaderStatus = state => state.loader;

const getTemplateNo = state => state.personalInfo.selected_template

function* fetchTemplate(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        const loader = yield select(getLoaderStatus)
        const selected_template = yield select(getTemplateNo)
        if(!loader.mainloader){
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})
        }

        const result = yield call(Api.fetchTemplate, candidateId,selected_template);
        if (result['error']) {
            ////console.log('error');
        }
        ////console.log(result)

        yield put({type: Actions.SAVE_TEMPLATE, data: result['data']})
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
    } catch (e) {
        ////console.log(e);
    }
}

function* customizeTemplate(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        // yield put({type: UPDATE_UI, data: {loader: true}});
        const {payload} = action;
        const result = yield call(Api.customizeTemplate, candidateId, payload.template, payload);
        if (result['error']) {
            console.log('error');
        }


        let {data} = result;

        data = {
            ...data,
            ...{
                templateId: data['template_no']
            }
        };

        yield put({type: SET_CUSTOMIZATION, data: data});


        // yield put({type: UPDATE_UI, data: {loader: false}});

        // yield call(fetchTemplate)

    } catch (e) {
        console.log(e);
    }
}


function* fetchTemplateImages(action) {
    try {
        const candidateId = 12; //localStorage.getItem('candidateId') || '';
        // yield put({type: UPDATE_UI, data: {loader: true}});

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
        // yield put({type: UPDATE_UI, data: {loader: false}});

        // yield call(fetchTemplate)

    } catch (e) {
        console.log(e);
    }
}


function* fetchDefaultCustomization(action) {
    try {
        const candidateId = 12; //localStorage.getItem('candidateId') || '';
        // yield put({type: UPDATE_UI, data: {loader: true}});
        const {templateId} = action;
        const result = yield call(Api.fetchDefaultCustomization, candidateId, templateId);

        if (result['error']) {
            console.log('error');
        }
        let {data} = result;

        data = {
            ...data,
            ...{
                templateId: data['template_no']
            }
        }

        yield put({type: SET_CUSTOMIZATION, data: data});

        // yield put({type: UPDATE_UI, data: {loader: false}});


        // yield call(fetchTemplate)

    } catch (e) {
        console.log(e);
    }
}

export default function* watchTemplate() {
    yield  takeLatest(Actions.FETCH_TEMPLATE, fetchTemplate)
    yield  takeLatest(Actions.CUSTOMIZE_TEMPLATE, customizeTemplate)
    yield  takeLatest(Actions.FETCH_TEMPLATE_IMAGES, fetchTemplateImages)
    yield  takeLatest(Actions.FETCH_DEFAULT_CUSTOMIZATION, fetchDefaultCustomization)
}