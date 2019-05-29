import {Api} from './Api';

import {takeLatest, put, call,select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';
import * as uiAction from '../../ui/actions/actionTypes';

import {SubmissionError} from 'redux-form'

const getUIStatus = state => state.ui;

function* fetchUserAward(action) {
    try {
        let x=10
        const candidateId = localStorage.getItem('candidateId') || '';
        const ui = yield select(getUIStatus)
        if(!ui.mainloader){
            yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})
        }

        if (localStorage.getItem('award')) {
            let local_data = JSON.parse(localStorage.getItem('award')).length ? 
                            JSON.parse(localStorage.getItem('award')) :
                            [
                                {
                                    "candidate_id": '',
                                    "id": '',
                                    "title": '',
                                    "date": '',
                                    "summary": '',
                                    "order": 0
                                }
                            ]

            yield put({type: Actions.SAVE_USER_AWARD, data: {list:local_data}})

            yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
            return;
        }
        
        const result = yield call(Api.fetchUserAward, candidateId);
        if (result['error']) {
        }
        const {data: {results}} = result;
        results.sort((a,b) => (a.order > b.order) ? 1 : ((b.order > a.order) ? -1 : 0));
        let data = {list: results};
        if(! data.list.length){
            data = {
                ...data,
                ...{
                    list: [
                        {
                            "candidate_id": '',
                            "id": '',
                            "title": '',
                            "date": '',
                            "summary": '',
                            "order": 0
                        }
                    ]
                }
            };
        }
        yield put({type: Actions.SAVE_USER_AWARD, data: data})
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
    } catch (e) {
    }
}


function* bulkUpdateUserAward(action) {
    try {
        let {payload: {list,resolve,reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})

        const result = yield call(Api.bulkUpdateUserAward, list, candidateId);

        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        else{
            
            if (localStorage.getItem('award')){
                localStorage.removeItem('award')
                yield call(fetchUserAward)
            }
            
            yield put({type: Actions.SAVE_USER_AWARD, data:{list:result['data']}});
            yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
            return resolve('Bulk Update Done.');
        }

    } catch (e) {
        console.log('error', e);
    }
}


function* deleteUserAward(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})

        const {awardId} = action;

        const result = yield call(Api.deleteUserAward, candidateId, awardId);


        if (result['error']) {
            console.log(result['error'])
        }
        // yield call(fetchUserLanguage)
        yield put({type: Actions.REMOVE_AWARD, id: awardId});
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
        yield call(fetchUserAward)
        

    } catch (e) {
        console.log('error', e);
    }
}


export default function* watchAward() {
    yield takeLatest(Actions.FETCH_USER_AWARD, fetchUserAward);
    yield takeLatest(Actions.DELETE_USER_AWARD, deleteUserAward);
    yield takeLatest(Actions.BULK_UPDTATE_USER_AWARD, bulkUpdateUserAward);
}