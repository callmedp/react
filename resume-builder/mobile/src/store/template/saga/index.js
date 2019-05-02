import {call, takeLatest, put,select} from 'redux-saga/effects'

import * as Actions from '../actions/actionTypes'
import {Api} from "./Api";
import * as LoaderAction from '../../loader/actions/actionTypes';


const getLoaderStatus = state => state.loader;

function* fetchTemplate(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        const loader = yield select(getLoaderStatus)
        if(!loader.mainloader){
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: true}})
        }

        const result = yield call(Api.fetchTemplate, candidateId);
        if (result['error']) {
            ////console.log('error');
        }
        ////console.log(result)

        yield put({type: Actions.SAVE_TEMPLATE, data: result['data']})
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: false}})
    } catch (e) {
        ////console.log(e);
    }
}

export default function* watchTemplate() {
    yield  takeLatest(Actions.FETCH_TEMPLATE, fetchTemplate)
}