import {
    mostViewedCoursesFetched,
    inDemandProductsFetched,
    jobAssistanceAndBlogsFetched,
    testimonialsFetched,
    skillwithDemandsFetched
} from './actions';

const mostViewedCoursesState = {
    mostViewedCourses: {}
}

export const MostViewedCoursesReducer = (state = mostViewedCoursesState, action) => {
    switch (action.type) {
        case mostViewedCoursesFetched.type: return { mostViewedCourses: { ...state.mostViewedCourses, ...action.payload } }
        default: return state;
    }
}

const inDemandProductsState = {
    courses: [],
    certifications: []
}

const appendProduct = (state, { payload }) => {
    if (payload.device === 'mobile') {
        if (!!payload.courses) {
            let courses;
            if (state.type === 'desktop') {
                courses = [ ...payload.courses];
            }
            else {
                courses = [...state.courses, ...payload.courses];
            }
            return { courses, type: 'mobile' };
        }
        else if (!!payload.certifications) {
            let certifications;
            if(state.type === 'desktop'){
                certifications = [ ...payload.certifications];
            }
            else{
                certifications = [...state.certifications, ...payload.certifications];
            }
            return { certifications, type: 'mobile' }
        }
        else {
            return {}
        }
    }
    else {
        if (!!payload.courses) {
            let courses ;
            if(state.type === 'mobile'){
                courses = [];
            } 
            else{
                courses =  [...state.courses];
            }

            if (courses.length === 0 || !Array.isArray(courses[0])) {
                courses = Array.from(Array(payload.pages), () => new Array());
            }

            courses[payload.id - 1] = [...payload.courses]

            return { courses, type: 'desktop' }

        }
        else if (!!payload.certifications) {

            let certifications;
            if(state.type === 'mobile'){
                certifications = [];
            } 
            else{
                certifications =  [...state.certifications];
            }

            if (certifications.length === 0 || !Array.isArray(certifications[0])) certifications = Array.from(Array(payload.pages), () => new Array());

            certifications[payload.id - 1] = [...payload.certifications]

            return { certifications, type: 'desktop' }
        }
        else {
            return {}
        }
    }
}

export const InDemandProductsReducer = (state = inDemandProductsState, action) => {
    switch (action.type) {
        case inDemandProductsFetched.type: return { ...state, ...appendProduct(state, action) }
        default: return state;
    }
}

const jobAssistanceAndBlogsState = {
    jobAssistanceServices: [],
    latestBlog: []
}

export const JobAssistanceAndBlogsReducer = (state = jobAssistanceAndBlogsState, action) => {
    switch (action.type) {
        case jobAssistanceAndBlogsFetched.type: return { ...jobAssistanceAndBlogsState, ...action.payload }
        default: return state;
    }
}

const testimonialsState = {
    testimonialCategory: [],
    meta : {}
}

export const TestimonialsReducer = (state = testimonialsState, action) => {
    switch (action.type) {
        case testimonialsFetched.type: return { ...testimonialsState, ...action?.payload }
        default: return state;
    }
}


const skillwithDemandsState = {
    skillDemand: []
}

export const SkillwithDemandsReducer = (state = skillwithDemandsState, action) => {
    switch (action.type) {
        case skillwithDemandsFetched.type: return { ...skillwithDemandsFetched, ...action?.payload?.item }
        default: return state;
    }
}