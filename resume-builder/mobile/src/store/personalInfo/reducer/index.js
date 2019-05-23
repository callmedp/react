import {SAVE_USER_INFO,SAVE_INTEREST_LIST} from "../actions/actionTypes";

const initialState = {
    first_name: '',
    last_name: '',
    email: '',
    number: '',
    image: '',
    date_of_birth: '',
    location: '',
    gender: '',
    entity_preference_data : [],
    extracurricular: [],
    extra_info: '',
    interest_list:['loading...']


};


export const personalInfoReducer = (state = initialState, action) => {
    switch (action.type) {
        case SAVE_USER_INFO: {
            return {
                ...state,
                ...action.data
            };
        }
        case SAVE_INTEREST_LIST: {
            return {
                ...state,
                ...{
                    interest_list:action.data
                }
            }
        }
        default: {
            return state;
        }
    }
};

