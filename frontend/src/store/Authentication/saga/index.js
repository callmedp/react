import * as Actions from '../actions/actionTypes';
import { takeLatest, call } from 'redux-saga/effects';
import Api from './Api';


function* fetchUserInfos(action) {
    const { payload: { payload, resolve, reject } } = action;
    yield call(chatbotScriptSaga);

    try {
        const response = yield call(Api.fetchUserInform, payload);
        if (!response || response?.error) {
            return reject(response?.error);
        }
        const item = response?.data;
        sessionStorage.setItem('code2', item.code2 || 'IN');
        sessionStorage.setItem('candidate_id', item.candidate_id);
        return resolve(item)

    } catch (e) {
        return reject(e);
    }
}

function* chatbotScriptSaga() {
    var hours = 24; // Reset when storage is more than 24hours
    var now = new Date().getTime();
    var setupTime = localStorage.getItem('setupTime');

    try {
        const result = yield call(Api.chatbotScriptApi);
        
        if (setupTime == null) {
            if(result['data']['script_link'] != "script not available") {
                localStorage.setItem('script_link', result['data']['script_link'])
                localStorage.setItem('setupTime', now);
            }
        }
        else {
            if(now-setupTime > hours*60*60*1000) {
                localStorage.clear();
                if(result['data']['script_link'] != "script not available") {
                    localStorage.setItem('script_link', result['data']['script_link'])
                    localStorage.setItem('setupTime', now);
                }
            }
        }
    }
    catch (e) {
        console.log(e);
    }
}

export default function* WatchFetchUserInfo() {
    yield takeLatest(Actions.FETCH_USER, fetchUserInfos);
    // yield takeLatest(Actions.FETCH_CHATBOT_SCRIPT, chatbotScriptSaga);
}