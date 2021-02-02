import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';
import { mostViewedCoursesFetched,
    inDemandProductsFetched,
    jobAssistanceAndBlogsFetched, 
    fetchMostViewedCourses,
    fetchInDemandProducts, 
    fetchJobAssistanceAndBlogs, 
    skillwithDemandsFetched,
    fetchSkillwithDemands} from './actions';




function* mostViewedCourse(action){
    const { payload } = action;
    try{
        const response = yield call(Api.mostViewedCourse);
        
        if(response?.error){
            return payload?.reject(response?.error);
        }
        const item = response?.data?.data;
        yield put(mostViewedCoursesFetched({ item }))
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
        const response = yield call(Api.inDemandProducts, payload);
        
        if(response?.error){
            return payload?.reject(response);
        }
        const item = response?.data?.data;
        yield put(inDemandProductsFetched({ courses : item.courses, certifications: item.certifications, 
            id: payload?.pageId, pages:item.pages, device: payload?.device }))
        return payload?.resolve(item);
    }
    catch(e){
        console.error("Exception occured in inDemandProducts Api", e)
        return payload?.reject(e);
    }
}



function* jobAssistanceAndBlogs(action){
    const { payload } = action;
    try{
        const response = yield call(Api.jobAssistanceAndBlogs);
        
        if(response?.error){
            return payload?.reject(response?.error);
        }
        const item = response?.data?.data;
        yield put(jobAssistanceAndBlogsFetched({ item }))
        return payload?.resolve(item);
    }
    catch(e){
        console.error("Exception occured in jobAssistanceServices Api", e)
        return payload?.reject(e);
    }
}


function* skillwithDemands(action) {
    const { payload } = action;
    try {
        const response = yield call(Api.skillwithDemands);

        if (response?.error){
            return payload?.reject(response?.error);
        }
        const item = response?.data?.data;
        yield put(skillwithDemandsFetched({ item }))
        return payload?.resolve(item);
    }
    catch(e) {
        console.log("Exception occured in skillWithDemads Api", e)
        return payload?.reject(e);
    }
}

export default function* WatchHomePage() {
    yield takeLatest(fetchMostViewedCourses.type, mostViewedCourse);
    yield takeLatest(fetchInDemandProducts.type, inDemandProducts);
    yield takeLatest(fetchJobAssistanceAndBlogs.type, jobAssistanceAndBlogs);
    yield takeLatest(fetchSkillwithDemands.type, skillwithDemands);
}
