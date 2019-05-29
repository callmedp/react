import {call, takeLatest, put, all} from 'redux-saga/effects'

import * as Actions from '../actions/actionTypes'
import {Api} from "./Api";
import {UPDATE_UI} from "../../ui/actions/actionTypes";
import {
    FETCH_TEMPLATE_IMAGES,
    SET_CUSTOMIZATION,
    SAVE_TEMPLATE_IMAGES,
    SAVE_THUMBNAIL_IMAGES
} from "../actions/actionTypes";
import {FETCH_THUMBNAIL_IMAGES} from "../actions/actionTypes";


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


        let {data} = result;

        data = {
            ...data,
            ...{
                templateId: data['template_no']
            }
        };

        yield put({type: SET_CUSTOMIZATION, data: data});

        yield call(fetchTemplate, {payload: {template: data['templateId']}})


        yield put({type: UPDATE_UI, data: {loader: false}});


    } catch (e) {
        console.log(e);
    }
}


function* fetchTemplateImages(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
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
        const images = result.map(el => el.data);
        yield  put({type: SAVE_TEMPLATE_IMAGES, data: {templateImages: images}});

        yield put({type: UPDATE_UI, data: {loader: false}});

        // yield call(fetchTemplate)

    } catch (e) {
        console.log(e);
    }
}


function* fetchThumbnailImages(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type: UPDATE_UI, data: {loader: true}});

        const query = 'tsize=151x249';
        const result = yield all([
            call(Api.fetchTemplateImages, candidateId, 1, query),
            call(Api.fetchTemplateImages, candidateId, 2, query),
            call(Api.fetchTemplateImages, candidateId, 3, query),
            call(Api.fetchTemplateImages, candidateId, 4, query),
            call(Api.fetchTemplateImages, candidateId, 5, query),
        ]);
        if (result['error']) {
            console.log('error');
        }
        const images = result.map(el => el.data);
        yield  put({type: SAVE_THUMBNAIL_IMAGES, data: {thumbnailImages: images}});

        yield put({type: UPDATE_UI, data: {loader: false}});

        // yield call(fetchTemplate)

    } catch (e) {
        console.log(e);
    }
}


function* fetchDefaultCustomization(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type: UPDATE_UI, data: {loader: true}});
        const {payload: {templateId, resolve, reject}} = action;
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


        yield put({type: UPDATE_UI, data: {loader: false}});


        resolve(data)

        // yield call(fetchTemplate)

    } catch (e) {
        console.log(e);
    }
}


function* reorderSection(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type: UPDATE_UI, data: {loader: true}});
        const {payload: {templateId, info}} = action;
        const result = yield call(Api.reorderSection, candidateId, templateId, info);

        if (result['error']) {
            console.log('error');
        }
        let {data: {data}} = result;
        // console.log('order ----', JSON.parse(data));
        data = {
            entity_position: data
        }

        yield put({type: SET_CUSTOMIZATION, data: data});


        yield call(fetchTemplate, {payload: {template: templateId}})


        yield put({type: UPDATE_UI, data: {loader: false}});


        // yield call(fetchTemplate)

    } catch
        (e) {
        console.log(e);
    }
}


export default function* watchTemplate() {
    yield  takeLatest(Actions.FETCH_TEMPLATE, fetchTemplate)
    yield  takeLatest(Actions.CUSTOMIZE_TEMPLATE, customizeTemplate)
    yield  takeLatest(Actions.FETCH_TEMPLATE_IMAGES, fetchTemplateImages)
    yield  takeLatest(Actions.FETCH_DEFAULT_CUSTOMIZATION, fetchDefaultCustomization)
    yield  takeLatest(Actions.FETCH_SELECTED_TEMPLATE_IMAGE, fetchTemplateImages)
    yield  takeLatest(Actions.FETCH_THUMBNAIL_IMAGES, fetchThumbnailImages)
    yield  takeLatest(Actions.REORDER_SECTION, reorderSection)

}