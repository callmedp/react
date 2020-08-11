import {Api} from './Api';
import {takeLatest, put, call, select} from "redux-saga/effects";
import * as Actions from '../actions/actionTypes';
import {SubmissionError} from 'redux-form'
import {courseTypeList} from "../../../Utils/courseTypeList";
import {UPDATE_UI} from '../../ui/actions/actionTypes'
import {initialState} from "../reducer/index"
import  {Toast} from "../../../services/ErrorToast";

function modifyEducation(data) {
    data = {
        ...data,
        ...{
            list: data['list'].map(el => {
                return {
                    ...el,
                    course_type: courseTypeList[el['course_type']] || ''
                }
            })
        }
    };
    return data.list.length ? data : initialState
}

function* fetchUserEducation(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';


        if (localStorage.getItem('education')) {

            yield put({
                type: Actions.SAVE_USER_EDUCATION,
                data: modifyEducation({list: JSON.parse(localStorage.getItem('education')) || []})
            });
            return;
        }
        yield put({type: UPDATE_UI, data: {loader: true}});

        const result = yield call(Api.fetchUserEducation, candidateId);
        if (result['error']) {
            Toast.fire({
                type: 'error',
                title: result['errorMessage']
            });
        }

        yield put({type: UPDATE_UI, data: {loader: false}})

        let {data: {results}} = result;
        if (!results.length) {
            const state = yield select();
            let {education: {list}} = state;
            results = list
        }
        let data = {list: results};

        data = modifyEducation(data);

        yield put({type: Actions.SAVE_USER_EDUCATION, data: data})
    } catch (e) {
        console.log(e);
    }
}

function* updateUserEducation(action) {
    try {
        const {payload: {userEducation, resolve, reject}} = action;

        const candidateId = localStorage.getItem('candidateId') || '';

        const {id} = userEducation;

        yield put({type: UPDATE_UI, data: {loader: true}})

        const result = yield call(id ? Api.updateUserEducation : Api.createUserEducation, userEducation, candidateId, id);

        yield put({type: UPDATE_UI, data: {loader: false}})

        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        localStorage.removeItem('education');


        return resolve('User Education  Info saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}


function* handleEducationSwap(action) {
    try {
        let {payload: {list, resolve, reject}} = action;

        const candidateId = localStorage.getItem('candidateId') || '';

        yield put({type: UPDATE_UI, data: {loader: true}});

        const result = yield call(Api.bulkUpdateUserEducation, list, candidateId);

        yield put({type: UPDATE_UI, data: {loader: false}});

        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        localStorage.removeItem('education');

        let {data} = result;

        data.sort((a, b) => a.order <= b.order);

        data = {list: data};

        data = modifyEducation(data);

        yield put({type: Actions.SAVE_USER_EDUCATION, data: data})

        return resolve('User Education  Info saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}


function* deleteUserEducation(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';

        const {educationId} = action;

        const result = yield call(Api.deleteUserEducation, candidateId, educationId);


        if (result['error']) {
            Toast.fire({
                type: 'error',
                title: result['errorMessage']
            });
        }
        localStorage.removeItem('education');

        // yield call(fetchUserLanguage)
        yield put({type: Actions.REMOVE_EDUCATION, id: educationId});

    } catch (e) {
        console.log('error', e);
    }
}


export default function* watchEducation() {
    yield takeLatest(Actions.FETCH_USER_EDUCATION, fetchUserEducation);
    yield takeLatest(Actions.UPDATE_USER_EDUCATION, updateUserEducation);
    yield takeLatest(Actions.DELETE_USER_EDUCATION, deleteUserEducation);
    yield takeLatest(Actions.HANDLE_EDUCATION_SWAP, handleEducationSwap);
    yield takeLatest(Actions.BULK_U_C_USER_EDUCATION, handleEducationSwap);

}