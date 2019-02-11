import {Api} from './Api';
import {takeLatest, put, call, select} from "redux-saga/effects";
import * as Actions from '../actions/actionTypes';
import {SubmissionError} from 'redux-form'
import {UPDATE_USER_DETAILS} from "../actions/actionTypes";
import {FETCH_SKILL_LIST} from "../actions/actionTypes";


function* saveUserInfo(action) {
    try {
        const {payload: {userDetails, resolve, reject}} = action;
        const result = yield call(Api.saveUserData, userDetails);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        yield put({type: Actions.STORE_USER_INFO, data: result['data']});
        return resolve('User Info saved successfully.');
    } catch (e) {
        console.log('error', e);
    }
}

function* saveUserExperience(action) {
    try {
        let {payload: {userExperiences, resolve, reject}} = action;
        const {userInfoReducer: {id}} = yield select();
        userExperiences = {
            ...userExperiences,
            user: id
        };

        const result = yield call(Api.saveUserExperience, userExperiences);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        yield put({type: Actions.STORE_USER_INFO, data: {'experiences': result['data']}});
        return resolve('User experience saved successfully.');
    } catch (e) {
        console.log('error', e);
    }
}

function* updateUserInfo(action) {
    try {
        const {userInfoReducer: {id}} = yield select();
        let {payload: {userDetails, resolve, reject}} = action;
        userDetails = {
            ...userDetails,
            id: id
        }
        const result = yield call(Api.updateUserData, userDetails, id);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        yield put({type: Actions.STORE_USER_INFO, data: result['data']});
        return resolve('User Info updated successfully.');
    } catch (e) {
        console.log('error', e);
    }
}


function* saveUserEducation(action) {
    try {
        const {userInfoReducer: {id}} = yield select();
        let {payload: {userEducation, resolve, reject}} = action;
        userEducation = {
            ...userEducation,
            user: id
        }
        const result = yield call(Api.saveUserEducation, userEducation, id);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        yield put({type: Actions.STORE_USER_INFO, data: {'education': result['data']}});
        return resolve('User Education added successfully.');
    } catch (e) {
        console.log('error', e);
    }
}

function* saveUserCertification(action) {
    try {
        const {userInfoReducer: {id}} = yield select();
        let {payload: {userCertification, resolve, reject}} = action;
        userCertification = {
            ...userCertification,
            user: id
        };
        const result = yield call(Api.saveUserCertification, userCertification, id);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        yield put({type: Actions.STORE_USER_INFO, data: {'certifications': result['data']}});
        return resolve('User Certification added successfully.');
    } catch (e) {
        console.log('error', e);
    }
}

function* saveUserReference(action) {
    try {
        const {userInfoReducer: {id}} = yield select();
        let {payload: {userReference, resolve, reject}} = action;
        userReference = {
            ...userReference,
            user: id
        };
        const result = yield call(Api.saveUserReference, userReference, id);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        yield put({type: Actions.STORE_USER_INFO, data: {'references': result['data']}});
        return resolve('User Reference added successfully.');
    } catch (e) {
        console.log('error', e);
    }
}


function* saveUserProject(action) {
    try {
        const {userInfoReducer: {id, projects}} = yield select();
        let {payload: {userProject, resolve, reject}} = action;

        const {skills} = userProject
        const updatedSkills = (skills || []).map(skill => skill['value'])
        userProject = {
            ...userProject,
            user: id,
            skills: updatedSkills
        };
        let projectList = projects || [];
        projectList.push(userProject);
        yield put({type: Actions.ADD_PROJECT, data: {'projects': projectList}});

        const result = yield call(Api.saveUserProject, projectList, id);
        console.log('result after --', result);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        yield put({type: Actions.STORE_USER_INFO, data: {'projects': result['data']}});
        return resolve('User projects added successfully.');
    } catch (e) {
        console.log('error', e);
    }
}


function* saveUserAchievement(action) {
    try {
        const {userInfoReducer: {id}} = yield select();
        let {payload: {userAchievement, resolve, reject}} = action;
        userAchievement = {
            ...userAchievement,
            user: id
        };
        const result = yield call(Api.saveUserAchievement, userAchievement, id);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        yield put({type: Actions.STORE_USER_INFO, data: {'achievements': result['data']}});
        return resolve('User achievements added successfully.');
    } catch (e) {
        console.log('error', e);
    }
}


function* fetchSkillList(action) {
    try {
        let {payload: {inputValue, resolve, reject}} = action;
        const result = yield call(Api.fetchSkills, inputValue);

        console.log('result ===', result, result['error']);
        if (result['error']) {
            return reject(new Error(result['errorMessage']));
        }
        // yield put({type: Actions.SAVE_SKILL_LIST, data: {'achievements': result['data']}});
        return resolve(result['data']);
    } catch (e) {
        console.log('error', e);
    }
}

function* fetchDefaultSkillList(action) {
    try {
        let {inputValue} = action;
        const result = yield call(Api.fetchSkills, inputValue);
        console.log('result ===', result, result['error']);
        const list = (result && result.data && result.data.results || []).map(skill => ({
            value: skill.id,
            label: skill.name
        }));
        yield put({type: Actions.SAVE_DEFAULT_SKILL_LIST, data: {'defaultList': list}});
    } catch (e) {
        console.log('error', e);
    }
}


export default function* watchFetchHomeData() {
    yield takeLatest(Actions.SAVE_USER_DETAILS, saveUserInfo);
    yield takeLatest(Actions.UPDATE_USER_DETAILS, updateUserInfo);
    yield takeLatest(Actions.SAVE_USER_EXPERIENCES, saveUserExperience);
    yield takeLatest(Actions.SAVE_USER_EDUCATION, saveUserEducation);
    yield takeLatest(Actions.SAVE_USER_PROJECT, saveUserProject);
    yield takeLatest(Actions.SAVE_USER_ACHIEVEMENT, saveUserAchievement);
    yield takeLatest(Actions.SAVE_USER_CERTIFICATION, saveUserCertification);
    yield takeLatest(Actions.SAVE_USER_REFERENCE, saveUserReference);
    yield takeLatest(Actions.FETCH_SKILL_LIST, fetchSkillList);
    yield takeLatest(Actions.FETCH_DEFAULT_SKILL_LIST, fetchDefaultSkillList);

}