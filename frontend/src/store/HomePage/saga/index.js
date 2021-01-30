import * as Actions from '../actions/actionTypes';
import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';

function* latestBlog(action){
    const { payload } = action;
    try{
        const response = yield call(Api.latestBlog);
        
        if(response?.error){
            return payload?.reject(response?.error);
        }
        const item = response?.data?.data;
        yield put({ 
            type : Actions.LATEST_BLOG_FETCHED,
            item : item
        })
        return payload?.resolve(item);
    }
    catch(e){
        console.error("Exception occured in latestBlog Api", e)
        return payload?.reject(e);
    }
}


function* mostViewedCourse(action){
    const { payload } = action;
    try{
        const response = yield call(Api.mostViewedCourse);
        
        if(response?.error){
            return payload?.reject(response?.error);
        }
        const item = response?.data?.data;
        yield put({ 
            type : Actions.MOST_VIEWED_PRODUCTS_FETCHED,
            item : item
        })
        return payload?.resolve(item);
    }
    catch(e){
        console.error("Exception occured in mostViewedCourse Api", e)
        return payload?.reject(e);
    }
}


function* inDemandProducts(action){
    const { payload } = action;
    try{
        const response = yield call(Api.inDemandProducts);
        
        if(response?.error){
            return payload?.reject(response?.error);
        }
        const item = response?.data?.data;
        yield put({ 
            type : Actions.IN_DEMAND_PRODUCTS_FETCHED,
            item : item
        })
        return payload?.resolve(item);
    }
    catch(e){
        console.error("Exception occured in inDemandProducts Api", e)
        return payload?.reject(e);
    }
}


function* jobAssistanceServices(action){
    const { payload } = action;
    try{
        const response = yield call(Api.jobAssistanceServices);
        
        if(response?.error){
            return payload?.reject(response?.error);
        }
        const item = response?.data?.data;
        yield put({ 
            type : Actions.JOB_ASSISTANCE_SERVICES_FETCHED,
            item : item
        })
        return payload?.resolve(item);
    }
    catch(e){
        console.error("Exception occured in jobAssistanceServices Api", e)
        return payload?.reject(e);
    }
}

export default function* WatchHomePage() {
    yield takeLatest(Actions.FETCH_LATEST_BLOG, latestBlog);
    yield takeLatest(Actions.FETCH_MOST_VIEWED_PRODUCTS, mostViewedCourse);
    yield takeLatest(Actions.FETCH_IN_DEMAND_PRODUCTS, inDemandProducts);
    yield takeLatest(Actions.FETCH_JOB_ASSISTANCE_SERVICES, jobAssistanceServices);
}
