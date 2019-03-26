import {Api} from './Api';
import {takeLatest, put, call, select} from "redux-saga/effects";

import * as Actions from '../actions/actionTypes';


function* getShineProfile() {
    yield call()
}


export default function* watchLandingPage() {
    yield takeLatest(Actions.FETCH_SHINE_PROFILE, getShineProfile)
}