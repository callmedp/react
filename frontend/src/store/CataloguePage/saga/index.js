import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';


function* trendingCategories(action) {
    const { payload } = action;

    try {

        const response = yield call(Api.trendingCategories, payload);
        
        if(!response || response?.error){
            return payload?.reject(response?.error);
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

        return payload?.resolve(item)

    } catch (e) {
        console.error("Exception occured in trending categories api",e)
        return payload?.reject(e);
    }
}


function* recentlyAddedCourses(action){
    const { payload } = action;
    try{
        const response = yield call(Api.recentlyAddedCourses);
        
        if(!response || response?.error){
            return payload?.reject(response?.error);
        }
        const item = response?.data?.data;
        yield put({ 
            type : Actions.RECENTLY_ADDED_COURSES_FETCHED,
            item : item
        })
        return payload?.resolve(item);
    }
    catch(e){
        console.error("Exception occured in recentlyAddedCourses Api", e)
        return payload?.reject(e);
    }
}

function* popularServices(action){
    const { payload } = action;
    try{
        const response = yield call(Api.popularServices);
        
        if(!response || response?.error){
            return payload?.reject(response?.error);
        }
        const item = response?.data?.data;
        yield put({ 
            type : Actions.POPULAR_SERVICES_FETCHED,
            item : item
        })
        return payload?.resolve(item);
    }
    catch(e){
        console.error("Exception occured in popularServices Api", e)
        return payload?.reject(e);
    }
}

function* allCategories(action){
    const { payload } = action;
    try{
        const response = yield call(Api.allCategories, payload?.num);
        
        if(!response || response?.error){
            return payload?.reject(response?.error);
        }
        const item = response?.data?.data;
        yield put({ 
            type : Actions.ALL_CATEGORIES_AND_VENDORS_FETCHED,
            item : item
        })
        return payload?.resolve(item);
    }
    catch(e){
        console.error("Exception occured in allCategories Api", e)
        return payload?.reject(e);
    }
}

export default function* WatchCataloguePage() {
    yield takeLatest(Actions.FETCH_RECENTLY_ADDED_COURSES, recentlyAddedCourses);
    yield takeLatest(Actions.FETCH_POPULAR_SERVICES, popularServices);
    yield takeLatest(Actions.FETCH_TRENDING_CATEGORIES, trendingCategories);
    yield takeLatest(Actions.FETCH_ALL_CATEGORIES_AND_VENDORS, allCategories);
}