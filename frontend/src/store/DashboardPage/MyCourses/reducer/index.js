import * as Actions from '../actions/actionTypes';

const initState = {
    data: {
        heading: "",
        id: 0,
        img: "",
        img_alt: "",
        name: "",
        price: 0,
        provider: "",
        rating: 0,
        stars: [],
        url: ""
    },
    error: false,
    message: ""
}

export const DashboardMyCoursesReducer = (state=initState, action) => {
    switch(action.type){
        case Actions.MY_COURSES_FETCHED : return { ...initState,...action.item}
        default: return state;
    }
}