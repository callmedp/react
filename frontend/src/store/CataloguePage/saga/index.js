import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';


function* trendingCategories(action) {
    const { payload: { payload, resolve, reject } } = action;

    try {

        const response = yield call(Api.trendingCategories, payload);

        if (!response || response?.error) {
            return reject(response?.error);
        }
        const item = response?.data;

        var SnMCourseList = item?.SnMCourseList
        var ITCourseList = item?.ITCourseList
        var BnFCourseList = item?.BnFCourseList
       

        if(!!payload && !payload.medium && SnMCourseList instanceof Array 
            && ITCourseList instanceof Array && BnFCourseList instanceof Array){
            //converts 1D array to 2D array
            SnMCourseList = !!item && item.SnMCourseList?.length ? item.SnMCourseList.reduce((rows, key, index) => 
            (index % 3 == 0 ? rows.push([key]) : rows[rows.length-1].push(key)) && rows, []) : [];
        
            //converts 1D array to 2D array
            ITCourseList = !!item && item.ITCourseList?.length ? item?.ITCourseList.reduce((rows, key, index) => 
            (index % 3 == 0 ? rows.push([key]) : rows[rows.length-1].push(key)) && rows, []) : [];

            //converts 1D array to 2D array
            BnFCourseList = !!item && item.BnFCourseList?.length ? item?.BnFCourseList.reduce((rows, key, index) => 
            (index % 3 == 0 ? rows.push([key]) : rows[rows.length-1].push(key)) && rows, []) : [];
        }
        
        
        yield put({ 
            type : Actions.TRENDING_CATEGORIES_FETCHED, 
            item : {
                SnMCourseList,
                ITCourseList,
                BnFCourseList
            }
        })

        return resolve(item)

    } catch (e) {
        return reject(e);
    }
}


function* recentlyAddedCourses(action) {
    const { payload: { payload, resolve, reject } } = action;
    try {
        const response = yield call(Api.recentlyAddedCourses, payload);

        if (!response || response?.error) {
            return reject(response?.error);
        }
        const item = response?.data?.data;
        yield put({ 
            type : Actions.RECENTLY_ADDED_COURSES_FETCHED,
            item : item
        })
        return resolve(item);
    }
    catch (e) {
        return reject(e);
    }
}

function* popularServices(action) {
    const { payload: { payload, resolve, reject } } = action;
    try {
        const response = yield call(Api.popularServices, payload);

        if (!response || response?.error) {
            return reject(response?.error);
        }
        const item = response?.data?.data;
        yield put({ 
            type : Actions.POPULAR_SERVICES_FETCHED,
            item : item
        })
        return resolve(item);
    }
    catch (e) {
        return reject(e);
    }
}

function* allCategories(action) {
    const { payload: { payload, resolve, reject } } = action;
    try {
        const response = yield call(Api.allCategories, payload);

        if (!response || response?.error) {
            return reject(response?.error);
        }
        const item = response?.data?.data;
        yield put({
            type: Actions.ALL_CATEGORIES_AND_VENDORS_FETCHED,
            item: item
        })
        return resolve(item);
    }
    catch (e) {
        return reject(e);
    }
}

export default function* WatchCataloguePage() {
    yield takeLatest(Actions.FETCH_RECENTLY_ADDED_COURSES, recentlyAddedCourses);
    yield takeLatest(Actions.FETCH_POPULAR_SERVICES, popularServices);
    yield takeLatest(Actions.FETCH_TRENDING_CATEGORIES, trendingCategories);
    yield takeLatest(Actions.FETCH_ALL_CATEGORIES_AND_VENDORS, allCategories);
}