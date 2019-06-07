import {Api} from './Api';

import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';

import {SubmissionError} from 'redux-form'
import {proficiencyList} from "../../../Utils/proficiencyList";
import {UPDATE_UI} from "../../ui/actions/actionTypes";
import {courseTypeList} from "../../../Utils/courseTypeList";
import {initialState} from '../reducer';


function modifySkill(data) {
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
    return data.list.length ? data : initialState;
}

function* fetchUserSkill(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';

        if (localStorage.getItem('skill')) {
            yield put({
                type: Actions.SAVE_USER_SKILL,
                data: modifySkill({list: JSON.parse(localStorage.getItem('skill')) || []})
            });
            return;
        }

        yield put({type: UPDATE_UI, data: {loader: true}});

        const result = yield call(Api.fetchUserSkill, candidateId);

        if (result['error']) {
            console.log('error');
        }

        yield put({type: UPDATE_UI, data: {loader: false}})

        let {data: {results}} = result;

        if (!results.length) {
            const state = yield select();
            let {skill: {list}} = state;
            results = list
        }
        let data = {list: results};
        data = modifySkill(data);
        yield put({type: Actions.SAVE_USER_SKILL, data: data})
    } catch (e) {
        console.log(e);
    }
}


function* updateUserSkill(action) {
    try {
        let {payload: {userSkill, resolve, reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';

        const {id} = userSkill;


        yield put({type: UPDATE_UI, data: {loader: true}})

        const result = yield call(id ? Api.updateUserSkill : Api.createUserSkill, userSkill, candidateId, id);
        yield put({type: UPDATE_UI, data: {loader: false}});

        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        localStorage.removeItem('skill');

        yield put({type: Actions.SAVE_USER_SKILL, data: result['data']});

        return resolve('User Skill  Info saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}

function* handleSkillSwap(action) {
    try {
        let {payload: {list, resolve, reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';

        yield put({type: UPDATE_UI, data: {loader: true}});

        const result = yield call(Api.bulkUpdateUserSkill, list, candidateId);

        yield put({type: UPDATE_UI, data: {loader: false}});

        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }


        localStorage.removeItem('skill');

        let {data} = result;

        data.sort((a, b) => a.order <= b.order);

        data = {list: data};

        data = modifySkill(data);


        yield put({type: Actions.SAVE_USER_SKILL, data: data});

        return resolve('User Skill  Info saved successfully.');


    } catch (e) {
        console.log('error', e);
    }
}


function* deleteUserSkill(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';

        const {skillId} = action;

        const result = yield call(Api.deleteUserSkill, candidateId, skillId);


        if (result['error']) {
            console.log(result['error'])
        }


        localStorage.removeItem('skill');

        // yield call(fetchUserSkill)
        yield put({type: Actions.REMOVE_SKILL, id: skillId});


    } catch (e) {
        console.log('error', e);
    }
}


export default function* watchSkill() {
    yield takeLatest(Actions.FETCH_USER_SKILL, fetchUserSkill);
    yield takeLatest(Actions.UPDATE_USER_SKILL, updateUserSkill);
    yield takeLatest(Actions.DELETE_USER_SKILL, deleteUserSkill);
    yield takeLatest(Actions.HANDLE_SKILL_SWAP, handleSkillSwap);
    yield takeLatest(Actions.BULK_U_C_USER_SKILL, handleSkillSwap);

}