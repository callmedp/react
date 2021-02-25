import { fetchedUserIntentData, careerChangeDataFetched, findRightJobsDataFetched, serviceRecommendationFetched, uploadFileUrl, upskillYourselfDataFetched } from './actions';

const userIntentState = {
    userIntent: [
        {
            "id": 3987,
            "name": "Neo Test",
            "about": "assa",
            "url": "/course/sales-and-marketing/neo-test/pd-3987",
            "imgUrl": "https://learning-media-staging-189607.storage.googleapis.com/l2/m/product_image/3987/1613459220_7943.png",
            "imgAlt": "Neo Test",
            "title": "Neo Test (INR 123) - Shine Learning",
            "slug": "neo-test",
            "jobsAvailable": 0,
            "skillList": [
                "Java",
                "Python",
                "php",
                "English",
                "C++"
            ],
            "rating": 4.85,
            "stars": [
                "*",
                "*",
                "*",
                "*",
                "*"
            ],
            "mode": "Instructor Led",
            "providerName": "Neo",
            "price": 1000.0,
            "tags": 0,
            "highlights": [
                "sasa"
            ],
            "duration": "90 Days",
            "brochure": null,
            "u_courses_benefits": null,
            "u_desc": "<p>sdaas</p>",
            "duration": 3,
            "type": "TR",
            "label": "Neo Trial",
            "level": "Beginner"
        }
    ]
}

export const userIntentReducer = (state=userIntentState, action) => {
    switch(action.type) {
        case fetchedUserIntentData.type : return {...state.userIntent, ...action.payload}
        default: return state;
    }
}

const careerChangeState = {
    course_data: [],
    page: {}
}

export const careerChangeReducer = (state=careerChangeState, action) => {
    switch(action.type) {
        case careerChangeDataFetched.type : return {...state.careerChangeDataFetched, ...action?.payload?.item}
        default: return state;
    }
}

const findRightJobsState = {
    jobsList: {
        page: 1,
        results: [],
        next: ""
    },
}


export const findRightJobsReducer = (state=findRightJobsState, action) => {
    switch(action.type) {
        case findRightJobsDataFetched.type : return {
            ...state,
            jobsList: {
                page: action.payload.jobsList.page ?? 1,
                next: action.payload.jobsList.next ?? '',
                results: [...state.jobsList.results, ...(action.payload.jobsList.results ?? [])]
            }
        }
        default: return state;
    }
}

const upskillYourselfState = {
    course_data: [],
    page: {},
    recommended_course_ids: []
}

export const upskillYourselfReducer = (state=upskillYourselfState, action) => {
    switch(action.type) {
        case upskillYourselfDataFetched.type : return {
            ...state,
            page:action.payload.page ?? {},
            recommended_course_ids: action.payload.recommended_course_ids ?? [],
            course_data: [...state.course_data, ...(action.payload.course_data ?? [])]
        }
        default: return state;
    }
}

const serviceRecommendationState = {
    services: [],
    page: {}
}

export const serviceRecommendationReducer = (state=serviceRecommendationState, action) => {
    switch(action.type) {
        case serviceRecommendationFetched.type : return {...state.serviceRecommendationFetched, ...action.payload}
        default: return state;
    }
}

const initialState = {
    total_score : 0
};


export const ResumeScoreReducer = (state = initialState, action) => {
    switch (action.type) {
        case uploadFileUrl.type : {
            return {
                ...state,
                ...action.payload
            }
        }
        default: {
            return state;
        }
    }
};