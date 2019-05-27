import {Api} from './Api';

import {takeLatest, put, call,select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';
import * as LoaderAction from '../../loader/actions/actionTypes';
import {SubmissionError} from 'redux-form'

const getLoaderStatus = state => state.loader;

function* fetchUserLanguage(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        const loader = yield select(getLoaderStatus)
        if(!loader.mainloader){
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})
        }

        if (localStorage.getItem('language')) {

            let local_data = JSON.parse(localStorage.getItem('language')).length ? 
                            JSON.parse(localStorage.getItem('language')) :
                            [
                                {
                                    "candidate_id": '',
                                    "id": '',
                                    "name": '',
                                    "proficiency": '',
                                    "order": 0
                                }
                            ]

            yield put({type: Actions.SAVE_USER_LANGUAGE, data: {list:local_data}})
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
            return;
        }

        const result = yield call(Api.fetchUserLanguage, candidateId);
        if (result['error']) {
            ////console.log('error');
        }
        let {data: {results}} = result;
        results.sort((a,b) => (a.order > b.order) ? 1 : ((b.order > a.order) ? -1 : 0));
        let data = {list: results};

        data = {
            ...data,
            ...{
                list: data['list']
            }
        }
        if(! data.list.length){
            data = {
                ...data,
                ...{
                    list: [
                            {
                                "candidate_id": '',
                                "id": '',
                                "name": '',
                                "proficiency": '',
                                "order": 0
                            }
                        ]
                }
            };
        }
        yield put({type: Actions.SAVE_USER_LANGUAGE, data: data})
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
    } catch (e) {
        ////console.log(e);
    }
}


function* updateUserLanguage(action) {
    try {
        let {payload: {userLanguage, resolve, reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';

        const {id} = userLanguage;

        const result = yield call(id ? Api.updateUserLanguage : Api.createUserLanguage, userLanguage, candidateId, id);
        // if (result['error']) {
        //     return reject(new SubmissionError({_error: result['errorMessage']}));
        // }
        // yield call(fetchUserLanguage)
        return resolve('User Language  Info saved successfully.');

    } catch (e) {
        ////console.log('error', e);
    }
}


function* bulkUpdateUserLanguage(action) {
    try {
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})
        let {payload: {list,resolve,reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';


        const result = yield call(Api.bulkUpdateUserLanguage, list, candidateId);

        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        else{
            if (localStorage.getItem('language')){
                localStorage.removeItem('language')
                yield call(fetchUserLanguage)
            }
            yield put({type: Actions.SAVE_USER_LANGUAGE, data: {list: result['data']}})
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
            return resolve('Bulk Update Done.');
        }

        ////console.log('-language swap result--', result);
        // yield call(fetchUserLanguage)

    } catch (e) {
        ////console.log('error', e);
    }
}


function* deleteUserLanguage(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})

        // userLanguage['cc_id'] = candidateId;
        const {languageId} = action;

        const result = yield call(Api.deleteUserLanguage, candidateId, languageId);


        if (result['error']) {
            ////console.log(result['error'])
        }
        // yield call(fetchUserLanguage)
        yield put({type: Actions.REMOVE_LANGUAGE, id: languageId});
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
        yield call(fetchUserLanguage)

    } catch (e) {
        ////console.log('error', e);
    }
}

export default function* watchLanguage() {
    yield takeLatest(Actions.FETCH_USER_LANGUAGE, fetchUserLanguage);
    yield takeLatest(Actions.UPDATE_USER_LANGUAGE, updateUserLanguage);
    yield takeLatest(Actions.DELETE_USER_LANGUAGE, deleteUserLanguage);
    yield takeLatest(Actions.BULK_UPDATE_USER_LANGUAGE, bulkUpdateUserLanguage);

}