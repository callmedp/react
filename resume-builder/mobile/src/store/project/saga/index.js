import {Api} from './Api';

import {takeLatest, put, call,select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';
import * as LoaderAction from '../../loader/actions/actionTypes';

import {SubmissionError} from 'redux-form'

const getLoaderStatus = state => state.loader;

function* fetchUserProject(action) {
    try {
        const candidateId = localStorage.getItem('candidateId') || '';
        const loader = yield select(getLoaderStatus)
        if(!loader.mainloader){
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})
        }
        

        if (localStorage.getItem('project')) {
            let local_data = JSON.parse(localStorage.getItem('project')).length ? 
                            JSON.parse(localStorage.getItem('project')) :
                            [
                                {
                                    "candidate_id": '',
                                    "id": '',
                                    "project_name": '',
                                    "start_date": '',
                                    "end_date": '',
                                    "skills": [],
                                    "description": '',
                                    "order": 0
                                }
                            ]

            yield put({type: Actions.SAVE_USER_PROJECT, data: {list:local_data}})
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
            return;
        }

        const result = yield call(Api.fetchUserProject, candidateId);
        if (result['error']) {
            console.log('error');
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
                                "project_name": '',
                                "start_date": '',
                                "end_date": '',
                                "skills": [],
                                "description": '',
                                "order": 0
                            }
                        ]
                }
            };
        }

        yield put({type: Actions.SAVE_USER_PROJECT, data: data})
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
    } catch (e) {
        console.log(e);
    }
}


 function* updateUserProject(action) {
    try {
        let {payload: {userProject, resolve, reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';

        const {id} = userProject;

        const result = yield call(id ? Api.updateUserProject : Api.createUserProject, userProject, candidateId, id);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }

        yield put({type: Actions.SAVE_USER_PROJECT, data: result['data']});

        return resolve('User Project have saved successfully.');

    } catch (e) {
        console.log('error', e);
    }
}


function* bulkUpdateUserProject(action) {
    try {
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})
        let {payload: {list,resolve,reject}} = action;


        const candidateId = localStorage.getItem('candidateId') || '';


        const result = yield call(Api.bulkUpdateUserProject, list, candidateId);

        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        else{
            if (localStorage.getItem('project')){
                localStorage.removeItem('project')
                yield call(fetchUserProject)
            }
            yield put({type: Actions.SAVE_USER_PROJECT, data: {list: result['data']}})
            yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
            return resolve('Bulk Update Done.');
        }

    } catch (e) {
        console.log('error', e);
    }
}


function* deleteUserProject(action) {
    try {

        const candidateId = localStorage.getItem('candidateId') || '';
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: true}})

        const {projectId} = action;

        const result = yield call(Api.deleteUserProject, candidateId, projectId);


        if (result['error']) {
            console.log(result['error'])
        }
        yield put({type: Actions.REMOVE_PROJECT, id: projectId});
        yield put({type:LoaderAction.UPDATE_DATA_LOADER,payload:{mainloader: false}})
        
        yield call(fetchUserProject)

    } catch (e) {
        console.log('error', e);
    }
}


export default function* watchProject() {
    yield takeLatest(Actions.FETCH_USER_PROJECT, fetchUserProject);
    yield takeLatest(Actions.UPDATE_USER_PROJECT, updateUserProject);
    yield takeLatest(Actions.DELETE_USER_PROJECT, deleteUserProject);
    yield takeLatest(Actions.BULK_UPDATE_USER_PROJECT, bulkUpdateUserProject);

}