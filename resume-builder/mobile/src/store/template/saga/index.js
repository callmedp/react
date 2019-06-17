import {call, takeLatest, put,select,all} from 'redux-saga/effects'

import * as Actions from '../actions/actionTypes'
import {Api} from './Api';
import {apiError} from '../../../Utils/apiError';
import * as uiAction from '../../ui/actions/actionTypes';
import {SAVE_THUMBNAIL_IMAGES, SET_CUSTOMIZATION,SAVE_TEMPLATE_IMAGES} from "../actions/actionTypes";
import {SubmissionError} from 'redux-form'


const getUIStatus = state => state.ui;

const getTemplateNo = state => state.personalInfo.selected_template

String.prototype.splice = function(idx, rem, str) {
    return this.slice(0, idx) + str + this.slice(idx + Math.abs(rem));
};

function* fetchTemplate(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        const ui = yield select(getUIStatus)
        const selected_template = yield select((getTemplateNo|| 1))
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})

        const result = yield call(Api.fetchTemplate, candidateId,selected_template);
        if (result['error']) {
            apiError();
        }
        let w = window,
            d = document,
            e = d.documentElement,
            g = d.getElementsByTagName('body')[0],
            width = w.innerWidth || e.clientWidth || g.clientWidth;
        
        let htmlString = '<html'
        let html = result['data'] && result['data'].html
        let pos = html.indexOf(htmlString)
        let scale
        switch(true){
            case (width>400 && width <=500) : scale = 0.37; break;
            case (width>500 && width <=600) : scale = 0.45; break;
            case (width>600 && width <=700) : scale = 0.53; break;
            case (width>700) : scale = 0.6; break;
            default : scale = 0.32; break;
        }
        
        
        let  zoomOut = html.splice(pos + 5, 0, ` style ="transform-origin: top left;
                                                    transform: scale(${scale});
                                                    width: 1236px;
                                                    max-height: 105vh;"`)

        let zoomIn = html.splice(pos + 5, 0, ` style ="transform-origin: top left;
                                                width: 1236px;
                                                max-height: 105vh;"`)
        yield put({type: Actions.SAVE_TEMPLATE, data:{html : zoomOut,zoomInHtml:zoomIn}})
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
    } catch (e) {
        apiError();
    }
}

function* customizeTemplate(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})
        const {payload:{resolve,reject,template_data}} = action;
        const result = yield call(Api.customizeTemplate, candidateId, template_data.template, template_data);
        if (result['error']) {
            apiError();
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }


        let {data} = result;
        let {entity_position,template_no} = data

        data = {
            ...data,
            ...{
                entity_position:JSON.parse(entity_position),
                templateId: template_no
            }
        };

        yield put({type: SET_CUSTOMIZATION, data: data});
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
        return resolve("Customize Done")

    } catch (e) {
        apiError();
    }
}

function* reorderSection(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})
        const {payload: {templateId, info}} = action;
        const result = yield call(Api.reorderSection, candidateId, templateId, info);
        if (result['error']) {
            apiError();
        }
        let {data: {data}} = result;

        let entity_position = data && eval(data) || []
        let error = false
        if(entity_position[info.pos-1].entity_id === info.entity_id){
            error =true
        } 
        
        data = {
            entity_position: JSON.parse(data),
            reorderFailToast: error
        }

        yield put({type: SET_CUSTOMIZATION, data:data});
        yield call(fetchTemplate)

        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
        // yield call(fetchTemplate)

    } catch
        (e) {
        apiError();
    }
}

function* fetchThumbnailImages(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        // yield put({type: UPDATE_UI, data: {loader: true}});

        const query = 'tsize=151x249';
        const result = yield all([
            call(Api.fetchTemplateImages, candidateId, 1, query),
            call(Api.fetchTemplateImages, candidateId, 2, query),
            call(Api.fetchTemplateImages, candidateId, 3, query),
            call(Api.fetchTemplateImages, candidateId, 4, query),
            call(Api.fetchTemplateImages, candidateId, 5, query),
        ]);
        if (result['error']) {
            apiError();
        }
        const images = result.map(el => el.data);
        yield  put({type: SAVE_THUMBNAIL_IMAGES, data: {thumbnailImages: images}});

        // yield put({type: UPDATE_UI, data: {loader: false}});

        // yield call(fetchTemplate)

    } catch (e) {
        apiError();
    }
}


function* fetchTemplateImages(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        const {payload:{resolve,reject,template_id}} = action;
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})

        const result = yield call(Api.fetchTemplateImages, candidateId, template_id);
        if (result['error']) {
            apiError();
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        const images = result['data']
        yield  put({type: SAVE_TEMPLATE_IMAGES, data: {templateImage: images}});

        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
        return resolve("Image Received")

    } catch (e) {
        apiError();
    }
}


function* fetchDefaultCustomization(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        const {templateId} = action;
        const result = yield call(Api.fetchDefaultCustomization, candidateId, templateId);

        if (result['error']) {
            apiError();
        }
        let {data} = result;
        let {entity_position,template_no} = data

        data = {
            ...data,
            ...{
                entity_position: JSON.parse(entity_position),
                templateId: template_no
            }
        }

        yield put({type: SET_CUSTOMIZATION, data: data});

    } catch (e) {
        apiError();
    }
}

export default function* watchTemplate() {
    yield  takeLatest(Actions.FETCH_TEMPLATE, fetchTemplate)
    yield  takeLatest(Actions.CUSTOMIZE_TEMPLATE, customizeTemplate)
    yield  takeLatest(Actions.FETCH_DEFAULT_CUSTOMIZATION, fetchDefaultCustomization)
    yield  takeLatest(Actions.REORDER_SECTION, reorderSection)
    yield  takeLatest(Actions.FETCH_SELECTED_TEMPLATE_IMAGE, fetchTemplateImages)
    yield  takeLatest(Actions.FETCH_THUMBNAIL_IMAGES, fetchThumbnailImages)
}