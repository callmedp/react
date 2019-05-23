import {call, takeLatest, put,select} from 'redux-saga/effects'

import * as Actions from '../actions/actionTypes'
import {Api} from "./Api";
import * as LoaderAction from '../../loader/actions/actionTypes';


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
        // yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
    } catch (e) {
        ////console.log(e);
    }
}

export default function* watchTemplate() {
    yield  takeLatest(Actions.FETCH_TEMPLATE, fetchTemplate)
}