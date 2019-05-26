import {Api} from './Api';

import {takeLatest, put, call,select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';
import * as LoaderAction from '../../loader/actions/actionTypes';

import {SubmissionError} from 'redux-form'

const getLoaderStatus = state => state.loader;

function* fetchUserReference(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        const loader = yield select(getLoaderStatus)
        if(!loader.mainloader){
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: true}})
        }

        if (localStorage.getItem('reference')) {

            let local_data = JSON.parse(localStorage.getItem('reference')).length ? 
                            JSON.parse(localStorage.getItem('reference')) :
                            [
                                {
                                    "candidate_id": '',
                                    "id": '',
                                    "reference_name": '',
                                    "reference_designation": '',
                                    "about_user": "",
                                    "order": 0
                                }
                            ]

            yield put({type: Actions.SAVE_USER_REFERENCE, data: {list:local_data}})
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: false}})
            return;
        }

        const result = yield call(Api.fetchUserReference, candidateId);
        if (result['error']) {
            ////console.log('error');
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
                                "reference_name": '',
                                "reference_designation": '',
                                "about_user": "",
                                "order": 0
                            }
                        ]
                }
            };
        }
        yield put({type: Actions.SAVE_USER_REFERENCE, data: data})
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: false}})
    } catch (e) {
        ////console.log(e);
    }
}


function* updateUserReference(action) {
    try {
        let {payload: {userReference, resolve, reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';

        const {id} = userReference;

        const result = yield call(id ? Api.updateUserReference : Api.createUserReference, userReference, candidateId, id);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        yield put({type: Actions.SAVE_USER_REFERENCE, data: result['data']});

        return resolve('User Reference have saved successfully.');

    } catch (e) {
        ////console.log('error', e);
    }
}


function* bulkUpdateUserReference(action) {
    try {
        let {payload: {list,resolve,reject}} = action;
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: true}})


        const candidateId = localStorage.getItem('candidateId') || '';


        const result = yield call(Api.bulkUpdateUserReference, list, candidateId);

        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        else{
            if (localStorage.getItem('reference')){
                localStorage.removeItem('reference')
                yield call(fetchUserReference)
            }
            yield put({type: Actions.SAVE_USER_REFERENCE, data: {list: result['data']}})
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: false}})
            return resolve('Bulk Update Done.');
            
        }
        ////console.log('---', result);
        // yield call(fetchUserLanguage)

    } catch (e) {
        ////console.log('error', e);
    }
}


function* deleteUserReference(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: true}})

        const {referenceId} = action;

        const result = yield call(Api.deleteUserReference, candidateId, referenceId);


        if (result['error']) {
            ////console.log(result['error'])
        }
        // yield call(fetchUserLanguage)
        yield put({type: Actions.REMOVE_REFERENCE, id: referenceId});
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: false}})
        yield call(fetchUserReference)

    } catch (e) {
        ////console.log('error', e);
    }
}


export default function* watchReference() {
    yield takeLatest(Actions.FETCH_USER_REFERENCE, fetchUserReference);
    yield takeLatest(Actions.UPDATE_USER_REFERENCE, updateUserReference);
    yield takeLatest(Actions.DELETE_USER_REFERENCE, deleteUserReference);
    yield takeLatest(Actions.BULK_UPDATE_USER_REFERENCE, bulkUpdateUserReference);

}