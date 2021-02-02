import { mostViewedCoursesFetched,
    inDemandProductsFetched,
    jobAssistanceAndBlogsFetched, 
    skillwithDemandsFetched} from './actions';

const mostViewedCoursesState = {
    recentCoursesList : []
}

export const MostViewedCoursesReducer = (state=mostViewedCoursesState, action) => {
    switch(action.type){
        case mostViewedCoursesFetched.type  : return {...mostViewedCoursesState, ...action.item}
        default : return state;
    }
}

const inDemandProductsState = {
    courses : [],
    certifications : []
}

const getProduct = (state, action) => {
    if( action.device === 'mobile' )
    return {
        // gaurav, write mobile logic to store product
    }
    else {

        if(!!action.courses){

            let courses = [...state.courses];
            if(courses.length === 0)    courses = Array.from(Array(action.pages), () => new Array());
            courses[action.id] = [...action.courses]
            
            return { courses: courses }

        }
        else if(!!action.certifications){

            let certifications = [...state.certifications];
            if(certifications.length === 0)   certifications = Array.from(Array(action.pages), () => new Array());
            certifications[action.id] = [...action.certifications]

            return { certifications: certifications}
        }
        else {
            return { }
        }
    }
}

export const InDemandProductsReducer = (state=inDemandProductsState, action) => {
    switch(action.type){
        case inDemandProductsFetched.type : return {...state, ...getProduct(state, action)}
        default : return state;
    }
}

const jobAssistanceAndBlogsState = {
    recentCoursesList : []
}

export const JobAssistanceAndBlogsReducer = (state=jobAssistanceAndBlogsState, action) => {
    switch(action.type){
        case jobAssistanceAndBlogsFetched.type : return {...jobAssistanceAndBlogsState, ...action.item}
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