import * as Actions from '../actions/actionTypes';

const initState = {
    data: {
        wal_total: 0,
        page: [],
        loyality_txns: []
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