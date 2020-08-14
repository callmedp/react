import {Api} from './Api';
import {apiError} from '../../../Utils/apiError';

import {takeLatest, put, call,select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';
import * as uiAction from '../../ui/actions/actionTypes';

import {SubmissionError} from 'redux-form'

const getUIStatus = state => state.ui;

function* fetchUserCourse(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        const ui = yield select(getUIStatus)
        if(!ui.mainloader){
            yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})
        }

        if (localStorage.getItem('course')) {
            let local_data =JSON.parse(localStorage.getItem('course')) && JSON.parse(localStorage.getItem('course')).length ? 
                            JSON.parse(localStorage.getItem('course')) :
                            [
                                {
                                    "candidate_id": '',
                                    "id": '',
                                    "name_of_certification": '',
                                    "year_of_certification": '',
                                    "order": 0
                                }
                            ]

            yield put({type: Actions.SAVE_USER_COURSE, data: {list:local_data}})
          
            yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
            return;
        }

        const result = yield call(Api.fetchUserCourse, candidateId);
        if (result['error']) {
            apiError();
        }
        const {data: {results}} = result;
        results.sort((a,b) => (a.order > b.order) ? 1 : ((b.order > a.order) ? -1 : 0));
        let data = {list: results}
        if(! data.list.length){
            data = {
                ...data,
                ...{
                    list: [
                        {
                            "candidate_id": '',
                            "id": '',
                            "name_of_certification": '',
                            "year_of_certification": '',
                            "order": 0
                        }
                    ]
                }
            };
        }
        yield put({type: Actions.SAVE_USER_COURSE, data: data})
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
    } catch (e) {
        apiError();
    }
}


function* updateUserCourse(action) {
    try {
        const {payload: {userCourse, resolve, reject}} = action;

        const candidateId = localStorage.getItem('candidateId') || '';

        const {id} = userCourse;

        const result = yield call(id ? Api.updateUserCourse : Api.createUserCourse, userCourse, candidateId, id);
        if (result['error']) {
            apiError();
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        

        yield put({type: Actions.SAVE_USER_COURSE, data: result['data']});

        return resolve('User Course  Info saved successfully.');

    } catch (e) {
        apiError();
    }
}


function* bulkUpdateUserCourse(action) {
    try {
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})
        let {payload: {list,resolve,reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';


        const result = yield call(Api.bulkUpdateUserCourse, list, candidateId);

        if (result['error']) {
            apiError();
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        else{
            if (localStorage.getItem('course')){
                localStorage.removeItem('course')
                yield call(fetchUserCourse)
            }
            yield put({type: Actions.SAVE_USER_COURSE, data:{list: result['data']}});
            yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
            return resolve('Bulk Update Done.');
        }

    } catch (e) {
        apiError();
    }
}


function* deleteUserCourse(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})

        const {courseId} = action;

        const result = yield call(Api.deleteUserCourse, candidateId, courseId);


        if (result['error']) {
            apiError();
        }
        // yield call(fetchUserLanguage)
        yield put({type: Actions.REMOVE_COURSE, id: courseId});
        yield put({type:uiAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
        yield call(fetchUserCourse)

    } catch (e) {
        apiError();
    }
}


export default function* watchCourse() {
    yield takeLatest(Actions.FETCH_USER_COURSE, fetchUserCourse);
    yield takeLatest(Actions.UPDATE_USER_COURSE, updateUserCourse);
    yield takeLatest(Actions.DELETE_USER_COURSE, deleteUserCourse);
    yield takeLatest(Actions.BULK_UPDATE_USER_COURSE, bulkUpdateUserCourse);
}