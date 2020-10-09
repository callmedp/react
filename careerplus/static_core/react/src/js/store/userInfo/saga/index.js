import {Api} from './Api';
import {takeLatest, put, call, select} from "redux-saga/effects";
import * as Actions from '../actions/actionTypes';
import {SubmissionError} from 'redux-form'

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
        const {userInfoReducer: {id, experiences}} = yield select();
        let {payload: {userExperiences, resolve, reject}} = action;
        userExperiences = {
            ...userExperiences,
            user: id
        };

        let experienceList = experiences || [];
        experienceList.push(userExperiences);
        yield put({type: Actions.ADD_EXPERIENCE, data: {'experiences': experienceList}});

        const result = yield call(Api.saveUserExperience, experienceList);
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
        var data = new FormData();
        userDetails = {
            ...userDetails,
            "gender": userDetails['gender'].value,
            id: id
        };

        for (const key in userDetails) {
            data.append(key, userDetails[key]);
        }
        const result = yield call(Api.updateUserData, data, id);
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
        const {userInfoReducer: {id, educations}} = yield select();
        let {payload: {userEducation, resolve, reject}} = action;
        userEducation = {
            ...userEducation,
            "course_type": userEducation['course_type'].value,
            user: id
        };

        let educationList = educations || [];
        educationList.push(userEducation);
        yield put({type: Actions.ADD_EDUCATION, data: {'educations': educationList}});

        const result = yield call(Api.saveUserEducation, educationList);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        yield put({type: Actions.STORE_USER_INFO, data: {'educations': result['data']}});
        return resolve('User Education added successfully.');
    } catch (e) {
        console.log('error', e);
    }
}

function* saveUserCertification(action) {
    try {
        const {userInfoReducer: {id, certifications}} = yield select();
        let {payload: {userCertification, resolve, reject}} = action;
        userCertification = {
            ...userCertification,
            user: id
        };

        let certificationList = certifications || [];
        certificationList.push(userCertification);
        yield put({type: Actions.ADD_CERTIFICATION, data: {'certifications': certificationList}});


        const result = yield call(Api.saveUserCertification, certificationList);
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
        const {userInfoReducer: {id, references}} = yield select();
        let {payload: {userReference, resolve, reject}} = action;
        userReference = {
            ...userReference,
            user: id
        };

        let referenceList = references || [];
        referenceList.push(userReference);
        yield put({type: Actions.ADD_REFERENCE, data: {'references': referenceList}});

        const result = yield call(Api.saveUserReference, referenceList);
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

        const {skills} = userProject;
        const updatedSkills = (skills || []).map(skill => skill['value']);
        userProject = {
            ...userProject,
            user: id,
            skills: updatedSkills
        };
        let projectList = projects || [];
        projectList.push(userProject);
        yield put({type: Actions.ADD_PROJECT, data: {'projects': projectList}});

        const result = yield call(Api.saveUserProject, projectList);
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
        const {userInfoReducer: {id, achievements}} = yield select();
        let {payload: {userAchievement, resolve, reject}} = action;
        userAchievement = {
            ...userAchievement,
            user: id
        };

        let achievementList = achievements || [];
        achievementList.push(userAchievement);
        yield put({type: Actions.ADD_ACHIEVEMENT, data: {'achievements': achievementList}});

        const result = yield call(Api.saveUserAchievement, achievementList);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        yield put({type: Actions.STORE_USER_INFO, data: {'achievements': result['data']}});
        return resolve('User achievements added successfully.');
    } catch (e) {
        console.log('error', e);
    }
}


function* saveUserSkill(action) {
    try {
        const {userInfoReducer: {id, skills}} = yield select();
        let {payload: {userSkill, resolve, reject}} = action;
        userSkill = {
            ...userSkill,
            user: id
        };

        let skillList = skills || [];
        skillList.push(userSkill);
        yield put({type: Actions.ADD_SKILL, data: {'skills': skillList}});

        const result = yield call(Api.saveUserSkill, skillList);
        if (result['error']) {
            return reject(new SubmissionError({_error: result['errorMessage']}));
        }
        yield put({type: Actions.STORE_USER_INFO, data: {'skills': result['data']}});
        return resolve('User skills added successfully.');
    } catch (e) {
        console.log('error', e);
    }
}


function* fetchSkillList(action) {
    try {
        let {payload: {inputValue, resolve, reject}} = action;
        const result = yield call(Api.fetchSkills, inputValue);

        if (result['error']) {
            return reject(new Error(result['errorMessage']));
        }
        return resolve(result['data']);
    } catch (e) {
        console.log('error', e);
    }
}

function* fetchDefaultSkillList(action) {
    try {
        let {inputValue} = action;
        const result = yield call(Api.fetchSkills, inputValue);
        const list = (result && result.data && result.data.results || []).map(skill => ({
            value: skill.id,
            label: skill.name
        }));
        yield put({type: Actions.SAVE_DEFAULT_SKILL_LIST, data: {'defaultList': list}});
    } catch (e) {
        console.log('error', e);
    }
}

function* sendProductToCart(action) {
    try {
        let data = {
            'prod_id': 2831,
            'cart_type': 'cart',
            'cv_id': 2795,
            'add_resume': true
        };
        const result = yield call(Api.addToCart, data);

    } catch (e) {
        console.log('error', e);
    }
}

function* showResumePreview(action) {
    try {
        const {userInfoReducer: {id}} = yield select();
        let {payload: {resolve, reject}} = action;
        const result = yield call(Api.showResumePreview, id)
        return resolve(result['data']);
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
    yield takeLatest(Actions.SAVE_USER_SKILL, saveUserSkill);
    yield takeLatest(Actions.FETCH_SKILL_LIST, fetchSkillList);
    yield takeLatest(Actions.FETCH_DEFAULT_SKILL_LIST, fetchDefaultSkillList);
    yield takeLatest(Actions.ADD_TO_CART, sendProductToCart);
    yield takeLatest(Actions.SHOW_RESUME_PREVIEW, showResumePreview);


}