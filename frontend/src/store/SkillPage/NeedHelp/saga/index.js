import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Swal from "sweetalert2";
import Api from './Api';
import { startSkillPageLoader, stopSkillPageLoader } from 'store/Loader/actions';

function* createLead(action) {
    const { payload: {data, resolve} } = action;
    try {
        yield put(startSkillPageLoader());
        const result = yield call(Api.createLead, data);
        yield put(stopSkillPageLoader())
        
        if (result["error"]) {
            Swal.fire({
                icon: 'error',
                html: result.message
            })
            return resolve(0)
        }
        Swal.fire({
            icon: "success", 
            html: "<h3>Form submitted successfully<h3>"
        });
        return resolve(1)

    } catch (e) {
        Swal.fire({
            icon: "error", 
            html: "<h3>Something went wrong</h3>"
        });
        }
        return resolve(0)
}




export default function* WatchLeadForm() {
    yield takeLatest(Actions.SEND_LEAD_DATA, createLead);
}