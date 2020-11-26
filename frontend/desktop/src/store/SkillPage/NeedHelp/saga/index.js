import * as Actions from '../actions/actionTypes';
import { takeLatest, call } from 'redux-saga/effects';
import Swal from "sweetalert2";
import Api from './Api';

function* createLead(action) {
    try {
        const { payload } = action;
        const result = yield call(Api.createLead, payload);
        if (result["error"]) {
            Swal.fire({
                icon: 'error',
                html: result.errorMessage
            })
            return
        }
        Swal.fire({
            icon: "success", 
            html: "<h3>Form submitted successfully<h3>"
        });

    } catch (e) {
        Swal.fire({
            icon: "error", 
            html: "<h3>Something went wrong</h3>"
        });
        }
}




export default function* WatchLeadForm() {
    yield takeLatest(Actions.SEND_LEAD_DATA, createLead);
}