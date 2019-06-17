import {Api} from './Api';
import {apiError} from '../../../Utils/apiError';

import {takeLatest, put, call,select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';
import * as uiAction from '../../ui/actions/actionTypes';

import {SubmissionError} from 'redux-form'

const getUIStatus = state => state.ui;

function* fetchUserEducation(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        const ui = yield select(getUIStatus)
        if(!ui.mainloader){
            yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})
        }
        if (localStorage.getItem('education')) {

            let local_data = JSON.parse(localStorage.getItem('education')) && JSON.parse(localStorage.getItem('education')).length ? 
                            JSON.parse(localStorage.getItem('education')) :
                            [
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

            yield put({type: Actions.SAVE_USER_EDUCATION, data: {list:local_data}})
            yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
            return;
        }

        const result = yield call(Api.fetchUserEducation, candidateId);
        if (result['error']) {
            apiError();
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
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
    } catch (e) {
        apiError();
    }
}

function* updateUserEducation(action) {
    try {
        const {payload: {userEducation, resolve, reject}} = action;

        const candidateId = localStorage.getItem('candidateId') || '';

        const {id} = userEducation;
        const result = yield call(id ? Api.updateUserEducation : Api.createUserEducation, userEducation, candidateId, id);
        if (result['error']) {
            apiError();
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        return resolve('User Education  Info saved successfully.');

    } catch (e) {
        apiError();
    }
}


function* bulkUpdateUserEducation(action) {
    try {
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})
        let {payload: {list,resolve,reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';


        const result = yield call(Api.bulkUpdateUserEducation, list, candidateId);

        if (result['error']) {
            apiError();
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        else{
            if (localStorage.getItem('education')){
                localStorage.removeItem('education')
                yield call(fetchUserEducation)
            }
            yield put({type: Actions.SAVE_USER_EDUCATION, data:{list: result['data']}})
            yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
            return resolve('Bulk Update Done.');
        }

    } catch (e) {
        apiError();
    }
}


function* deleteUserEducation(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})

        const {educationId} = action;

        const result = yield call(Api.deleteUserEducation, candidateId, educationId);


        if (result['error']) {
            apiError();
        }
        // yield call(fetchUserLanguage)
        yield put({type: Actions.REMOVE_EDUCATION, id: educationId});
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
        yield call(fetchUserEducation)
        

    } catch (e) {
        apiError();
    }
}


export default function* watchEducation() {
    yield takeLatest(Actions.FETCH_USER_EDUCATION, fetchUserEducation);
    yield takeLatest(Actions.UPDATE_USER_EDUCATION, updateUserEducation);
    yield takeLatest(Actions.DELETE_USER_EDUCATION, deleteUserEducation);
    yield takeLatest(Actions.BULK_UPDATE_USER_EDUCATION , bulkUpdateUserEducation);

}