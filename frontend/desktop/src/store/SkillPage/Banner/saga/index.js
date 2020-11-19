import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';



function* skillPageBanner(action) {
    try {
        const { payload } = action;
        console.log("payload is ", payload)
        const response = yield call(Api.skillPageBanner, payload);
        if (response["error"]) {
            return
        }
        const item = response.data;
        
        //converts 1D array to 2D array
        const storiesList = item?.testimonialCategory.reduce((rows, key, index) => 
            (index % 3 == 0 ? rows.push([key]) : rows[rows.length-1].push(key)) && rows, []);
        console.log("storiesList", storiesList)
        
        if(storiesList.length){
            item.testimonialCategory = storiesList.slice()
        }
        
        console.log("breadLitem",item)
        yield put({ 
            type : Actions.SKILL_PAGE_BANNER_FETCHED, 
            item 
        })

    } catch (e) {
        console.error("Exception occured ",e)
    }
}




export default function* WatchSkillPageBanner() {
    yield takeLatest(Actions.FETCH_SKILL_PAGE_BANNER, skillPageBanner);
}