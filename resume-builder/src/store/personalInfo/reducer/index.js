import {SAVE_PERSONAL_INFO} from "../actions/actionTypes";

const initialState = {
    first_name: '',
    last_name: '',
    email: '',
    number: '',
    image: '',
    date_of_birth: '',
    location: '',
    gender: '',

};


export const personalInfoReducer = (state = initialState, action) => {
    switch (action.type) {

        case SAVE_PERSONAL_INFO: {
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

