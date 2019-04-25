import {SAVE_USER_INFO,UPDATE_PERSONAL_INFO} from "../actions/actionTypes";

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
    extra_info: ''


};


export const personalInfoReducer = (state = initialState, action) => {
    console.log(action)
    switch (action.type) {
        case SAVE_USER_INFO: {
            return {
                ...state,
                ...action.data
            };
        }
        default: {
            return state;
        }
    }
};

