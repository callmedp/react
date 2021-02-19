import { takeLatest, call, put } from 'redux-saga/effects';
import Api from './Api';
import { mostViewedCoursesFetched,
    inDemandProductsFetched,
    jobAssistanceAndBlogsFetched, 
    fetchMostViewedCourses,
    fetchInDemandProducts, 
    fetchJobAssistanceAndBlogs,
    fetchTestimonials, 
    testimonialsFetched,
    skillwithDemandsFetched,
    fetchSkillwithDemands } from './actions';




function* mostViewedCourse(action){
    const { payload } = action;
    try{
        const response = yield call(Api.mostViewedCourse, payload);
        
        if(response?.error){
            return payload?.reject(response);
        }
        const item = response?.data?.data;
        yield put(mostViewedCoursesFetched({ [payload.categoryId]: item.mostViewedCourses }))
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
            id: payload?.pageId, pages:item.page?.total, device: payload?.device }))
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
            return payload?.reject(response);
        }
        const item = response?.data?.data;
        yield put(jobAssistanceAndBlogsFetched({ ...item }))
        return payload?.resolve(item);
    }
    catch(e){
        console.error("Exception occured in jobAssistanceServices Api", e)
        return payload?.reject(e);
    }
}

function* fetchTestimonialsData(action){
    const { payload } = action;
    try{
        const response = yield call(Api.testimonialsApi);
        
        if(response?.error){
            return payload?.reject(response);
        }
        const item = response?.data?.data;

        if(!!payload && payload.device === 'desktop' && !!item && item.testimonialCategory instanceof Array){
            const storiesList = item.testimonialCategory.reduce((rows, key, index) => 
                (index % 2 == 0 ? rows.push([key]) : rows[rows.length-1].push(key)) && rows, []);
            
            if(storiesList.length){
                item.testimonialCategory = storiesList.slice()
            }
        }

        yield put(testimonialsFetched({ ...item }))
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
        const response = yield call(Api.skillwithDemands, payload?.numCourses);

        if (response?.error){
            return payload?.reject(response);
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
    yield takeLatest(fetchTestimonials.type, fetchTestimonialsData);
    yield takeLatest(fetchSkillwithDemands.type, skillwithDemands);
}
