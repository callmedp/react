import {Api} from './Api';

import {takeLatest, put, call,select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';
import * as LoaderAction from '../../loader/actions/actionTypes';

import {SubmissionError} from 'redux-form'

const getLoaderStatus = state => state.loader;

function* fetchUserAward(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        const loader = yield select(getLoaderStatus)
        if(!loader.mainloader){
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})
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

            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
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
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
    } catch (e) {
    }
}

function* updateUserAward(action) {
    try {
        const {payload: {userAward, resolve, reject}} = action;

        const candidateId = localStorage.getItem('candidateId') || '';

        const {id} = userAward;
        const result = yield call(id ? Api.updateUserAward : Api.createUserAward, userAward, candidateId, id);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        
        yield put({type: Actions.SAVE_USER_AWARD, data: result['data']});

        return resolve('User Award  Info saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}


function* bulkUpdateUserAward(action) {
    try {
        let {payload: {list,resolve,reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})

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
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
            return resolve('Bulk Update Done.');
        }

    } catch (e) {
        console.log('error', e);
    }
}


function* deleteUserAward(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})

        const {awardId} = action;

        const result = yield call(Api.deleteUserAward, candidateId, awardId);


        if (result['error']) {
            console.log(result['error'])
        }
        // yield call(fetchUserLanguage)
        yield put({type: Actions.REMOVE_AWARD, id: awardId});
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
        yield call(fetchUserAward)
        

    } catch (e) {
        console.log('error', e);
    }
}


export default function* watchAward() {
    yield takeLatest(Actions.FETCH_USER_AWARD, fetchUserAward);
    yield takeLatest(Actions.UPDATE_USER_AWARD, updateUserAward);
    yield takeLatest(Actions.DELETE_USER_AWARD, deleteUserAward);
    yield takeLatest(Actions.BULK_UPDTATE_USER_AWARD, bulkUpdateUserAward);
}