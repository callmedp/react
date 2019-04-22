import {SAVE_USER_INFO} from "../actions/actionTypes";

const initialState = {
    first_name: '',
    last_name: '',
    email: '',
    number: '',
    image: '',
    date_of_birth: '',
    location: '',
    gender: '',
    extracurricular: '',
    extra_info: '',
    entity_preference_data: []


};


export const personalInfoReducer = (state = initialState, action) => {
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

