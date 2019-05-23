import {Api} from './Api';

import {takeLatest, put, call,select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';
import * as LoaderAction from '../../loader/actions/actionTypes';

import {SubmissionError} from 'redux-form'

const getLoaderStatus = state => state.loader;

function* fetchUserEducation(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        const loader = yield select(getLoaderStatus)
        if(!loader.mainloader){
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: true}})
        }
        if (localStorage.getItem('education')) {

            yield put({
                type: Actions.SAVE_USER_EDUCATION,
                data:{list: JSON.parse(localStorage.getItem('education'))
                 || [
                    {
                    "candidate_id": '',
                    "id": '',
                    "specialization": '',
                    "institution_name": '',
                    "course_type": '',
                    "start_date": '',
                    "percentage_cgpa": '',
                    "end_date": '',
                    "is_pursuing": false,
                    "order": 0}
            ]}})
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: false}})
            return;
        }

        const result = yield call(Api.fetchUserEducation, candidateId);
        if (result['error']) {
            ////console.log('error');
        }
        const {data: {results}} = result;
        results.sort((a,b) => (a.order > b.order) ? 1 : ((b.order > a.order) ? -1 : 0));
        let data = {list: results};
        data = {
            ...data,
            ...{
                list: data['list']
            }
        };


        if(! data.list.length){
            data = {
                ...data,
                ...{
                    list: [
                            {
                            "candidate_id": '',
                            "id": '',
                            "specialization": '',
                            "institution_name": '',
                            "course_type": '',
                            "start_date": '',
                            "percentage_cgpa": '',
                            "end_date": '',
                            "is_pursuing": false,
                            "order": 0}
                    ]
                }
            };
        }
        yield put({type: Actions.SAVE_USER_EDUCATION, data: data})
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: false}})
    } catch (e) {
        ////console.log(e);
    }
}

function* updateUserEducation(action) {
    try {
        const {payload: {userEducation, resolve, reject}} = action;

        const candidateId = localStorage.getItem('candidateId') || '';

        const {id} = userEducation;
        ////console.log('--user Education-');
        const result = yield call(id ? Api.updateUserEducation : Api.createUserEducation, userEducation, candidateId, id);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        return resolve('User Education  Info saved successfully.');

    } catch (e) {
        ////console.log('error', e);
    }
}


function* bulkUpdateUserEducation(action) {
    try {
        console.log("My Action",action)
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: true}})
        let {payload: {list,resolve,reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';


        const result = yield call(Api.bulkUpdateUserEducation, list, candidateId);

        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        else{
            if (localStorage.getItem('education')){
                localStorage.removeItem('education')
                yield call(fetchUserEducation)
            }
            yield put({type: Actions.SAVE_USER_EDUCATION, data:{list: result['data']}})
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: false}})
            console.log("Came Here before resolve")
            console.log(resolve)
            return resolve('Bulk Update Done.');
        }

        ////console.log('---', result);
        // yield call(fetchUserLanguage)

    } catch (e) {
        ////console.log('error', e);
    }
}


function* deleteUserEducation(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: true}})

        const {educationId} = action;

        const result = yield call(Api.deleteUserEducation, candidateId, educationId);


        if (result['error']) {
            ////console.log(result['error'])
        }
        // yield call(fetchUserLanguage)
        yield put({type: Actions.REMOVE_EDUCATION, id: educationId});
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: false}})
        yield call(fetchUserEducation)
        

    } catch (e) {
        ////console.log('error', e);
    }
}


export default function* watchEducation() {
    yield takeLatest(Actions.FETCH_USER_EDUCATION, fetchUserEducation);
    yield takeLatest(Actions.UPDATE_USER_EDUCATION, updateUserEducation);
    yield takeLatest(Actions.DELETE_USER_EDUCATION, deleteUserEducation);
    yield takeLatest(Actions.BULK_UPDATE_USER_EDUCATION , bulkUpdateUserEducation);

}