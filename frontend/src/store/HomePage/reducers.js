import { mostViewedCoursesFetched,
    inDemandProductsFetched,
    jobAssistanceAndBlogsFetched,
    testimonialsFetched,
    skillwithDemandsFetched } from './actions';

const mostViewedCoursesState = {
    mostViewedCourses : []
}

export const MostViewedCoursesReducer = (state=mostViewedCoursesState, action) => {
    switch(action.type){
        case mostViewedCoursesFetched.type  : return {...mostViewedCoursesState, ...action.payload}
        default : return state;
    }
}

const inDemandProductsState = {
    courses : [],
    certifications : []
}

const appendProduct = ( state, {payload} ) => {
    if( payload.device === 'mobile' ){
        if(!!payload.courses){
            let courses = [...state.courses,...payload.courses];
            return { courses : courses };
        }
        else if(!!payload.certifications){
            let certifications = [...state.certifications, ...payload.certifications];
            return { certifications: certifications }
        }
        else{
            return { }
        }
    }
    else {
        if(!!payload.courses){

            let courses = [...state.courses];
            if(courses.length === 0)    courses = Array.from(Array(payload.pages), () => new Array());
            courses[payload.id-1] = [...payload.courses]
            
            return { courses: courses }

        }
        else if(!!payload.certifications){

            let certifications = [...state.certifications];
            if(certifications.length === 0)   certifications = Array.from(Array(payload.pages), () => new Array());
            certifications[payload.id-1] = [...payload.certifications]

            return { certifications: certifications}
        }
        else {
            return { }
        }
    }
}

export const InDemandProductsReducer = (state=inDemandProductsState, action) => {
    switch(action.type){
        case inDemandProductsFetched.type : return {...state, ...appendProduct(state, action )}
        default : return state;
    }
}

const jobAssistanceAndBlogsState = {
    jobAssistanceServices : [],
    latestBlog : []
}

export const JobAssistanceAndBlogsReducer = (state=jobAssistanceAndBlogsState, action) => {
    switch(action.type){
        case jobAssistanceAndBlogsFetched.type : return {...jobAssistanceAndBlogsState, ...action.payload}
        default : return state;
    }
}

const testimonialsState = {
    // data : []
}

export const TestimonialsReducer = (state=testimonialsState, action) => {
    switch(action.type){
        case testimonialsFetched.type : return {...testimonialsState, ...action?.payload?.item}
        default : return state;
    }
}


const skillwithDemandsState = {
    skillDemand: []
}

export const SkillwithDemandsReducer = (state=skillwithDemandsState, action) => {
    switch(action.type) {
        case skillwithDemandsFetched.type : return {...skillwithDemandsFetched, ...action.payload.item}
        default : return state;
    }
}