import {call, takeLatest, put,select,all} from 'redux-saga/effects'

import * as Actions from '../actions/actionTypes'
import {Api} from "./Api";
import * as LoaderAction from '../../loader/actions/actionTypes';
import {FETCH_TEMPLATE_IMAGES, SET_CUSTOMIZATION} from "../actions/actionTypes";


const getLoaderStatus = state => state.loader;

const getTemplateNo = state => state.personalInfo.selected_template

String.prototype.splice = function(idx, rem, str) {
    return this.slice(0, idx) + str + this.slice(idx + Math.abs(rem));
};

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

        console.log(scale)
        
        
        let  newhtml = html.splice(pos + 5, 0, ` style ="transform-origin: top left;
                                                    transform: scale(${scale});
                                                    width: 1236px;
                                                    max-height: 105vh;"`)
        yield put({type: Actions.SAVE_TEMPLATE, data:{html : newhtml}})
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