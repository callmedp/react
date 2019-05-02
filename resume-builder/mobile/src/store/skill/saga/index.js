import {Api} from './Api';

import {takeLatest, put, call,select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';
import * as LoaderAction from '../../loader/actions/actionTypes';

import {SubmissionError} from 'redux-form'

const getLoaderStatus = state => state.loader;

function* fetchUserSkill(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        const loader = yield select(getLoaderStatus)
        if(!loader.mainloader){
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: true}})
        }

        if (localStorage.getItem('skill')) {
            yield put({
                type: Actions.SAVE_USER_SKILL,
                data: {list: JSON.parse(localStorage.getItem('skill')) 
                || [
                    {
                        "candidate_id": '',
                        "id": '',
                        "name": '',
                        "proficiency": '',
                        "order": 0
                    }
                ]}
            });
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: false}})
            return;
        }

        const result = yield call(Api.fetchUserSkill, candidateId);
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
        yield put({type: Actions.SAVE_USER_SKILL, data: data})
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: false}})
    } catch (e) {
        ////console.log(e);
    }
}


function* updateUserSkill(action) {
    try {
        let {payload: {userSkill, resolve, reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';

        const {id} = userSkill;

        const result = yield call(id ? Api.updateUserSkill : Api.createUserSkill, userSkill, candidateId, id);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        localStorage.removeItem('skill');

        yield put({type: Actions.SAVE_USER_SKILL, data: result['data']});

        return resolve('User Skill  Info saved successfully.');

    } catch (e) {
        ////console.log('error', e);
    }
}


function* bulkSaveUserSkill(action) {
    try {
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: true}})
        let {payload: {list}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';


        const result = yield call(Api.bulkSaveUserSkill, list, candidateId);

        if (result['error']) {
            ////console.log(result['error']);
        }
        else{
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: false}})
        }

        ////console.log('---', result);

    } catch (e) {
        ////console.log('error', e);
    }
}


function* deleteUserSkill(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: true}})

        const {skillId} = action;

        const result = yield call(Api.deleteUserSkill, candidateId, skillId);


        if (result['error']) {
            ////console.log(result['error'])
        }
        localStorage.deleteItem('skill');
        // yield call(fetchUserSkill)
        yield put({type: Actions.REMOVE_SKILL, id: skillId});
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{dataloader: false}})
        yield call(fetchUserSkill)

    } catch (e) {
        ////console.log('error', e);
    }
}


export default function* watchSkill() {
    yield takeLatest(Actions.FETCH_USER_SKILL, fetchUserSkill);
    yield takeLatest(Actions.UPDATE_USER_SKILL, updateUserSkill);
    yield takeLatest(Actions.DELETE_USER_SKILL, deleteUserSkill);
    yield takeLatest(Actions.BULK_SAVE_USER_SKILL, bulkSaveUserSkill);
}