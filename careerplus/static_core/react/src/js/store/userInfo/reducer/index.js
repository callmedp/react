import {FETCH_HOME_DATA, STORE_USER_INFO, SAVE_DEFAULT_SKILL_LIST, ADD_PROJECT, GET_PROJECT_DETAIL} from "../actions/actionTypes";

const initialState = {
    id: '',
    first_name: '',
    last_name: '',
    email: '',
    number: '',
    projects: []
};


const userInfoReducer = (state = initialState, action) => {
    switch (action.type) {
        case FETCH_HOME_DATA: {
            return {
                ...state
            };
        }

        case STORE_USER_INFO: {
            return {
                ...state,
                ...action.data
            };
        }
        case ADD_PROJECT: {
            return {
                ...state,
                ...action.data

            }
        }
        default : {
            return state;
        }
    }
};

const skillReducer = (state = {
    defaultList: ''
}, action) => {
    switch (action.type) {
        case SAVE_DEFAULT_SKILL_LIST: {
            return {
                ...state,
                ...action.data
            }
        }
        default : {
            return state;
        }
    }
}

const projectReducer = (state = {}, action) => {
     switch (action.type){
         case GET_PROJECT_DETAIL:
     }
}

export const UserReducer = {
    skillReducer,
    userInfoReducer
};