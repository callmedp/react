import {Api} from './Api';

import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';
import {proficiencyList} from "../../../Utils/proficiencyList";
import {SubmissionError} from 'redux-form'
import {UPDATE_UI} from "../../ui/actions/actionTypes";
import {courseTypeList} from "../../../Utils/courseTypeList";


function modifyLanguage(data) {
    data = {
        ...data,
        ...{
            list: data['list'].map(el => {
                return {
                    ...el,
                    proficiency: proficiencyList[el['proficiency'].toString()]
                }
            })
        }
    };
    return data;
}

function* fetchUserLanguage(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';


        if (localStorage.getItem('language')) {

            yield put({
                type: Actions.SAVE_USER_LANGUAGE,
                data: modifyLanguage({list: JSON.parse(localStorage.getItem('language')) || []})
            });
            return;
        }
        yield put({type: UPDATE_UI, data: {loader: true}})

        const result = yield call(Api.fetchUserLanguage, candidateId);
        if (result['error']) {
            console.log('error');
        }

        yield put({type: UPDATE_UI, data: {loader: false}})

        let {data: {results}} = result;

        if (!results.length) {
            const state = yield select();
            let {language: {list}} = state;
            results = list
        }

        let data = {list: results};

        data = modifyLanguage(data)
        yield put({type: Actions.SAVE_USER_LANGUAGE, data: data})
    } catch (e) {
        console.log(e);
    }
}


function* updateUserLanguage(action) {
    try {
        let {payload: {userLanguage, resolve, reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';

        const {id} = userLanguage;
        yield put({type: UPDATE_UI, data: {loader: true}})

        const result = yield call(id ? Api.updateUserLanguage : Api.createUserLanguage, userLanguage, candidateId, id);

        yield put({type: UPDATE_UI, data: {loader: false}})

        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        localStorage.removeItem('language');


        yield put({type: Actions.SAVE_USER_LANGUAGE, data: result['data']});

        // yield call(fetchUserLanguage)
        return resolve('User Language  Info saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}


function* handleLanguageSwap(action) {
    try {
        let {payload: {list}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';


        const result = yield call(Api.bulkUpdateUserLanguage, list, candidateId);

        if (result['error']) {
            console.log(result['error']);
        }

        console.log('-language swap result--', result);
        // yield call(fetchUserLanguage)

    } catch (e) {
        console.log('error', e);
    }
}


function* deleteUserLanguage(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';

        // userLanguage['cc_id'] = candidateId;
        const {languageId} = action;

        const result = yield call(Api.deleteUserLanguage, candidateId, languageId);


        if (result['error']) {
            console.log(result['error'])
        }
        // yield call(fetchUserLanguage)
        yield put({type: Actions.REMOVE_LANGUAGE, id: languageId});

    } catch (e) {
        console.log('error', e);
    }
}

export default function* watchLanguage() {
    yield takeLatest(Actions.FETCH_USER_LANGUAGE, fetchUserLanguage);
    yield takeLatest(Actions.UPDATE_USER_LANGUAGE, updateUserLanguage);
    yield takeLatest(Actions.DELETE_USER_LANGUAGE, deleteUserLanguage);
    yield takeLatest(Actions.HANDLE_LANGUAGE_SWAP, handleLanguageSwap);

}