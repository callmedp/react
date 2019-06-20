import {call, takeLatest, put, all} from 'redux-saga/effects'

import * as Actions from '../actions/actionTypes'
import {Api} from "./Api";
import {UPDATE_UI} from "../../ui/actions/actionTypes";
import {
    SET_CUSTOMIZATION,
    SAVE_TEMPLATE_IMAGES,
    SAVE_THUMBNAIL_IMAGES
} from "../actions/actionTypes";
import {SHOW_ALERT_MODAL} from "../../ui/actions/actionTypes"
import {Toast} from "../../../services/ErrorToast";

function* fetchTemplate(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type: UPDATE_UI, data: {loader: true}});
        const {template} = action.payload;
        const result = yield call(Api.fetchTemplateImages, candidateId, template);

        yield put({type: UPDATE_UI, data: {loader: false}});

        if (result['error']) {
            Toast.fire({
                type: 'error',
                title: result['errorMessage']
            });
        }

        let {data} = result;
        yield put({type: Actions.SAVE_TEMPLATE, data: {"templateToPreview": data}});
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
            Toast.fire({
                type: 'error',
                title: result['errorMessage']
            });
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


function* fetchSelectedTemplateImage(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type: UPDATE_UI, data: {loader: true}});
        const {payload: {templateId, resolve, reject, isModal}} = action;
        const result = yield call(Api.fetchTemplateImages, candidateId, templateId)

        if (result['error']) {
            return reject("API request Failed")

        }
        if (isModal) {
            yield  put({type: SAVE_TEMPLATE_IMAGES, data: {modalTemplateImage: result['data']}});
            yield put({type: UPDATE_UI, data: {loader: false}});
            return resolve("Got the Modal Template Selected")
        }
        // const images = result.map(el => el.data);
        yield  put({type: SAVE_TEMPLATE_IMAGES, data: {templateImage: result['data']}});

        yield put({type: UPDATE_UI, data: {loader: false}});
        return resolve("Got the Template Selected")

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
            Toast.fire({
                type: 'error',
                title: result['errorMessage']
            });
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
        // yield put({type: UPDATE_UI, data: {loader: true}});
        const {payload: {templateId, resolve, reject}} = action;
        const result = yield call(Api.fetchDefaultCustomization, candidateId, templateId);

        if (result['error']) {
            Toast.fire({
                type: 'error',
                title: result['errorMessage']
            });
            return reject(result['errorMessage'])

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
            Toast.fire({
                type: 'error',
                title: result['errorMessage']
            });
        }
        let {data: {data}} = result;
        let entity_position = (data && eval(data)) || [];
        if (entity_position[info.pos - 1].entity_id === info.entity_id) {
            yield  put({type: SHOW_ALERT_MODAL, data: {alertModal: true, alertType: 'error'}});
        }

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
    yield  takeLatest(Actions.FETCH_DEFAULT_CUSTOMIZATION, fetchDefaultCustomization)
    yield  takeLatest(Actions.FETCH_SELECTED_TEMPLATE_IMAGE, fetchSelectedTemplateImage)
    yield  takeLatest(Actions.FETCH_THUMBNAIL_IMAGES, fetchThumbnailImages)
    yield  takeLatest(Actions.REORDER_SECTION, reorderSection)

}